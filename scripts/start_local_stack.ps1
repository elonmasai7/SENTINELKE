$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$runtime = Join-Path $root '.runtime'
New-Item -ItemType Directory -Path $runtime -Force | Out-Null

$djangoOut = Join-Path $runtime 'django.out.log'
$djangoErr = Join-Path $runtime 'django.err.log'
$mlOut = Join-Path $runtime 'ml.out.log'
$mlErr = Join-Path $runtime 'ml.err.log'

$djangoCmd = "cd /d `"$root`" && python backend/manage.py runserver 127.0.0.1:8010 --settings=sentinelke.settings_local"
$mlCmd = "cd /d `"$($root)\ml_services`" && python -m uvicorn main:app --host 127.0.0.1 --port 9000"

$django = Start-Process -FilePath cmd.exe -ArgumentList @('/c', $djangoCmd) -PassThru -RedirectStandardOutput $djangoOut -RedirectStandardError $djangoErr
$ml = Start-Process -FilePath cmd.exe -ArgumentList @('/c', $mlCmd) -PassThru -RedirectStandardOutput $mlOut -RedirectStandardError $mlErr

Set-Content -Path (Join-Path $runtime 'django.pid') -Value $django.Id
Set-Content -Path (Join-Path $runtime 'ml.pid') -Value $ml.Id

Write-Output "Django PID: $($django.Id)"
Write-Output "ML PID: $($ml.Id)"
Write-Output 'Django URL: http://127.0.0.1:8010'
Write-Output 'ML URL: http://127.0.0.1:9000/health'
