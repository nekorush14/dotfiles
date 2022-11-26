# Load user plofile
. $env:USERPROFILE\.config\powershell\user_profile.ps1

# Completion configs
# For .Net
Register-ArgumentCompleter -Native -CommandName dotnet -ScriptBlock {
    param($commandName, $wordToComplete, $cursorPosition)
    dotnet complete --position $cursorPosition "$wordToComplete" | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}

# Set Environment variables
# $env:PAGER="less"
$env:EDITOR="nvim"
$env:Path+=";C:\Users\leica\AppData\Roaming\Python\Python39\Scripts"
$env:Path+=";C:\Users\leica\bin"

# FZF configs
$env:FZF_DEFAULT_COMMAND='fd -H -t f --color=always'
$env:FZF_DEFAULT_OPTS='--no-height --color=bg+:#343d46,gutter:-1,pointer:#ff3c3c,info:#0dbc79,hl:#0dbc79,hl+:#23d18b'

$env:FZF_CTRL_T_COMMAND='fd -H -L -E .git -t f'
$env:FZF_CTRL_T_OPTS="--preview 'bat --color=always --line-range :50 {}'"

$env:FZF_ALT_C_COMMAND='fd -H -L -E .git -t d'
$env:FZF_ALT_C_OPTS="--preview 'tree -C {} | head -50'"

# Set Prompt
oh-my-posh init pwsh --config 'C:\Users\leica\lib\posh-theme.omp.json' | Invoke-Expression

