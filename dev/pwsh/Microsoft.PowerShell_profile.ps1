# Modules
Import-Module -Name CompletionPredictor

# Environmets
$env:Path+=';C:\Program Files\Git\usr\bin'

# Remove original aliases
Remove-Alias ls
Remove-Alias rm

# Aliases
Set-Alias vim nvim
Set-Alias grep rg
Set-Alias witch gcm
Set-Alias mkdir 'C:\Program Files\Git\usr\bin\mkdir.exe'

# Functions for Aliase
function ls() { eza --icons --git $args}
function la() { eza -a --icons --git $args}
function ll() { eza -aal --icons --git $args}
function lt() { eza -T -L 3 -a -I 'node_modules|.git|.cache' --icons $args}
function ltl() { eza -T -L 3 -al -I 'node_modules|.git|.cache' --icons $args}
function lta() { eza -T -al -I 'node_modules|.git|.cache' --color=always --icons | less -r $args}

# PSReadLine configs
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineKeyHandler -Chord "Ctrl+f" -Function ForwardWord
Set-PSReadLineKeyHandler -Chord "RightArrow" -Function ForwardWord

# Starship Initalization
Invoke-Expression (&starship init powershell)