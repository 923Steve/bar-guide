# Registers a Windows Scheduled Task that pulls the bar-guide slate every
# Friday morning and pushes it to GitHub Pages.
#
# Same rules as MLB Morning Catchup / WNBA:
# - Stay LOGGED IN (lock/sleep is fine via WakeToRun; do not sign out / shut down).
# - Git uses the credentials already on this PC.
#
# Install ONCE (no admin needed):
#     powershell -ExecutionPolicy Bypass -File .\register_friday_pull.ps1
# Remove with:
#     Unregister-ScheduledTask -TaskName "Bar Guide Friday Pull" -Confirm:$false

$ErrorActionPreference = "Stop"

$TaskName = "Bar Guide Friday Pull"
$RepoDir  = $PSScriptRoot
$LogDir   = Join-Path $RepoDir "logs"
$LogFile  = Join-Path $LogDir "friday_pull.log"
$Runner   = Join-Path $RepoDir "friday_run.ps1"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

Write-Host "Repo : $RepoDir"
Write-Host "Log  : $LogFile"

$inner = "Set-Location '$RepoDir'; " +
         "`$env:PYTHONUTF8='1'; `$env:PYTHONIOENCODING='utf-8'; " +
         "Add-Content -Path '$LogFile' -Value ('==== ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ' ===='); " +
         "& '$Runner' *>> '$LogFile'"
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($inner))

$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -EncodedCommand $encoded"

# After MLB 06:00 so they don't stomp each other. Missed Friday (travel/sleep)
# re-fires when the PC is next up.
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At "06:15"

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
    Write-Host "Removed existing task to re-register."
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal `
    -Description "Friday ESPN slate pull + git push for Bar Guide (GitHub Pages). See friday_run.ps1." | Out-Null

Write-Host ""
Write-Host "Installed '$TaskName' Fridays at 06:15 local."
Write-Host "Test it now with:  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "Then check:        Get-Content '$LogFile' -Tail 20"
