# dotfiles

## Description

Dotfiles for each OS. Set up the new environment.

## Install

Download the repository with following command.

```bash
cd && git clone git@github.com:nekorush14/dotfiles.git

# Or using https
cd && git clone https://github.com/nekorush14/dotfiles.git
```

Once done, run the following command to setup the environment.

```bash
# Preview changes (recommended for first run)
./bin/setup.sh -n

# Apply changes
./bin/setup.sh
```

### Options

- `-n, --dry-run`: Show what would be done without making changes
- `-h, --help`: Show help message

### Environment Variables

- `DOTFILES_DIR`: Path to dotfiles repository (default: `~/Developer/ghq/github.com/nekorush14/dotfiles`)

## Author

[nekorush14](https://github.com/nekorush14)

## License

This software is released under the Apache License 2.0, see LICENSE.
