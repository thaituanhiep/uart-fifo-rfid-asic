// Tool to convert binary firmware to 32-bit word hex for Verilog $readmemh
#include <stdio.h>
#include <stdlib.h>

#define TOTAL_WORDS 2048 // 8 KBytes

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: bin2hex <input.bin> <output.hex>\n");
        return 1;
    }

    FILE *fin = fopen(argv[1], "rb");
    if (!fin) {
        perror("Failed to open input file");
        return 1;
    }

    FILE *fout = fopen(argv[2], "w");
    if (!fout) {
        perror("Failed to open output file");
        fclose(fin);
        return 1;
    }

    unsigned char buf[4];
    size_t n;
    int word_count = 0;

    while ((n = fread(buf, 1, 4, fin)) > 0) {
        for (size_t i = n; i < 4; i++) {
            buf[i] = 0; // Pad last word with zeros
        }
        // Write little-endian word: MSB to LSB = byte 3, byte 2, byte 1, byte 0
        fprintf(fout, "%02x%02x%02x%02x\n", buf[3], buf[2], buf[1], buf[0]);
        word_count++;
    }

    // Pad remainder of memory up to 2048 words with NOP instructions (addi x0, x0, 0 = 0x00000013)
    while (word_count < TOTAL_WORDS) {
        fprintf(fout, "00000013\n");
        word_count++;
    }

    fclose(fin);
    fclose(fout);
    printf("Successfully converted %d words to %s\n", word_count, argv[2]);
    return 0;
}
