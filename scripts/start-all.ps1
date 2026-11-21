# Requires: pwsh
# Starts MySQL (Docker), backend (:8080), ML service (:5000) and frontend (:5500).

param(
    [switch]$SkipMySQL,
    [switch]$Restart
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$runDir = Join-Path $root '.run'
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

function Stop-PortProcess([int]$port) {
    try {
        $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
        foreach ($c in $conns) {
            $p = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue
            if ($p) {
                Write-Host "  Stopping existing process on port $port (PID $($p.Id): $($p.ProcessName))..."
                Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
            }
        }
    } catch { }
}

function Test-Port([int]$port) {
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $async = $client.BeginConnect('127.0.0.1', $port, $null, $null)
        $connected = $async.AsyncWaitHandle.WaitOne(700, $false)
        if ($connected -and $client.Connected) { $client.Close(); return $true }
        $client.Close()
        return $false
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

function Invoke-Http([string]$url, [int]$timeoutSec = 3) {
    try {
        return Invoke-WebRequest -Uri $url -TimeoutSec $timeoutSec -UseBasicParsing
    } catch {
        return $null
    }
}

function Show-LogTail([string]$log, [int]$lines = 25) {
    if (Test-Path $log) {
        Write-Host ('  --- ' + (Split-Path -Leaf $log) + ' (tail) ---') -ForegroundColor DarkGray
        Get-Content $log -Tail $lines | ForEach-Object { Write-Host "  $_" -ForegroundColor DarkGray }
    }
}

function Remove-PortConflict([int]$port) {
    $running = docker ps --format '{{.Names}}' 2>$null | Where-Object { $_ }
    foreach ($name in $running) {
        if ($name -eq 'staymart-mysql') { continue }
        $published = (docker port $name 2>$null | Out-String)
        if ($published -match ":$port->") {
            Write-Host "  ! container '$name' also publishes host port $port - stopping it (StayMart needs it)" -ForegroundColor Yellow
            docker stop $name | Out-Null
        }
    }
}

Write-Host '==> MySQL (Docker container: staymart-mysql)'
if (-not $SkipMySQL) {
    docker info *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host '  ! Docker daemon is not running. Start Docker Desktop, then re-run this script.' -ForegroundColor Red
        exit 1
    }

    # Another container squatting on 3306 makes the backend silently connect to the
    # wrong (empty) database, which fails schema validation on startup.
    Remove-PortConflict 3306

    $exists = docker ps -a --format '{{.Names}}' | Where-Object { $_ -eq 'staymart-mysql' }
    if (-not $exists) {
        docker run --name staymart-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=staymart `
            -p 3306:3306 --restart unless-stopped -d mysql:8.0 | Out-Null
        Write-Host '  Created and started staymart-mysql'
    } else {
        docker start staymart-mysql | Out-Null
        Write-Host '  Started existing staymart-mysql'
    }

    Write-Host '  Waiting for host port 3306...'
    if (-not (Wait-Port 3306 90 'MySQL host port')) {
        # Container runs but is not publishing on the host: recreate it, keeping the data volume.
        $volume = docker inspect staymart-mysql --format '{{range .Mounts}}{{if eq .Destination "/var/lib/mysql"}}{{.Name}}{{end}}{{end}}' 2>$null
        Write-Host '  ! staymart-mysql is not publishing host port 3306 - recreating container (data volume kept)' -ForegroundColor Yellow
        docker stop staymart-mysql | Out-Null
        docker rm staymart-mysql | Out-Null
        $runArgs = @('--name', 'staymart-mysql', '-e', 'MYSQL_ROOT_PASSWORD=root', '-e', 'MYSQL_DATABASE=staymart',
                     '-p', '3306:3306', '--restart', 'unless-stopped')
        if ($volume) { $runArgs += @('-v', "${volume}:/var/lib/mysql") }
        $runArgs += @('-d', 'mysql:8.0')
        docker run @runArgs | Out-Null
        Wait-Port 3306 90 'MySQL host port' | Out-Null
    }

    Write-Host '  Waiting for MySQL to accept connections...'
    $deadline = (Get-Date).AddSeconds(90)
    $mysqlReady = $false
    while ((Get-Date) -lt $deadline) {
        docker exec staymart-mysql mysql -uroot -proot -e "SELECT 1" *> $null
        if ($LASTEXITCODE -eq 0) { $mysqlReady = $true; Write-Host '  MySQL ready'; break }
        Start-Sleep -Seconds 3
    }
    if (-not $mysqlReady) {
        Write-Host '  ! MySQL did not become ready - aborting (see: docker logs staymart-mysql)' -ForegroundColor Red
        exit 1
    }

    # Schema check: ddl-auto=validate means an empty database kills the backend on boot.
    $tableCount = (docker exec staymart-mysql mysql -uroot -proot -N -B `
        -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='staymart';" 2>$null | Out-String).Trim()
    if (-not $tableCount -or [int]$tableCount -eq 0) {
        Write-Host '  Schema missing - loading database/*.sql ...' -ForegroundColor Yellow
        foreach ($file in '01_schema.sql', '02_seed.sql', '03_seed_listings.sql') {
            $path = Join-Path $root "database/$file"
            if (-not (Test-Path $path)) {
                Write-Host "  ! database/$file not found - skipped" -ForegroundColor Yellow
                continue
            }
            Get-Content -Raw -Path $path | docker exec -i staymart-mysql mysql -uroot -proot *> $null
            if ($LASTEXITCODE -ne 0) {
                Write-Host "  ! Loading database/$file failed" -ForegroundColor Red
                exit 1
            }
            Write-Host "  Loaded $file"
        }
        $tableCount = (docker exec staymart-mysql mysql -uroot -proot -N -B `
            -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='staymart';" 2>$null | Out-String).Trim()
    }
    if (-not $tableCount -or [int]$tableCount -eq 0) {
        Write-Host '  ! staymart schema is still empty - aborting' -ForegroundColor Red
        exit 1
    }
    Write-Host "  Schema OK ($tableCount tables)"
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

if (-not (Get-Command mvn -ErrorAction SilentlyContinue)) {
    $maven = Get-ChildItem 'C:\Users\divya\apache-maven' -Directory -Filter 'apache-maven*' -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($maven) {
        $env:Path = "$($maven.FullName)\bin;$env:Path"
        Write-Host "  MAVEN_HOME=$($maven.FullName)"
    }
}

Write-Host '==> Backend (:8080)'
if ($Restart) { Stop-PortProcess 8080; Start-Sleep -Seconds 1 }
$backendLog = Join-Path $runDir 'backend.out.log'
if (Test-Port 8080) {
    Write-Host '  Already running'
} else {
    Remove-Item $backendLog -Force -ErrorAction SilentlyContinue
    $proc = Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', 'mvn spring-boot:run' -WorkingDirectory $root `
        -RedirectStandardOutput $backendLog `
        -RedirectStandardError (Join-Path $runDir 'backend.err.log') -WindowStyle Hidden -PassThru
    Set-Content -Path (Join-Path $runDir 'backend.pid') -Value $proc.Id
    Write-Host '  Started (logs: .run/backend.out.log)'
    Wait-Port 8080 180 'Backend' | Out-Null
    Start-Sleep -Seconds 2
    if (-not (Test-Port 8080)) {
        Write-Host '  ! Backend failed to start. Last log lines:' -ForegroundColor Red
        Show-LogTail $backendLog
        exit 1
    }
    if (Select-String -Path $backendLog -Pattern 'BUILD FAILURE' -Quiet -ErrorAction SilentlyContinue) {
        Write-Host '  ! Maven reported BUILD FAILURE. Last log lines:' -ForegroundColor Red
        Show-LogTail $backendLog
        exit 1
    }
    if (-not (Select-String -Path $backendLog -Pattern 'Started StayMartApplication' -Quiet -ErrorAction SilentlyContinue)) {
        Write-Host '  ! Backend port is open but startup was not confirmed; check .run/backend.out.log' -ForegroundColor Yellow
    } else {
        Write-Host '  Backend started OK'
    }
}

Write-Host '==> ML service (:5000)'
if ($Restart) { Stop-PortProcess 5000; Start-Sleep -Seconds 1 }
if (Test-Port 5000) {
    Write-Host '  Already running'
} else {
    $venvPython = Join-Path $root 'ml-service\.venv\Scripts\python.exe'
    if (Test-Path $venvPython) {
        Remove-Item (Join-Path $runDir 'ml.out.log') -Force -ErrorAction SilentlyContinue
        $proc = Start-Process -FilePath $venvPython -ArgumentList 'app.py' -WorkingDirectory (Join-Path $root 'ml-service') `
            -RedirectStandardOutput (Join-Path $runDir 'ml.out.log') `
            -RedirectStandardError (Join-Path $runDir 'ml.err.log') -WindowStyle Hidden -PassThru
        Set-Content -Path (Join-Path $runDir 'ml.pid') -Value $proc.Id
        Write-Host '  Started (logs: .run/ml.out.log)'
        if (-not (Wait-Port 5000 60 'ML service')) {
            Show-LogTail (Join-Path $runDir 'ml.err.log')
            exit 1
        }
    } else {
        Write-Host '  ! venv python not found; run: python -m venv ml-service/.venv' -ForegroundColor Yellow
    }
}

if (Test-Port 5000) {
    $mlDeadline = (Get-Date).AddSeconds(90)
    while ((Get-Date) -lt $mlDeadline) {
        $health = Invoke-Http 'http://localhost:5000/health' 5
        if ($health) {
            try {
                $payload = $health.Content | ConvertFrom-Json
                if ($payload.models_loaded) { Write-Host '  ML models loaded'; break }
            } catch { }
        }
        Start-Sleep -Seconds 5
    }
    $health = Invoke-Http 'http://localhost:5000/health' 5
    if ($health) {
        $payload = $health.Content | ConvertFrom-Json
        if (-not $payload.models_loaded) {
            Write-Host '  ! ML models still not loaded - check .run/ml.err.log and the MySQL connection' -ForegroundColor Yellow
        }
    } else {
        Write-Host '  ! ML service health check failed' -ForegroundColor Yellow
    }
}

Write-Host '==> Frontend (:5500)'
if ($Restart) { Stop-PortProcess 5500; Start-Sleep -Seconds 1 }
if (Test-Port 5500) {
    Write-Host '  Already running'
} else {
    $serveScript = Join-Path $root 'scripts\serve_frontend.py'
    $proc = Start-Process -FilePath 'python' -ArgumentList $serveScript, '5500' -WorkingDirectory $root `
        -RedirectStandardOutput (Join-Path $runDir 'frontend.out.log') `
        -RedirectStandardError (Join-Path $runDir 'frontend.err.log') -WindowStyle Hidden -PassThru
    Set-Content -Path (Join-Path $runDir 'frontend.pid') -Value $proc.Id
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
