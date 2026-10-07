$src = "C:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\test_slide1_logos.pptx"
$out = "C:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\test_s1_logos.png"
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($src, 1, 0, 0)
$pres.Slides.Item(1).Export($out, "PNG", 1600, 900)
$pres.Close()
$ppt.Quit()
Write-Host "Exported test s1 successfully"
