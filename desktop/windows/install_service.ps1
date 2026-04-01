param(
  [string]$NssmPath = 'nssm.exe'
)

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$launcher = Join-Path $PSScriptRoot 'launcher.py'
$serviceName = 'SentinelKE Service'
$python = (Get-Command python).Source

if (-not (Test-Path $NssmPath)) {
  Write-Error "nssm was not found at $NssmPath"
  exit 1
}

& $NssmPath install $serviceName $python "$launcher --service --env-file $root\.env.desktop"
& $NssmPath set $serviceName AppDirectory $root
& $NssmPath set $serviceName Start SERVICE_AUTO_START
& $NssmPath set $serviceName DisplayName $serviceName
& $NssmPath start $serviceName
