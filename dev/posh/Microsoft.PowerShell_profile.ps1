
Register-ArgumentCompleter -Native -CommandName dotnet -ScriptBlock {
    param($commandName, $wordToComplete, $cursorPosition)
    dotnet complete --position $cursorPosition "$wordToComplete" | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}

$env:PAGER="less"
$env:EDITOR="nvim"

. $env:USERPROFILE\.config\powershell\user_profile.ps1

oh-my-posh init pwsh --config 'C:\Users\leica\lib\posh-theme.omp.json' | Invoke-Expression

