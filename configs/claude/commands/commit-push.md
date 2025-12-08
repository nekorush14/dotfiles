---
description: Create a commit message and execute commit, also push to remote repository.
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git diff:*), Bash(git log:*)
argument-hint: [scope]
---
# Create a commit and Push to remote repository

Your task is to create a git commit message and execute the commit.
You must follow the flow section.

## Flow

1. YOU **DO NOT** run `git add .` command to stage file. (You must run `git add <file>`
command to stage file.)
2. Run `git status` to confirm the files to be committed.
3. Commit it by following the rule of [conversational commit](https://www.conventionalcommits.org/en/v1.0.0/).
4. Push it to remote repository.

### Available types

- `feat(<scope>): <commit abstract>` # Use when you add a new feature
- `fix(<scope>): <commit abstract>` # Use when you fix a bug
- `docs(<scope>): <commit abstract>` # Use when you add or update documentation
- `refactor(<scope>): <commit abstract>` # Use when you change the code structure without changing the behavior
- `test(<scope>): <commit abstract>` # Use when you add or update test code
- `ci(<scope>): <commit abstract>` # Use when you change the CI configuration files and scripts
- `chore(<scope>): <commit abstract>` # Use when you change the build process or auxiliary tools and libraries such as documentation generation

Scope identifier will use $ARGUMENTS provided by user.
If no define the scope identifier, you confirm the changes for this commit from git diffs.

### Additional prioritized rules

If it contains the implementation of product code and test code, then you have to use a `feat` or `fix` type instead of `test` type.

## Example commit message

```txt
feat(auth_controller): Add login functionality
fix(example_api_handler): Resolve user data fetching issue
docs(readme): Update installation instructions
```

## Security Considerations

- NEVER use `git push --force` without explicit user approval
- **DO NOT** commit sensitive files (.env, credentials.json, *.pem, etc.)
- Warn the user if such files are staged
