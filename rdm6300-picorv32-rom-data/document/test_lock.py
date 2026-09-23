import os
try:
    with open('Bao_Cao_Do_An_RDM6300_PicoRV32_SoC.docx', 'r+b') as f:
        print("File is writable / unlocked!")
except Exception as e:
    print("File is locked:", e)
