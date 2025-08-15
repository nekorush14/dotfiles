# 汎用開発環境設定

このファイルは、Claude Codeのベストプラクティスに従った汎用的な開発環境設定です。

## プロジェクトの概要

様々なプログラミング言語とフレームワークを使用した開発プロジェクト用の汎用設定。

## 開発コマンド

### リント・フォーマット
```bash
# JavaScript/TypeScript
npm run lint
npm run lint:fix
npm run format

# Python
ruff check .
ruff format .
black .
flake8 .

# Go
go fmt ./...
golint ./...

# Rust
cargo fmt
cargo clippy
```

### テスト実行
```bash
# JavaScript/TypeScript
npm test
npm run test:watch
npm run test:coverage

# Python
pytest
pytest --cov=.

# Go
go test ./...

# Rust
cargo test
```

### ビルド
```bash
# JavaScript/TypeScript
npm run build
npm run dev

# Go
go build

# Rust
cargo build
cargo run
```

## コーディング規約

### 共通ルール
- インデント: 2スペース（YAML, JSON, JavaScript/TypeScript）
- インデント: 4スペース（Python）
- インデント: タブ（Go）
- 改行コード: LF
- 文字エンコーディング: UTF-8
- ファイル末尾に改行を追加

### 言語別ルール
- **JavaScript/TypeScript**: ESLint + Prettier
- **Python**: PEP8準拠、型ヒント推奨
- **Go**: 標準フォーマッタに従う
- **Rust**: rustfmt + clippy

## ディレクトリ構造

```
project/
├── src/          # ソースコード
├── tests/        # テストファイル
├── docs/         # ドキュメント
├── config/       # 設定ファイル
├── scripts/      # ビルド・デプロイスクリプト
└── .github/      # GitHub Actions
```

## 推奨ツール

### エディタ・IDE
- Visual Studio Code
- Neovim
- IntelliJ IDEA / WebStorm

### バージョン管理
- Git
- 適切な .gitignore の設定
- コミットメッセージ規約（Conventional Commits）

### パッケージマネージャー
- **Node.js**: npm, yarn, pnpm
- **Python**: pip, poetry, conda
- **Go**: go mod
- **Rust**: cargo

## セキュリティ

- 秘密情報は環境変数で管理
- .env ファイルは .gitignore に追加
- 依存関係の脆弱性チェック実行

## パフォーマンス

- コードレビューでパフォーマンスを考慮
- 適切なキャッシュ戦略
- メモリリークの監視

## 備考

このファイルは Claude Code が効率的にコードを理解・編集するためのガイドラインです。プロジェクト固有の要件に応じて適宜カスタマイズしてください。