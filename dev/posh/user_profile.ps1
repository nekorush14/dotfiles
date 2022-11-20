# Remove Aliases
Remove-Item alias:cp
Remove-Item alias:mv
Remove-Item alias:rm
Remove-Item alias:ls
Remove-Item alias:cat
Remove-Item alias:pwd
Remove-Item alias:sort -Force

# Alias
Set-Alias vim nvim
Set-Alias tig 'C:\Program Files\Git\usr\bin\tig.exe'
Set-Alias which gcm

# Alias from scoop package
Set-Alias sudo gsudo

# Replace common UNIX commands to modern tui commands.
Set-Alias cat bat
Set-Alias df duf
Set-Alias du dust
Set-Alias top ntop
Set-Alias grep rg

# Functions - Custom functions
function ll() { lsd -l --blocks permission --blocks size --blocks date --blocks name $args}
function tree() { lsd --tree $args}
function ls() { lsd $args}
function open() { Invoke-Item $args}
function history() { cat (Get-PSReadlineOption).HistorySavePath}

# Functions - using uutils for coreutils coomands on posh
function cp() { uutils cp $args}
function mv() { uutils mv $args}
function rm() { uutils rm $args}
function mkdir() { uutils mkdir $args}
function printenv() { uutils printenv $args}
function ln() { uutils ln $args}
# function cat() { $input | uutils cat $args}
function head() { $input | uutils head $args}
function tail() { $input | uutils tail $args}
function wc() { $input | uutils wc $args}
function tr() { $input | uutils tr $args}
function pwd() { $input | uutils pwd $args}
function cut() { $input | uutils cut $args}
function uniq() { $input | uutils uniq $args}
function sort() { $input | uutils sort $args}

# Import posh modules
Import-Module posh-git
Import-Module "$($(Get-Item $(Get-Command scoop.ps1).Path).Directory.Parent.FullName)\modules\scoop-completion"
Import-Module DockerCompletion

# PSReadine Configs
Set-PSReadLineOption -PredictionSource HistoryAndPlugin 
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
Set-PSReadLineOption -BellStyle None

