# Stops the backend, ML service and frontend, and (optionally) the MySQL container.

param(
    [switch]$KeepMySQL
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$runDir = Join-Path $root '.run'

function Stop-Port([int]$port) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    foreach ($c in $conns) {
        try {
            Stop-Process -Id $c.OwningProcess -Force -ErrorAction Stop
            Write-Host "  Stopped process on :$port (PID $($c.OwningProcess))"
        } catch {
            Write-Host "  Could not stop process on :$port" -ForegroundColor Yellow
        }
    }
}

# Stop PID-file processes first (ML / frontend)
foreach ($name in 'backend', 'ml', 'frontend') {
    $pidFile = Join-Path $runDir "$name.pid"
    if (Test-Path $pidFile) {
        $procId = Get-Content $pidFile -ErrorAction SilentlyContinue
        if ($procId) {
            try { Stop-Process -Id $procId -Force -ErrorAction Stop; Write-Host "  Stopped $name (PID $procId)" } catch { }
        }
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    }
}

# Port-based cleanup (covers forked JVM from mvn)
Write-Host '==> Releasing ports'
foreach ($port in 8080, 5000, 5500) { Stop-Port $port }

if (-not $KeepMySQL) {
    Write-Host '==> Stopping MySQL container'
    docker stop staymart-mysql | Out-Null
    Write-Host '  staymart-mysql stopped'
}

Write-Host 'StayMart services stopped.' -ForegroundColor Green
