param([string]$portName = "COM3")
$port = New-Object System.IO.Ports.SerialPort $portName, 9600, ([System.IO.Ports.Parity]::None), 8, ([System.IO.Ports.StopBits]::One)
$port.ReadTimeout = 3000
$port.DtrEnable = $true
$port.RtsEnable = $true

try {
    $port.Open()
    Write-Host "Listening on COM3 for 3 seconds..."
    $startTime = [System.DateTime]::Now
    $buffer = ""
    while (([System.DateTime]::Now - $startTime).TotalSeconds -lt 3) {
        $str = $port.ReadExisting()
        if ($str.Length -gt 0) {
            $buffer += $str
        }
        Start-Sleep -Milliseconds 100
    }
    Write-Host "RECEIVED: [$buffer] (Length: $($buffer.Length))"
    $port.Close()
} catch {
    Write-Host "ERROR: " $_.Exception.Message
    if ($port -and $port.IsOpen) { $port.Close() }
}
