$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
$pptxPath = "C:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx"
$outFolder = "C:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp_slides"

if (!(Test-Path $outFolder)) {
    New-Item -ItemType Directory -Path $outFolder | Out-Null
}

$pres = $ppt.Presentations.Open($pptxPath)
$pres.SaveAs($outFolder, 17)
$pres.Close()
$ppt.Quit()
Write-Host "Export completed successfully"
