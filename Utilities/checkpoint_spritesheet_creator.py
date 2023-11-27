from PIL import Image, ImageDraw, ImageFont

# Set the size of each tile and the number of tiles per row and column
tile_size = 128
tiles_per_row = 5
tiles_per_column = 5

# Calculate the total size of the spritesheet
spritesheet_size = (tile_size * tiles_per_row, tile_size * tiles_per_column)

# Create a new image for the spritesheet
spritesheet = Image.new("RGBA", spritesheet_size, color=(0, 0, 0, 0))

# Prepare to draw on the image
draw = ImageDraw.Draw(spritesheet)

# Load a font, using a default if necessary
try:
    font = ImageFont.truetype("arial", 40)
except IOError:
    font = ImageFont.load_default()

# Draw the numbers on the spritesheet
for i in range(1, 26):
    # Calculate the position for this tile
    x = (i - 1) % tiles_per_row * tile_size
    y = (i - 1) // tiles_per_column * tile_size

    # Calculate the position for the text
    text = str(i)
    text_width = draw.textlength(text, font=font)
    text_x = x + (tile_size - text_width) / 2
    text_y = y + (tile_size - font.size) / 2

    # Draw the number on the tile
    draw.text((text_x, text_y), text, fill="red", font=font)

# Save the spritesheet to a file
spritesheet_path = 'checkpoint_sprite.png'
spritesheet.save(spritesheet_path)
