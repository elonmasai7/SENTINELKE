$root = Split-Path -Parent $PSScriptRoot
$runtime = Join-Path $root '.runtime'
$pidFiles = @('django.pid', 'ml.pid')

foreach ($file in $pidFiles) {
  $path = Join-Path $runtime $file
  if (Test-Path $path) {
    $procId = Get-Content $path | Select-Object -First 1
    if ($procId) {
      try {
        cmd /c "taskkill /PID $procId /T /F" | Out-Null
        Write-Output "Stopped process tree rooted at PID $procId ($file)"
      } catch {
        Write-Output "PID $procId not running ($file)"
      }
    }
    Remove-Item $path -Force
  }
}
