$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx", 0, 0, 0)
$pres.Slides.Item(7).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\final_slide_07.png", "PNG", 1920, 1080)
$pres.Slides.Item(8).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\final_slide_08.png", "PNG", 1920, 1080)
$pres.Slides.Item(9).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\final_slide_09.png", "PNG", 1920, 1080)
$pres.Slides.Item(10).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\final_slide_10.png", "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Host "Exported main slides 7, 8, 9, 10 successfully"
