# Requires: pwsh
# Starts MySQL (Docker), backend (:8080), ML service (:5000) and frontend (:5500).

param(
    [switch]$SkipMySQL
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$runDir = Join-Path $root '.run'
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

function Test-Port([int]$port) {
    try {
        return [bool](Test-NetConnection -ComputerName 'localhost' -Port $port -WarningAction SilentlyContinue).TcpTestSucceeded
    } catch {
        return $false
    }
}

function Wait-Port([int]$port, [int]$timeoutSec, [string]$label) {
    $deadline = (Get-Date).AddSeconds($timeoutSec)
    while ((Get-Date) -lt $deadline) {
        if (Test-Port $port) { return $true }
        Start-Sleep -Seconds 2
    }
    Write-Host "  ! $label did not open :$port within ${timeoutSec}s (check the .run logs)" -ForegroundColor Yellow
    return $false
}

Write-Host '==> MySQL (Docker container: staymart-mysql)'
if (-not $SkipMySQL) {
    docker info *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host '  ! Docker daemon is not running. Start Docker Desktop, then re-run this script.' -ForegroundColor Red
        exit 1
    }
    $exists = docker ps -a --format '{{.Names}}' | Where-Object { $_ -eq 'staymart-mysql' }
    if (-not $exists) {
        docker run --name staymart-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=staymart `
            -p 3306:3306 --restart unless-stopped -d mysql:8.0 | Out-Null
        Write-Host '  Created and started staymart-mysql'
    } else {
        docker start staymart-mysql | Out-Null
        Write-Host '  Started existing staymart-mysql'
    }
    Write-Host '  Waiting for MySQL to accept connections...'
    $deadline = (Get-Date).AddSeconds(90)
    while ((Get-Date) -lt $deadline) {
        docker exec staymart-mysql mysql -uroot -proot -e "SELECT 1" *> $null
        if ($LASTEXITCODE -eq 0) { Write-Host '  MySQL ready'; break }
        Start-Sleep -Seconds 3
    }
} else {
    Write-Host '  (skipped)'
}

Write-Host '==> JDK 21'
$jdk = Get-ChildItem 'C:\Program Files\Eclipse Adoptium' -Directory -Filter 'jdk-21*' -ErrorAction SilentlyContinue |
    Select-Object -First 1
if ($jdk) {
    $env:JAVA_HOME = $jdk.FullName
    $env:Path = "$($jdk.FullName)\bin;$env:Path"
    Write-Host "  JAVA_HOME=$env:JAVA_HOME"
} else {
    Write-Host '  ! Temurin JDK 21 not found; falling back to system java' -ForegroundColor Yellow
}

Write-Host '==> Backend (:8080)'
if (Test-Port 8080) {
    Write-Host '  Already running'
} else {
    Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', 'mvn spring-boot:run' -WorkingDirectory $root `
        -RedirectStandardOutput (Join-Path $runDir 'backend.out.log') `
        -RedirectStandardError  (Join-Path $runDir 'backend.err.log') -WindowStyle Hidden | Out-Null
    Write-Host '  Started (logs: .run/backend.out.log)'
    Wait-Port 8080 180 'Backend' | Out-Null
}

Write-Host '==> ML service (:5000)'
if (Test-Port 5000) {
    Write-Host '  Already running'
} else {
    $venvPython = Join-Path $root 'ml-service\.venv\Scripts\python.exe'
    if (Test-Path $venvPython) {
        Start-Process -FilePath $venvPython -ArgumentList 'app.py' -WorkingDirectory (Join-Path $root 'ml-service') `
            -RedirectStandardOutput (Join-Path $runDir 'ml.out.log') `
            -RedirectStandardError  (Join-Path $runDir 'ml.err.log') -WindowStyle Hidden | Out-Null
        Write-Host '  Started (logs: .run/ml.out.log)'
        Wait-Port 5000 60 'ML service' | Out-Null
    } else {
        Write-Host '  ! venv python not found; run: python -m venv ml-service/.venv' -ForegroundColor Yellow
    }
}

Write-Host '==> Frontend (:5500)'
if (Test-Port 5500) {
    Write-Host '  Already running'
} else {
    Start-Process -FilePath 'python' -ArgumentList '-m', 'http.server', '5500' -WorkingDirectory (Join-Path $root 'frontend') `
        -RedirectStandardOutput (Join-Path $runDir 'frontend.out.log') `
        -RedirectStandardError  (Join-Path $runDir 'frontend.err.log') -WindowStyle Hidden | Out-Null
    Write-Host '  Started (logs: .run/frontend.out.log)'
    Wait-Port 5500 20 'Frontend' | Out-Null
}

Write-Host ''
Write-Host 'StayMart startup complete:' -ForegroundColor Green
Write-Host '  Frontend : http://localhost:5500'
Write-Host '  API      : http://localhost:8080/api'
Write-Host '  Swagger  : http://localhost:8080/swagger-ui.html'
Write-Host '  ML       : http://localhost:5000/health'
Write-Host '  Admin    : admin@staymart.com / Admin@123'
