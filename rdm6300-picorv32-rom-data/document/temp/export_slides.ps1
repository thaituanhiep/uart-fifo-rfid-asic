$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$docDir = Split-Path -Parent $scriptDir
$pptxPath = Join-Path $docDir "Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx"
$outFolder = Join-Path $scriptDir "temp_slides"

if (!(Test-Path $outFolder)) {
    New-Item -ItemType Directory -Path $outFolder | Out-Null
}

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptxPath, -1, 0, 0)
$pres.SaveAs($outFolder, 17)
$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

Write-Host "Export completed successfully to $outFolder"
