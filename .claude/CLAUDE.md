# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## リポジトリ概要

クロスプラットフォーム開発環境（主にmacOS、Linux、WSL）向けの設定ファイルとセットアップスクリプトを含む包括的なdotfilesリポジトリです。ターミナルエミュレータ、エディタ、ウィンドウマネージャー、開発ツールなどの設定を管理しています。

## アーキテクチャ

### コア構造
- `configs/` - アプリケーション別に整理された最新の設定ファイル
- `bin/` - パッケージインストールと環境セットアップ用ユーティリティスクリプト
- `brew/` - Homebrewパッケージ管理
- `zsh/` - シェル設定
- `tmux/` - ターミナルマルチプレクサセットアップ
- `obsolete/` - レガシー設定と非推奨セットアップスクリプト
- `dev/` - 開発固有の設定とアーカイブ

### 設定管理の哲学
リポジトリは`configs/`下で各アプリケーションが専用の設定ディレクトリを持つモジュラーアプローチに従っています。これにより個々のツール設定のクリーンな分離と容易なメンテナンスが可能です。

## セットアップコマンド

### 初期環境セットアップ
```bash
# リポジトリのクローン
cd && git clone https://github.com/nekorush14/dotfiles.git

# メインセットアップスクリプトの実行（レガシー - obsolete/setup.shを参照）
./dotfiles/setup.sh
```

### パッケージ管理
```bash
# Homebrewパッケージのインストール
brew bundle --file=brew/Brewfile

# 開発パッケージのセットアップ
./bin/node-setup.sh    # Claude Codeを含むNode.js CLIツールのインストール
./bin/ruby-packages.sh # Ruby gemのインストール
./bin/cargo-packages.sh # Rustパッケージのインストール（spotify_player、rmpc）
```

### アプリケーション固有のセットアップ
```bash
# brewファイル管理
cd dev/brew && ./setup.sh

# tmuxセットアップ
./tmux/tmux-setup.sh
```

## 主要設定ファイル

### 開発ツール
- `configs/nvim/` - LazyVimセットアップ付きNeovim設定
- `configs/code/` - VS Code設定、キーバインド、拡張機能
- `configs/claude/` - Claude Code設定とオプション

### シェル＆ターミナル
- `configs/starship.toml` - シェルプロンプト設定
- `configs/ghostty/config` - モダンターミナルエミュレータ設定
- `configs/zellij/config.kdl` - ターミナルワークスペースマネージャー

### macOSウィンドウ管理
- `configs/yabai/yabairc` - タイリングウィンドウマネージャー
- `configs/skhd/skhdrc` - ホットキーデーモン設定

### 開発環境
- `configs/lazygit/config.yml` - Git TUI設定
- `configs/bat/` - シンタックスハイライト付きbetter cat
- `configs/yazi/` - ターミナルファイルマネージャー

## 開発ツールセットアップ

### Node.js環境
`bin/node-setup.sh`スクリプトは必須CLIツールをインストールします：
- `@anthropic-ai/claude-code` - Claude Code CLI
- `ccusage@latest` - 使用量追跡
- `@google/gemini-cli` - Google Gemini CLI
- `neovim` - Neovim Node.jsサポート
- `safe-rm` - 安全なファイル削除

### Rust環境
Cargoパッケージは`bin/cargo-packages.sh`で管理：
- `spotify_player` - 画像とfzfサポート付きターミナルSpotifyクライアント
- `rmpc` - MPDクライアント

### Ruby環境
Ruby gemは`bin/ruby-packages.sh`でインストール：
- `neovim` - Neovim Rubyサポート

## ファイルリンク戦略

リポジトリは設定をデプロイするためにシンボリックリンクを使用します。レガシーの`obsolete/setup.sh`には以下を行う`slink()`関数を含むコアリンクロジックが含まれています：
1. 既存のファイル/リンクをチェック
2. 競合するファイルを削除
3. リポジトリからホームディレクトリへのシンボリックリンクを作成

## 重要な注意事項

- `obsolete/`ディレクトリには機能する可能性があるがモダンなモジュラーアプローチに置き換えられたレガシーセットアップスクリプトが含まれています
- `configs/`内の設定ファイルは現在の、積極的にメンテナンスされているセットアップを表します
- `dev/`ディレクトリには開発スナップショットとアーカイブ設定が含まれています
- HomebrewはmacOS用の主要パッケージマネージャーで、`brew/Brewfile`に包括的なパッケージリストがあります

## クロスプラットフォームサポート

リポジトリは複数のプラットフォームをサポートします：
- **macOS**: ウィンドウ管理（yabai/skhd）とHomebrewを含む完全サポート
- **Linux**: 基本的なシェルと開発ツール設定
- **WSL**: Windows Subsystem for Linux互換性

レガシーセットアップスクリプト（`obsolete/setup.sh`）には、OS検出とプラットフォーム固有の設定デプロイが含まれています。