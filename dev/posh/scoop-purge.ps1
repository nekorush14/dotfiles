# Usage: scoop purge <app> [options]
# Summary: Cleanup apps and caches by removing old versions except for last latest one.
# Help: 'scoop purge' cleans Scoop apps and caches by removing old versions except for last latest one.
# 'scoop purge <app>' cleans up the old versions of that app if said versions exist.
#
# You can use '*' in place of <app> to cleanup all apps and caches.
#
# Options:
#   -s, --skip <int>   Skip count for removing old versions. (default: 1)
#   -g, --global       Cleanup a globally installed app

. "$PSScriptRoot\..\apps\scoop\current\lib\getopt.ps1"
. "$PSScriptRoot\..\apps\scoop\current\lib\manifest.ps1" # 'Select-CurrentVersion' (indirectly)
. "$PSScriptRoot\..\apps\scoop\current\lib\versions.ps1" # 'Select-CurrentVersion'
. "$PSScriptRoot\..\apps\scoop\current\lib\install.ps1" # persist related

$opt, $apps, $err = getopt $args 's:g' @('skip=', 'global')
if ($err) { "scoop purge: $err"; exit 1 }

$global = $opt.g -or $opt.global
$skip = $opt.s + $opt.skip
if (!$skip) { $skip = 1 }
$cache = $true

if (!$apps -and !$all) { 'ERROR: <app> missing'; my_usage; exit 1 }

if ($global -and !(is_admin)) {
    'ERROR: you need admin rights to cleanup global apps'; exit 1
}

# ----------------------------------------------------
# | The following lines are copy-paste code from libexec\scoop-cleanup.ps1.
# ----------------------------------------------------

function purge($app, $global, $verbose, $cache, $skip) { # Change from original code.
    $current_version = Select-CurrentVersion -AppName $app -Global:$global
    # if ($cache) {
    #     Remove-Item "$cachedir\$app#*" -Exclude "$app#$current_version#*"
    # }

    $appDir = appdir $app $global
    $versions = Get-ChildItem $appDir -Name
    $versions = $versions | Where-Object { $current_version -ne $_ -and $_ -ne 'current' }
    
    # -- Change from original code. ---------------------
    $versions = $versions | Select-Object -SkipLast $skip
    $versions | ForEach-Object {
        Remove-Item "$cachedir\$app#$_#*" -Force
    }
    # ---------------------------------------------------
    
    if (!$versions) {
        if ($verbose) { success "$app is already clean" }
        return
    }

    Write-Host -f yellow "Removing $app`:" -NoNewline
    $versions | ForEach-Object {
        $version = $_
        Write-Host " $version" -NoNewline
        $dir = versiondir $app $version $global
        # unlink all potential old link before doing recursive Remove-Item
        unlink_persist_data (installed_manifest $app $version $global) $dir
        Remove-Item $dir -ErrorAction Stop -Recurse -Force
    }

    # $leftVersions = Get-ChildItem $appDir
    # if ($leftVersions.Length -eq 1 -and $leftVersions.Name -eq 'current' -and $leftVersions.LinkType) {
    #     attrib $leftVersions.FullName -R /L
    #     Remove-Item $leftVersions.FullName -ErrorAction Stop -Force
    #     $leftVersions = $null
    # }
    # if (!$leftVersions) {
    #     Remove-Item $appDir -ErrorAction Stop -Force
    # }
    Write-Host ''
}

if ($apps -or $all) {
    if ($apps -eq '*' -or $all) {
        $verbose = $false
        $apps = applist (installed_apps $false) $false
        if ($global) {
            $apps += applist (installed_apps $true) $true
        }
    } else {
        $verbose = $true
        $apps = Confirm-InstallationStatus $apps -Global:$global
    }

    # $apps is now a list of ($app, $global) tuples
    $apps | ForEach-Object { purge @_ $verbose $cache $skip } # Change from original code.

    if ($cache) {
        Remove-Item "$cachedir\*.download" -ErrorAction Ignore
    }

    if (!$verbose) {
        success 'Everything is shiny now!'
    }
}

exit 0
