---
description: "Create a commit message and exetute commit, also push to remote repository."
---
# Create a commit and Push to remote repository

Your task is to create a git commit message and execute the commit.
You must follow the flow section.

## Flow

1. YOU **DO NOT** run `git add` command to stage file. (Only pre-staged files will contain in the commit.)
2. Run `git status` to confirm the files to be committed.
3. Commit it by following the rule of [conversational commit](https://www.conventionalcommits.org/en/v1.0.0/).
4. Push it to remote repository.

## Commit message rule

You must follow the rule of [conversational commit](https://www.conventionalcommits.org/en/v1.0.0/) and you must write commit message by English.
You also follow the following type.

### Available types

- `feat(<scope>): <commit abstract>` # Use when you add a new feature
- `fix(<scope>): <commit abstract>` # Use when you fix a bug
- `docs(<scope>): <commit abstract>` # Use when you add or update documentation
- `refactor(<scope>): <commit abstract>` # Use when you change the code structure without changing the behavior
- `test(<scope>): <commit abstract>` # Use when you add or update test code
- `ci(<scope>): <commit abstract>` # Use when you change the CI configuration files and scripts
- `chore(<scope>): <commit abstract>` # Use when you change the build process or auxiliary tools and libraries such as documentation generation

### Additional prioritized rules

If it contains the implementation of product code and test code, then you have to use a `feat` or `fix` type instead of `test` type.

## Example commit message

```
feat(auth): add login functionality
fix(api): resolve user data fetching issue
docs(readme): update installation instructions
```
