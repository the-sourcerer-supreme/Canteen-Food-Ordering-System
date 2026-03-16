Param(
  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

function Assert-LastExitCode {
  param([string]$Step)
  if ($LASTEXITCODE -ne 0) {
    throw "$Step failed (exit code $LASTEXITCODE)."
  }
}

if (-not (Test-Path ".\manage.py")) {
  throw "manage.py not found. Run this from the HomeFood-main folder."
}

Write-Host "Creating virtual environment at .\.venv"
& $Python -m venv .venv
Assert-LastExitCode "python -m venv"

Write-Host "Upgrading pip"
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
Assert-LastExitCode "pip upgrade"

Write-Host "Installing requirements"
Write-Host "Writing a pip-safe requirements file for this Python version"
$reqTmp = Join-Path $env:TEMP ("homefood_requirements_" + [guid]::NewGuid().ToString("N") + ".txt")
$reqLines = @(
  "Django>=5.1,<5.3",
  "Pillow>=11.0.0",
  "asgiref>=3.8.1",
  "sqlparse>=0.5.0",
  "tzdata>=2024.1"
)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllBytes($reqTmp, $utf8NoBom.GetBytes(($reqLines -join "`n") + "`n"))
& .\.venv\Scripts\python.exe -m pip install -r $reqTmp
Assert-LastExitCode "pip install -r requirements.txt"

Write-Host "Running Django checks"
& .\.venv\Scripts\python.exe .\manage.py check
Assert-LastExitCode "manage.py check"

Write-Host "Applying migrations"
& .\.venv\Scripts\python.exe .\manage.py migrate
Assert-LastExitCode "manage.py migrate"

Write-Host "Setup complete."

