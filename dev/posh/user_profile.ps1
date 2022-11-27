# Remove Aliases
Remove-Item alias:ls
Remove-Item alias:cat
Remove-Item alias:pwd
Remove-Item alias:ps

# Alias
Set-Alias vim nvim
Set-Alias tig 'C:\Program Files\Git\usr\bin\tig.exe'
Set-Alias which gcm
Set-Alias pbcopy Set-Clipboard

# Alias from scoop package
Set-Alias sudo gsudo
Set-Alias lg lazygit

# Replace common UNIX commands to modern tui commands.
Set-Alias cat bat
Set-Alias df duf
Set-Alias du dust
Set-Alias ps procs
Set-Alias top btm
Set-Alias grep rg

# Functions - Custom functions
function ll() { lsd -l --blocks permission --blocks size --blocks date --blocks name $args}
function tree() { lsd --tree $args}
function ls() { lsd $args}
function open() { Invoke-Item $args}
function history() { cat (Get-PSReadlineOption).HistorySavePath}
function hgrep() { hgrep --theme Material-Theme --background $args}
function psFzf {
    $origin = [System.Console]::OutputEncoding
    $utf8 = [System.Text.Encoding]::GetEncoding("utf-8")
    $OutputEncoding = $utf8
    [System.Console]::OutputEncoding = $utf8
    $out = ($input | fzf $env:FZF_CTRL_T_OPTS)
    [System.Console]::OutputEncoding = $origin
    return $out
}

# Functions - using uutils for coreutils coomands on posh
@"
  arch, base32, base64, basename, cat, cksum, comm, cp, cut, date, df, dircolors, dirname,
  echo, env, expand, expr, factor, false, fmt, fold, hashsum, head, hostname, join, link, ln,
  ls, md5sum, mkdir, mktemp, more, mv, nl, nproc, od, paste, printenv, printf, ptx, pwd,
  readlink, realpath, relpath, rm, rmdir, seq, sha1sum, sha224sum, sha256sum, sha3-224sum,
  sha3-256sum, sha3-384sum, sha3-512sum, sha384sum, sha3sum, sha512sum, shake128sum,
  shake256sum, shred, shuf, sleep, sort, split, sum, sync, tac, tail, tee, test, touch, tr,
  true, truncate, tsort, unexpand, uniq, wc, whoami, yes
"@ -split ',' |
ForEach-Object { $_.trim() } |
Where-Object { ! @('tee', 'sort', 'sleep', 'cat', 'df', 'ls').Contains($_) } |
ForEach-Object {
    $cmd = $_
    if (Test-Path Alias:$cmd) { Remove-Item -Path Alias:$cmd }
    $fn = '$input | uutils ' + $cmd + ' $args'
    Invoke-Expression "function global:$cmd { $fn }" 
}

# Import posh modules
Import-Module posh-git
Import-Module "$($(Get-Item $(Get-Command scoop.ps1).Path).Directory.Parent.FullName)\modules\scoop-completion"
Import-Module DockerCompletion
Import-Module PSReadLine
Import-Module PSFzf

# PSReadine Configs
Set-PSReadLineOption -PredictionSource HistoryAndPlugin 
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -EditMode Emacs
Set-PSReadLineOption -BellStyle None
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
Set-PSReadLineKeyHandler -Key Ctrl+d -Function DeleteChar
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

# PSFzf Config
Remove-PSReadlineKeyHandler 'Ctrl+r'
Remove-PSReadlineKeyHandler 'Ctrl+t'

# replace 'Ctrl+t' and 'Ctrl+r' with your preferred bindings:
Set-PsFzfOption -PSReadlineChordProvider 'Ctrl+t' -PSReadlineChordReverseHistory 'Ctrl+r'
