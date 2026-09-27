param([string]$portName = "COM3")

$port = New-Object System.IO.Ports.SerialPort $portName, 9600, ([System.IO.Ports.Parity]::None), 8, ([System.IO.Ports.StopBits]::One)
$port.ReadTimeout = 1000
$port.WriteTimeout = 1000
$port.DtrEnable = $true
$port.RtsEnable = $true

try {
    $port.Open()
    $port.DiscardInBuffer()
    $port.Write("P`n")
    Start-Sleep -Milliseconds 300
    $resp = $port.ReadExisting()
    Write-Host "RESPONSE: [$resp]"
    $port.Close()
} catch {
    Write-Host "ERROR: " $_.Exception.Message
    if ($port -and $port.IsOpen) { $port.Close() }
}
