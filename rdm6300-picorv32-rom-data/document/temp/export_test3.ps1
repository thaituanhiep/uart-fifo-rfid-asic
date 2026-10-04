$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\test_3slides.pptx", 0, 0, 0)
$pres.Slides.Item(1).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\test_slide_01.png", "PNG", 1920, 1080)
$pres.Slides.Item(2).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\test_slide_02.png", "PNG", 1920, 1080)
$pres.Slides.Item(3).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\test_slide_03.png", "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Host "Exported all 3 test slides successfully"
