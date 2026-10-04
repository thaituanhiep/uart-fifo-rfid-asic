$ppt = New-Object -ComObject PowerPoint.Application
$pptxPath = "D:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx"
$pres = $ppt.Presentations.Open($pptxPath, -1, 0, 0)
$pres.Slides.Item(11).Export("D:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_11.png", "PNG", 1920, 1080)
$pres.Slides.Item(12).Export("D:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_12.png", "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Host "Exported slide 11 and 12 successfully!"
