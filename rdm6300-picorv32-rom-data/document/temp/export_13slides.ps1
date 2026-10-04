$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx", 0, 0, 0)
$pres.Slides.Item(2).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_02_agenda.png", "PNG", 1920, 1080)
$pres.Slides.Item(6).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_06_block_diagram_13.png", "PNG", 1920, 1080)
$pres.Slides.Item(7).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_07_tb1.png", "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Host "Exported slides 2, 6, 7 successfully"
