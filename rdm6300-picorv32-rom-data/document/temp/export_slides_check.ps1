$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx", 0, 0, 0)
$pres.Slides.Item(7).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_07_firmware_code_v2.png", "PNG", 1920, 1080)
$pres.Slides.Item(8).Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_08_bus_table_v2.png", "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Host "Exported slide 7 and 8 v2 successfully"
