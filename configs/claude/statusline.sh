#!/bin/bash

# Disable shell initialization that might interfere
export ZOXIDE_INIT_ENABLED=0
unset -f cd

# Read JSON input from stdin
input=$(cat)

# Escape single quotes in the input for safe passing to Node.js
escaped_input=$(echo "$input" | sed "s/'/'\\\\''/g")

# Use Node.js to process the JSON and generate the status line
node -e "
const fs = require('fs');
const { spawn } = require('child_process');

const data = JSON.parse('$escaped_input');

function formatTokens(tokens) {
  if (tokens >= 1_000_000) {
    return \`\${(tokens / 1_000_000).toFixed(1)}M tok\`;
  } else if (tokens >= 1_000) {
    return \`\${(tokens / 1_000).toFixed(1)}k tok\`;
  }
  return \`\${tokens.toString()} tok\`;
}

function getColorForPercentage(percentage) {
  if (percentage < 70) {
    return '\x1b[32m'; // Green
  } else if (percentage < 90) {
    return '\x1b[33m'; // Yellow
  } else {
    return '\x1b[31m'; // Red
  }
}

function colorize(text, color) {
  if (!color) return text;
  return \`\${color}\${text}\x1b[0m\`;
}

const colors = {
  brightYellow: '\x1b[93m',
  brightBlue: '\x1b[94m',
  brightWhite: '\x1b[97m',
  brightMagenta: '\x1b[95m',
  brightOrange: '\x1b[38;5;214m',
  white: '\x1b[37m'
};

function formatCurrentDir(currentDir) {
  if (!currentDir) return '';

  const homeDir = process.env.HOME || process.env.USERPROFILE || '';
  if (!homeDir || !currentDir.startsWith(homeDir)) {
    return currentDir;
  }

  const relativePath = currentDir.slice(homeDir.length).replace(/^\//, '');
  const pathParts = relativePath.split('/').filter(part => part !== '');

  if (pathParts.length <= 1) {
    return pathParts.length === 0 ? '~' : \`~/\${pathParts.join('/')}\`;
  }

  const lastTwoParts = pathParts.slice(-1);
  return \`~/…/\${lastTwoParts.join('/')}\`;
}

function getGitBranch() {
  try {
    const { execSync } = require('child_process');
    const branch = execSync('git rev-parse --abbrev-ref HEAD 2>/dev/null', { 
      cwd: process.cwd(),
      encoding: 'utf8'
    }).trim();
    return branch ? \` \${branch}\` : '';
  } catch {
    return '';
  }
}

function getGitDiffStats() {
  try {
    const { execSync } = require('child_process');
    const output = execSync('git diff --numstat 2>/dev/null', { 
      cwd: process.cwd(),
      encoding: 'utf8'
    });
    
    const lines = output.trim().split('\n');
    let additions = 0;
    let deletions = 0;

    for (const line of lines) {
      if (line.trim()) {
        const [add, del] = line.split('\t');
        if (add !== '-' && del !== '-') {
          additions += parseInt(add) || 0;
          deletions += parseInt(del) || 0;
        }
      }
    }

    return { additions, deletions };
  } catch {
    return { additions: 0, deletions: 0 };
  }
}

function getClaudeVersion() {
  try {
    const { execSync } = require('child_process');
    const version = execSync('claude -v 2>/dev/null', { encoding: 'utf8' }).trim();
    return version;
  } catch {
    return '';
  }
}

// Calculate total tokens from transcript file
let totalTokens = 0;

if (data.transcript_path) {
  try {
    const content = fs.readFileSync(data.transcript_path, 'utf8');
    const lines = content.trim().split('\n');

    let lastUsage = null;

    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        if (entry.type === 'assistant' && entry.message?.usage) {
          lastUsage = entry.message.usage;
        }
      } catch {
        // Skip invalid JSON lines
      }
    }

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

let modelName = 'Unknown';

if (data.model?.display_name?.startsWith('arn:aws:')) {
  modelName = 'by AWS Bedrock';
} else {
  modelName = data.model?.display_name || 'Unknown';
}

const tokensDisplay = formatTokens(totalTokens);
const gitBranch = getGitBranch();
const diffStats = getGitDiffStats();
const gitStats = gitBranch && (diffStats.additions > 0 || diffStats.deletions > 0)
  ? \` (+\${diffStats.additions}, -\${diffStats.deletions})\`
  : '';

const currentDir = formatCurrentDir(data.workspace?.current_dir || '');
const usageCostUsd = \`\${(data.cost?.total_cost_usd || 0).toFixed(2)} USD\`;
const claudeVersion = getClaudeVersion();

process.stdout.write(
  \`\\x1b[0m\${colorize(\`  \${modelName}\`, colors.brightYellow)} | \${colorize(
    \`  \${currentDir}\`,
    colors.brightBlue
  )} | \${colorize(gitBranch, colors.brightOrange)}\${colorize(
    gitStats,
    colors.brightOrange
  )}\\n\\x1b[0m\${colorize(
    \`󰭻 : \${tokensDisplay}\`,
    colors.brightWhite
  )} | \${color}󰈙 : \${percentage}%\\x1b[0m | \${colorize(
    \` : \${usageCostUsd}\`,
    colors.brightMagenta
  )}\${
    claudeVersion ? \` | \${colorize(\`v\${claudeVersion}\`, colors.white)}\` : ''
  }\\x1b[0m \`
);
" 2>/dev/null
