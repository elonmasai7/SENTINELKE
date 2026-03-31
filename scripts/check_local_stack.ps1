try {
  $django = Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8010/ -TimeoutSec 5
  Write-Output "Django: $($django.StatusCode)"
} catch {
  if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
    Write-Output "Django: $([int]$_.Exception.Response.StatusCode)"
  } else {
    Write-Output 'Django: down'
  }
}

try {
  $ml = Invoke-WebRequest -UseBasicParsing http://127.0.0.1:9000/health -TimeoutSec 5
  Write-Output "ML: $($ml.StatusCode)"
} catch {
  Write-Output 'ML: down'
}
