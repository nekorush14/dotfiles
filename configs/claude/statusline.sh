#!/bin/bash

# 色の定義
MODEL_NAME_COLOR='\033[38;2;135;206;250m'    # #87cefa
INPUT_TOKENS_COLOR='\033[38;2;0;250;154m'    # #00fa9a
OUTPUT_TOKENS_COLOR='\033[38;2;255;105;180m' # #ff69b4
TOTAL_TOKENS_COLOR='\033[38;2;0;255;255m'    # #00ffff
USAGE_PERCENT_COLOR='\033[38;2;123;104;238m' # #7b68ee
CURRENT_DIR_COLOR='\033[38;2;0;255;0m'       # #00ff00
GIT_BRANCH_COLOR='\033[38;2;72;209;204m'     # #48d1cc
GIT_DIFF_COLOR='\033[38;2;255;255;0m'        # #ffff00
RESET_COLOR='\033[0m'

# トークン使用量の上限（200K）
readonly MAX_TOKENS=200000

# JSON入力から情報を取得
parse_json_input() {
  local json_input=""
  if [[ -p /dev/stdin ]]; then
    json_input=$(cat)
  else
    json_input="$1"
  fi

  # JSON から基本情報を取得
  local transcript_path=""
  local current_dir_name=$(basename "$PWD")
  
  if [[ -n "$json_input" && "$json_input" != "" ]]; then
    transcript_path=$(echo "$json_input" | jq -r '.transcript_path // ""' 2>/dev/null)
    current_dir_name=$(echo "$json_input" | jq -r '.workspace.current_dir // .cwd' 2>/dev/null | xargs basename 2>/dev/null || echo "$(basename "$PWD")")
  fi

  # トランスクリプトファイルからトークン使用量を取得
  local input_tokens=0
  local output_tokens=0

  if [[ -n "$transcript_path" && -f "$transcript_path" ]]; then
    # トランスクリプトファイルの最後のassistantメッセージのusageを取得
    while IFS= read -r line; do
      if echo "$line" | jq -e '.message.role == "assistant"' >/dev/null 2>&1; then
        local usage=$(echo "$line" | jq -r '.message.usage // empty')
        if [[ -n "$usage" && "$usage" != "null" ]]; then
          input_tokens=$(echo "$usage" | jq -r '(.input_tokens // 0) + (.cache_creation_input_tokens // 0) + (.cache_read_input_tokens // 0)')
          output_tokens=$(echo "$usage" | jq -r '.output_tokens // 0')
        fi
      fi
    done <"$transcript_path"
  fi

  local total_tokens=$((input_tokens + output_tokens))
  local usage_percent=0
  if [[ $total_tokens -gt 0 ]]; then
    usage_percent=$(((total_tokens * 100) / MAX_TOKENS))
  fi

  # k単位に変換
  local input_tokens_k=$(((input_tokens + 500) / 1000))
  local output_tokens_k=$(((output_tokens + 500) / 1000))
  local total_tokens_k=$(((total_tokens + 500) / 1000))

  echo "$input_tokens_k" "$output_tokens_k" "$total_tokens_k" "$usage_percent" "$current_dir_name"
}

# 現在のディレクトリ表示を取得
get_current_dir() {
  local dir_name="$1"
  local current_path=$(pwd)
  local home_path="$HOME"

  if [[ "$current_path" == "$home_path" ]]; then
    echo "~"
  elif [[ "$current_path" == "$home_path"/* ]]; then
    local relative_path="${current_path#$home_path/}"
    # ホームディレクトリから1階層まで
    if [[ "$relative_path" != */* ]]; then
      echo "~/$relative_path"
    else
      echo "$dir_name"
    fi
  else
    echo "$dir_name"
  fi
}

# Gitブランチ名を取得
get_git_branch() {
  if git rev-parse --git-dir >/dev/null 2>&1; then
    git branch --show-current 2>/dev/null || echo "HEAD"
  else
    echo ""
  fi
}

# Git Diff行数を取得
get_git_diff() {
  if git rev-parse --git-dir >/dev/null 2>&1; then
    local diff_stats=$(git diff --numstat 2>/dev/null | awk '{added+=$1; deleted+=$2} END {print added, deleted}')
    local added=$(echo $diff_stats | cut -d' ' -f1)
    local deleted=$(echo $diff_stats | cut -d' ' -f2)

    if [[ "$added" == "" ]]; then added=0; fi
    if [[ "$deleted" == "" ]]; then deleted=0; fi

    if [[ $added -gt 0 || $deleted -gt 0 ]]; then
      echo "(+$added, -$deleted)"
    else
      echo ""
    fi
  else
    echo ""
  fi
}

# ccusageコマンドの実行結果を取得
get_ccusage_statusline() {
  if command -v ccusage &>/dev/null; then
    ccusage statusline 2>/dev/null || echo ""
  else
    echo ""
  fi
}

# メイン処理
main() {
  local json_input=""
  if [[ $# -gt 0 ]]; then
    json_input="$1"
  fi

  read -r input_tokens output_tokens total_tokens usage_percent dir_name <<<$(parse_json_input "$json_input")
  local current_dir=$(get_current_dir "$dir_name")
  local git_branch=$(get_git_branch)
  local git_diff=$(get_git_diff)
  local ccusage_result=$(get_ccusage_statusline)

  # 1行目: トークン情報
  echo -e "${INPUT_TOKENS_COLOR}  ${input_tokens}k${RESET_COLOR} | ${OUTPUT_TOKENS_COLOR} ${output_tokens}k${RESET_COLOR} | ${TOTAL_TOKENS_COLOR}󰷈  ${total_tokens}k${RESET_COLOR} | ${USAGE_PERCENT_COLOR}󰳲  ${usage_percent}%${RESET_COLOR}"

  # 2行目: ディレクトリとGit情報
  local line2="${CURRENT_DIR_COLOR}  ${current_dir}${RESET_COLOR}"
  if [[ -n "$git_branch" ]]; then
    line2="${line2} | ${GIT_BRANCH_COLOR} ${git_branch}${RESET_COLOR}"
  fi
  if [[ -n "$git_diff" ]]; then
    line2="${line2} | ${GIT_DIFF_COLOR} ${git_diff}${RESET_COLOR}"
  fi
  echo -e "$line2"

  # 3行目: ccusage結果
  if [[ -n "$ccusage_result" ]]; then
    echo -e "\033[38;2;255;255;255m${ccusage_result}\033[0m"
  fi
}

main "$@"
