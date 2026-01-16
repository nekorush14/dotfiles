#!/bin/bash
# ~/.local/bin/tmux-short-path.sh

path="$1"

# 引数が空の場合は現在のディレクトリを使用
if [[ -z "$path" ]]; then
  path="$(pwd)"
fi

# ホームディレクトリを~に置換
path="${path/#$HOME/~}"

# パスを/で分割
IFS='/' read -ra parts <<<"$path"
result=""

# 各部分を処理
for i in "${!parts[@]}"; do
  part="${parts[$i]}"

  if [[ $i -eq 0 ]]; then
    # 最初の部分（~や空文字、ルート/）
    result="$part"
  elif [[ $i -eq $((${#parts[@]} - 1)) ]]; then
    # 最後のディレクトリはフル表示
    if [[ -n "$part" ]]; then
      result="$result/$part"
    fi
  else
    # 中間ディレクトリの処理
    if [[ -n "$part" ]]; then
      if [[ "$part" =~ ^\. ]]; then
        # .で始まるディレクトリは.と直後の1文字を表示
        if [[ ${#part} -gt 1 ]]; then
          result="$result/${part:0:2}"
        else
          result="$result/$part"
        fi
      else
        # 通常のディレクトリは最初の1文字のみ
        result="$result/${part:0:1}"
      fi
    fi
  fi
done

echo "$result"
