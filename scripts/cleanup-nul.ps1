# nul 파일 정리 스크립트 (PowerShell)
# 사용법: powershell -ExecutionPolicy Bypass -File scripts\cleanup-nul.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🧹 Cleaning up nul files" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 프로젝트 루트로 이동
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptPath\.."

# nul 파일 찾기
Write-Host "Searching for nul files..." -ForegroundColor Yellow
$nulFiles = Get-ChildItem -Path . -Filter "nul" -Recurse -File -ErrorAction SilentlyContinue

if ($nulFiles.Count -eq 0) {
    Write-Host "✅ No nul files found!" -ForegroundColor Green
    exit 0
}

Write-Host "Found $($nulFiles.Count) nul file(s):" -ForegroundColor Yellow
foreach ($file in $nulFiles) {
    Write-Host "  - $($file.FullName)" -ForegroundColor Gray
}
Write-Host ""

# 삭제 확인
$response = Read-Host "Delete these files? (y/N)"

if ($response -match '^[Yy]$') {
    foreach ($file in $nulFiles) {
        Remove-Item $file.FullName -Force
        Write-Host "  Deleted: $($file.FullName)" -ForegroundColor Green
    }
    Write-Host "✅ Deleted all nul files" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Cancelled" -ForegroundColor Yellow
}

Write-Host "==========================================" -ForegroundColor Cyan
