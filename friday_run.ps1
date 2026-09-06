# Unattended slate pull + push. Called by the Tue/Fri scheduled task.
$ErrorActionPreference = "Stop"
$RepoDir = $PSScriptRoot
Set-Location $RepoDir

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:GIT_TERMINAL_PROMPT = "0"

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { $python = (Get-Command python3 -ErrorAction SilentlyContinue).Source }
if (-not $python) { throw "python not on PATH" }

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
