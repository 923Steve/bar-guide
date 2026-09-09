# Unattended slate pull + push. Called by the Tue/Fri scheduled task.
$ErrorActionPreference = "Stop"
$RepoDir = $PSScriptRoot
Set-Location $RepoDir

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:GIT_TERMINAL_PROMPT = "0"

function Resolve-Python {
    if ($env:BAR_GUIDE_PYTHON -and (Test-Path -LiteralPath $env:BAR_GUIDE_PYTHON)) {
        return $env:BAR_GUIDE_PYTHON
    }
    $cmd = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($cmd -and (Test-Path -LiteralPath $cmd)) { return $cmd }
    $cmd = (Get-Command python3 -ErrorAction SilentlyContinue).Source
    if ($cmd -and (Test-Path -LiteralPath $cmd)) { return $cmd }
    foreach ($ver in @("Python312", "Python313", "Python311", "Python310")) {
        $guess = Join-Path $env:LOCALAPPDATA "Programs\Python\$ver\python.exe"
        if (Test-Path -LiteralPath $guess) { return $guess }
    }
    throw "python not found (scheduled tasks do not get the user PATH)"
}

try {
    $python = Resolve-Python
    Write-Host "Python: $python"
    Write-Host "Pulling slate..."
    & $python pull_week.py
    if ($LASTEXITCODE -ne 0) { throw "pull_week.py failed ($LASTEXITCODE)" }

    git add src/data/slate.json
    $changed = @(git diff --cached --name-only)
    if (-not $changed) {
        Write-Host "Slate unchanged — no push."
        exit 0
    }

    git commit -m "Slate pull"
    if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
    git push
    if ($LASTEXITCODE -ne 0) { throw "git push failed" }
    Write-Host "Pushed. Phone updates in about a minute."
} catch {
    Write-Host "SLATE PULL FAILED: $($_.Exception.Message)"
    throw
}
