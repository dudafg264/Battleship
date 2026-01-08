from PIL import Image

# Load the image (ensure it's 64x64)
image_path = "image64.png"  # Replace with your image file path
image = Image.open(image_path)
image = image.resize((64, 64))  # Ensure it's exactly 64x64

# Convert image to RGB format
image = image.convert("RGB")

# Initialize the list for hexadecimal colors
color_vector = []

# Loop through each pixel to get RGB values and convert to 0xRRGGBB format
for y in range(64):
    for x in range(64):
        r, g, b = image.getpixel((x, y))
        color_hex = (r << 16) | (g << 8) | b  # Convert to 0xRRGGBB
        color_vector.append(f"0x{color_hex:06X}")

# Convert the color vector into a single MIPS assembly word format
color_vector_str = ", ".join(color_vector)

# Generate MIPS code to load the image into the Bitmap Display
mips_code = f"""
.data
bitmap_display: .word 0x10010000  # Base address of Bitmap Display
color_vector:  .word {color_vector_str}  # All colors as a single vector

.text
main:
    li $t0, 0x10010000  # Load base address of Bitmap Display
    la $t8, color_vector  # Load address of color vector

    # Update 64x64 cell with colors from vector
    li $s0, 64          # Row counter
row_loop:
    li $s1, 64          # Column counter
col_loop:
    lw $t9, 0($t8)      # Load color from vector
    sw $t9, 0($t0)      # Store color in Bitmap Display
    addiu $t0, $t0, 4   # Move to next pixel in row
    addiu $t8, $t8, 4   # Move to next color in vector
    subu $s1, $s1, 1    # Decrease column counter
    bnez $s1, col_loop  # Repeat for all 64 columns

    subu $s0, $s0, 1    # Decrease row counter
    addiu $t0, $t0, 1792 # Move to next row (512*4 - 64*4)
    bnez $s0, row_loop  # Repeat for all 64 rows

    jr $ra              # Return
"""

# Save the generated MIPS code to a file
with open("generate_image_mips.asm", "w") as f:
    f.write(mips_code)

print("MIPS code generated and saved as 'generate_image_mips.asm'")
