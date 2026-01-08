from PIL import Image

# Load image and convert to RGB
image_path = "image.png"  # Change this to your PNG file
output_asm = "saida.asm"

img = Image.open(image_path).convert("RGB")
width, height = img.size

if width != 512 or height != 512:
    raise ValueError("The image must be exactly 512x512 pixels.")

# Open the output ASM file
with open(output_asm, "w") as f:
    f.write(".data\n")
    f.write("bitmap_display: .word 0x10010000  # Bitmap Display Address\n")
    f.write("pixel_data: .word ")

    # Store pixel data as a memory array
    pixel_values = []
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            color = (r << 16) | (g << 8) | b  # Convert to 0xRRGGBB format
            pixel_values.append(f"0x{color:06X}")

    f.write(", ".join(pixel_values))  # Store pixel data efficiently
    f.write("\n\n.text\n")
    f.write("main:\n")
    f.write("    li $t0, 0x10010000  # Load base address of Bitmap Display\n")
    f.write("    la $t1, pixel_data  # Load base address of pixel array\n")
    f.write("    li $t2, 262144      # Set loop counter (512*512 pixels)\n")

    # Loop to write pixels
    f.write("loop:\n")
    f.write("    lw $t3, 0($t1)      # Load pixel color\n")
    f.write("    sw $t3, 0($t0)      # Store it in Bitmap Display\n")
    f.write("    addiu $t1, $t1, 4   # Move to next pixel in array\n")
    f.write("    addiu $t0, $t0, 4   # Move to next pixel in Bitmap Display\n")
    f.write("    subu $t2, $t2, 1    # Decrease loop counter\n")
    f.write("    bnez $t2, loop      # Repeat until all pixels are written\n")

    f.write("    jr $ra              # Return\n")

print(f"MIPS assembly saved to {output_asm}")
