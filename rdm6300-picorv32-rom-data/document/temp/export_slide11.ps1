$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx", 0, 0, 0)
$slide11 = $pres.Slides.Item(11)
$slide11.Export("d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_11_3col.png", "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Host "Exported slide 11 successfully"
