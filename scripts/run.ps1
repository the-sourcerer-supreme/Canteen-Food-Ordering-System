$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
  throw ".venv not found. Run .\scripts\setup.ps1 first."
}

Write-Host "Starting server at http://127.0.0.1:8000/"
& .\.venv\Scripts\python.exe .\manage.py runserver

