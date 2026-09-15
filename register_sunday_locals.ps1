# Registers a Windows Scheduled Task that stamps Phoenix FOX 10 / CBS 5
# locals every Sunday at 06:15 and pushes if the slate changed.
#
# Listings page only (TV Passport). Not DirecTV. Ticket numbers stay human.
#
# Install ONCE (no admin needed):
#     powershell -ExecutionPolicy Bypass -File .\register_sunday_locals.ps1
# Remove with:
#     Unregister-ScheduledTask -TaskName "Bar Guide Sunday Locals" -Confirm:$false

$ErrorActionPreference = "Stop"

$TaskName = "Bar Guide Sunday Locals"
$RepoDir  = $PSScriptRoot
$LogDir   = Join-Path $RepoDir "logs"
$LogFile  = Join-Path $LogDir "sunday_locals.log"
$Runner   = Join-Path $RepoDir "sunday_run.ps1"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

$python = $null
$cmd = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($cmd -and (Test-Path -LiteralPath $cmd)) { $python = $cmd }
if (-not $python) {
    foreach ($ver in @("Python312", "Python313", "Python311", "Python310")) {
        $guess = Join-Path $env:LOCALAPPDATA "Programs\Python\$ver\python.exe"
        if (Test-Path -LiteralPath $guess) { $python = $guess; break }
    }
}
if (-not $python) { throw "python not found. Install Python or add it to PATH, then re-run this script." }

Write-Host "Repo : $RepoDir"
Write-Host "Log  : $LogFile"
Write-Host "Py   : $python"

$inner = "Set-Location '$RepoDir'; " +
         "`$env:PYTHONUTF8='1'; `$env:PYTHONIOENCODING='utf-8'; " +
         "`$env:BAR_GUIDE_PYTHON='$python'; " +
         "Add-Content -Path '$LogFile' -Value ('==== ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ' ===='); " +
         "& '$Runner' *>> '$LogFile'"
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($inner))

$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -EncodedCommand $encoded"

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "06:15"

$settings = New-ScheduledTaskSettingsSet `
    -WakeToRun `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15) `
    -MultipleInstances IgnoreNew

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Removed existing task '$TaskName' to re-register."
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal `
    -Description "Sunday FOX 10 / CBS 5 local stamps + git push. See sunday_run.ps1." | Out-Null

Write-Host ""
Write-Host "Installed '$TaskName' Sundays at 06:15 local."
Write-Host "Test it now with:  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "Then check:        Get-Content '$LogFile' -Tail 20"
