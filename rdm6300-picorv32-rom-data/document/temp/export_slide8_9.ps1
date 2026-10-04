$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx", 0, 0, 0)
$pres.Slides.Item(8).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_08_interconnect.png", "PNG", 1920, 1080)
$pres.Slides.Item(9).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_09_execution_steps.png", "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Host "Exported slides 8 and 9 successfully"
