---
inclusion: always
---
# Git 規約

## Commit Message

- Conventional Commits に従う
    - feat: 新機能
    - fix: バグ修正
    - docs: ドキュメント変更
    - refactor: コード再構築
    - test: テストの追加/変更
- 形式：`type(scope): description`
    - 例：`feat(auth): Add support OAuth2`
- Kiro によるコミットにはトレーラーとして `Co-authored-by: Kiro Agent <244629292+kiro-agent@users.noreply.github.com>` を付与
- Commit Message は英語

## Branch

- トランクベースのシンプルな戦略を取る
    - `main`: 本番リリース
    - `nekorush14/<feature-name>`
        - 例: `nekorush14/add-cognito-auth-frontend`, `nekorush14/fix-login-form-styles`
