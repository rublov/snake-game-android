"""
Create icon.png for Android app
Icon size: 512x512 pixels
"""

from PIL import Image, ImageDraw, ImageFont

# Create 512x512 icon with green background
width = 512
height = 512
background_color = (34, 139, 34)  # Forest green

img = Image.new('RGB', (width, height), color=background_color)
draw = ImageDraw.Draw(img)

# Try to load a font, fallback to default
try:
    # Try different font sizes for the emoji
    font_size = 300
    font = ImageFont.truetype("seguiemj.ttf", font_size)
except:
    try:
        font = ImageFont.truetype("arial.ttf", 256)
    except:
        font = ImageFont.load_default()

# Draw snake emoji
text = "🐍"

# Get text size and center it
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = (width - text_width) // 2
y = (height - text_height) // 2

draw.text((x, y), text, fill=(255, 255, 255), font=font)

# Add a subtle border
border_width = 10
draw.rectangle(
    [0, 0, width-1, height-1],
    outline=(255, 255, 255),
    width=border_width
)

# Save icon
img.save('icon.png')
print("✓ icon.png создан! (512x512)")
print("  Файл готов для использования в Android APK")
