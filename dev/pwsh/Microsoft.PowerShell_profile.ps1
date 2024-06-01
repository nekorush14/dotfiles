# Modules
Import-Module -Name CompletionPredictor

# Environmets
$env:Path+=';C:\Program Files\Git\usr\bin'
$env:Path+=';C:\Program Files\LLVM\bin'

# Remove original aliases
Remove-Alias ls
Remove-Alias rm

# Aliases
Set-Alias mkdir 'C:\Program Files\Git\usr\bin\mkdir.exe'
Set-Alias cat bat
Set-Alias df duf
Set-Alias du dust
Set-Alias ps procs
Set-Alias top btm
Set-Alias grep rg
Set-Alias vim nvim
Set-Alias which gcm
Set-Alias lg lazygit
Set-Alias ld lazydocker

# Functions for Aliase
function ls() { eza --icons --git $args}
function la() { eza -a --icons --git $args}
function ll() { eza -aal --icons --git $args}
function lt() { eza -T -L 3 -a -I 'node_modules|.git|.cache' --icons $args}
function ltl() { eza -T -L 3 -al -I 'node_modules|.git|.cache' --icons $args}
function lta() { eza -T -al -I 'node_modules|.git|.cache' --color=always --icons | less -r $args}
function open() { Invoke-Item $args}
function history() { cat (Get-PSReadlineOption).HistorySavePath}
# function whereis ($command) {
#     Get-Command -Name $command -ErrorAction SilentlyContinue |
#     Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue
# }

# PSReadLine configs
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -PredictionSource HistoryAndPlugin 
Set-PSReadLineOption -EditMode Emacs
Set-PSReadLineOption -BellStyle None
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
Set-PSReadLineKeyHandler -Key Ctrl+d -Function DeleteChar
Set-PSReadLineKeyHandler -Chord "Ctrl+f" -Function ForwardWord
Set-PSReadLineKeyHandler -Chord "RightArrow" -Function ForwardWord
Set-PSReadlineOption -AddToHistoryHandler {
    param ($command)
    switch -regex ($command) {
        "SKIPHISTORY" {return $false}
        "^[a-z]$" {return $false}
        "exit" {return $false}
    }
    return $true
}
Set-PSReadLineOption -WordDelimiters ";:,.[]{}()/\|^&*-=+'`" !?@#$%&_<>「」（）『』『』［］、，。：；／"

# Completions
# Winget
Register-ArgumentCompleter -Native -CommandName winget -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
        [Console]::InputEncoding = [Console]::OutputEncoding = $OutputEncoding = [System.Text.Utf8Encoding]::new()
        $Local:word = $wordToComplete.Replace('"', '""')
        $Local:ast = $commandAst.ToString().Replace('"', '""')
        winget complete --word="$Local:word" --commandline "$Local:ast" --position $cursorPosition | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
}
# PowerShell parameter completion shim for the dotnet CLI
Register-ArgumentCompleter -Native -CommandName dotnet -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
        dotnet complete --position $cursorPosition "$commandAst" | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
}


# Starship Initalization
Invoke-Expression (&starship init powershell)   

#f45873b3-b655-43a6-b217-97c00aa0db58 PowerToys CommandNotFound module

Import-Module -Name Microsoft.WinGet.CommandNotFound
#f45873b3-b655-43a6-b217-97c00aa0db58


# ---------------- inshellisense shell plugin ----------------
$__IsCommandFlag = ([Environment]::GetCommandLineArgs() | ForEach-Object { $_.contains("-Command") }) -contains $true
$__IsNoExitFlag = ([Environment]::GetCommandLineArgs() | ForEach-Object { $_.contains("-NoExit") }) -contains $true
$__IsInteractive = -not $__IsCommandFlag -or ($__IsCommandFlag -and $__IsNoExitFlag)
if ([string]::IsNullOrEmpty($env:ISTERM) -and [Environment]::UserInteractive -and $__IsInteractive) {
  is -s pwsh
  Stop-Process -Id $pid
}
