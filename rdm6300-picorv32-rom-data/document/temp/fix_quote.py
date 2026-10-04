with open('create_presentation.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the offending line
bad_line = '            "            "    uart_puts(\\"\\n[SYSTEM] PicoRV32 RFID Access Control Ready.\\n\\");",'
good_line = '            "    uart_puts(\\"\\\\n[SYSTEM] PicoRV32 RFID Access Control Ready.\\\\n\\");",'

if bad_line in text:
    text = text.replace(bad_line, good_line)
    print("Found and replaced bad_line")
else:
    # search by uart_puts
    import re
    text = re.sub(r'^\s*".*uart_puts.*$', '            "    uart_puts(\\"[SYSTEM] PicoRV32 RFID Access Control Ready.\\");",', text, flags=re.MULTILINE)
    print("Replaced with regex")

with open('create_presentation.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done")
