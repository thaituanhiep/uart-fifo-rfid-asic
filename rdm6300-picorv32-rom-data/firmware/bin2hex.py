# bin2hex.py: Converts binary firmware to 32-bit word hex for Verilog $readmemh
import sys

def bin2hex(bin_path, hex_path, total_words=2048):
    with open(bin_path, 'rb') as f:
        data = f.read()
    
    words = []
    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        # Pad chunk with zeros to 4 bytes if needed
        if len(chunk) < 4:
            chunk = chunk + b'\x00' * (4 - len(chunk))
        # Little-endian 32-bit word format: MSB to LSB = byte 3, byte 2, byte 1, byte 0
        word_hex = f"{chunk[3]:02x}{chunk[2]:02x}{chunk[1]:02x}{chunk[0]:02x}"
        words.append(word_hex)
    
    # Pad remainder with NOP (addi x0, x0, 0 = 0x00000013)
    while len(words) < total_words:
        words.append("00000013")
    
    with open(hex_path, 'w') as f:
        for w in words:
            f.write(w + "\n")
    
    print(f"Successfully converted {len(words)} words to {hex_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: py bin2hex.py <input.bin> <output.hex>")
        sys.exit(1)
    bin2hex(sys.argv[1], sys.argv[2])
