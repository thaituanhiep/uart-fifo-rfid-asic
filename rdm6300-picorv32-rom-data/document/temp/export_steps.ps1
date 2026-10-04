$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open('d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.pptx')
$pres.Slides.Item(10).Export('d:\VirtualSharedFolders\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\slide_10_bus_table_16.png', 'PNG')
$pres.Close()
$ppt.Quit()
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
Write-Host "Slide 10 exported successfully!"
