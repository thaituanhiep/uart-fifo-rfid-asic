
 = New-Object -ComObject PowerPoint.Application
 = .Presentations.Open('C:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\test_table_slide.pptx', -1, 0, 0)
.SaveAs('C:\Users\HP DRAGONFLY G2\Desktop\uart-fifo-rfid-asic\rdm6300-picorv32-rom-data\document\temp\test_table_slide.png', 17)
.Close()
.Quit()
