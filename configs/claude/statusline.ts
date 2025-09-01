#!/usr/bin/env bun

interface SessionData {
  model: {
    display_name: string;
  };
  workspace: {
    current_dir: string;
  };
  transcript_path?: string;
  session_id?: string;
  cwd?: string;
  version?: string;
  cost: {
    total_cost_usd?: number;
  };
}

interface TranscriptEntry {
  type: string;
  message?: {
    usage?: {
      input_tokens?: number;
      output_tokens?: number;
      cache_creation_input_tokens?: number;
      cache_read_input_tokens?: number;
    };
  };
}

function formatTokens(tokens: number): string {
  if (tokens >= 1_000_000) {
    return `${(tokens / 1_000_000).toFixed(1)}M`;
  } else if (tokens >= 1_000) {
    return `${(tokens / 1_000).toFixed(1)}k`;
  }
  return tokens.toString();
}

function getColorForPercentage(percentage: number): string {
  if (percentage < 70) {
    return "\x1b[32m"; // Green
  } else if (percentage < 90) {
    return "\x1b[33m"; // Yellow
  } else {
    return "\x1b[31m"; // Red
  }
}

// Color helper function for status line items
function colorize(text: string, color?: string): string {
  if (!color) return text;
  return `${color}${text}\x1b[0m`;
}

// Predefined colors for easy use
const colors = {
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  magenta: "\x1b[35m",
  cyan: "\x1b[36m",
  white: "\x1b[37m",
  gray: "\x1b[90m",
  brightRed: "\x1b[91m",
  brightGreen: "\x1b[92m",
  brightYellow: "\x1b[93m",
  brightBlue: "\x1b[94m",
  brightMagenta: "\x1b[95m",
  brightCyan: "\x1b[96m",
  brightWhite: "\x1b[97m",
  brightOrange: "\x1b[38;5;214m",
};

function getGitDiffStats(): { additions: number; deletions: number } {
  try {
    const result = Bun.spawnSync(["git", "diff", "--numstat"], {
      cwd: process.cwd(),
      stderr: "ignore",
    });
    if (result.exitCode === 0) {
      const lines = result.stdout.toString().trim().split("\n");
      let additions = 0;
      let deletions = 0;

      for (const line of lines) {
        if (line.trim()) {
          const [add, del] = line.split("\t");
          if (add !== "-" && del !== "-") {
            additions += parseInt(add) || 0;
            deletions += parseInt(del) || 0;
          }
        }
      }

      return { additions, deletions };
    }
  } catch {
    return { additions: 0, deletions: 0 };
  }
  return { additions: 0, deletions: 0 };
}

function getGitBranch(): string {
  // Get current git branch if git branch available
  try {
    const result = Bun.spawnSync(["git", "rev-parse", "--abbrev-ref", "HEAD"], {
      cwd: process.cwd(),
      stderr: "ignore",
    });
    if (result.exitCode === 0) {
      return ` ${result.stdout.toString().trim()}`;
    }
  } catch {
    return "";
  }
  return "";
}

function getClaudeVersion(): string {
  try {
    const result = Bun.spawnSync(["claude", "-v"], {
      stderr: "ignore",
    });
    if (result.exitCode === 0) {
      return result.stdout.toString().trim();
    }
  } catch {
    return "";
  }
  return "";
}

function formatCurrentDir(currentDir: string): string {
  if (!currentDir) return "";

  const homeDir = process.env.HOME || process.env.USERPROFILE || "";
  if (!homeDir || !currentDir.startsWith(homeDir)) {
    return currentDir;
  }

  // Get relative path from home directory
  const relativePath = currentDir.slice(homeDir.length).replace(/^\//, "");
  const pathParts = relativePath.split("/").filter((part) => part !== "");

  // Show full path if 1 levels or less
  if (pathParts.length <= 1) {
    return pathParts.length === 0 ? "~" : `~/${pathParts.join("/")}`;
  }

  // Show abbreviated form with … for 1 or more levels
  const lastTwoParts = pathParts.slice(-1);
  return `~/…/${lastTwoParts.join("/")}`;
}

async function main() {
  const input = await Bun.stdin.text();
  const data: SessionData = JSON.parse(input);

  // Calculate total tokens from transcript file
  let totalTokens = 0;

  if (data.transcript_path) {
    try {
      const file = Bun.file(data.transcript_path);
      const content = await file.text();
      const lines = content.trim().split("\n");

      // Get only the last assistant message with usage info
      let lastUsage = null;

      for (const line of lines) {
        try {
          const entry: TranscriptEntry = JSON.parse(line);
          if (entry.type === "assistant" && entry.message?.usage) {
            lastUsage = entry.message.usage;
          }
        } catch {
          // Skip invalid JSON lines
        }
      }

      // Use the cumulative tokens from the last assistant message
      if (lastUsage) {
        totalTokens =
          (lastUsage.input_tokens || 0) +
          (lastUsage.output_tokens || 0) +
          (lastUsage.cache_creation_input_tokens || 0) +
          (lastUsage.cache_read_input_tokens || 0);
      }
    } catch (error) {
      // If we can't read the transcript, tokens remain 0
    }
  }

  // Auto-compact threshold is 80% of 200K tokens
  const autoCompactThreshold = 160_000;
  const percentage = Math.round((totalTokens / autoCompactThreshold) * 100);
  const color = getColorForPercentage(percentage);

  // Format output: Opus 4.1 | Tokens: 1.0k | Context: 10%
  let modelName = "Unknown";

  // if data.model?.display_name begins with "arn" then set modelName to "Provided by AWS Bedrock"
  if (data.model?.display_name?.startsWith("arn:aws:")) {
    modelName = "by AWS Bedrock";
  } else {
    modelName = data.model?.display_name || "Unknown";
  }

  const tokensDisplay = formatTokens(totalTokens);
  const gtitBranch = getGitBranch();
  const diffStats = getGitDiffStats();
  const gitStats =
    gtitBranch && (diffStats.additions > 0 || diffStats.deletions > 0)
      ? ` (+${diffStats.additions}, -${diffStats.deletions})`
      : "";
  // current dir show last 2 depth from user home with … icon

  const currentDir = formatCurrentDir(data.workspace?.current_dir || "");
  const usageCostUsd = `${(data.cost?.total_cost_usd || 0).toFixed(2)} USD`;
  const claudeVersion = getClaudeVersion();

  process.stdout.write(
    `[0m${colorize(`  ${modelName}`, colors.brightYellow)} | ${colorize(
      `  ${currentDir}`,
      colors.brightBlue
    )} | ${colorize(gtitBranch, colors.brightOrange)}${colorize(
      gitStats,
      colors.brightOrange
    )}\n[0m${colorize(
      `󰭻 Tokens: ${tokensDisplay}`,
      colors.brightWhite
    )} | ${color}󰈙 Context: ${percentage}%[0m | ${colorize(
      `  Costs: ${usageCostUsd}`,
      colors.brightMagenta
    )}${
      claudeVersion ? ` | ${colorize(`v${claudeVersion}`, colors.white)}` : ""
    }[0m `
  );
}

main().catch(console.error);
