"""
Simple Splash Screen Generator for Snake Game
Creates a splash screen image using PIL/Pillow
"""

import os

from PIL import Image, ImageDraw, ImageFont

# Create splash screen image
width = 720
height = 1280
background_color = (34, 139, 34)  # Forest green
text_color = (255, 255, 255)  # White

# Create image
img = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(img)

# Add title text
try:
    # Try to use a nice font
    title_font = ImageFont.truetype("arial.ttf", 100)
    subtitle_font = ImageFont.truetype("arial.ttf", 40)
except OSError:
    # Fallback to default font
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

# Draw title
title = "🐍 ЗМЕЙКА"
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (width - title_width) // 2
draw.text((title_x, height // 3), title, fill=text_color, font=title_font)

# Draw subtitle
subtitle = "Snake Game"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (width - subtitle_width) // 2
draw.text((subtitle_x, height // 2), subtitle,
          fill=text_color, font=subtitle_font)

# Draw snake body pattern
snake_color = (50, 205, 50)  # Lime green
segment_size = 40
for i in range(8):
    x = width // 2 - 160 + i * segment_size
    y = height * 2 // 3
    draw.rectangle([x, y, x + segment_size - 5, y + segment_size - 5],
                   fill=snake_color, outline=(255, 255, 255), width=2)

# Draw loading text
loading_text = "Загрузка..."
loading_bbox = draw.textbbox((0, 0), loading_text, font=subtitle_font)
loading_width = loading_bbox[2] - loading_bbox[0]
loading_x = (width - loading_width) // 2
draw.text((loading_x, height * 4 // 5), loading_text,
          fill=text_color, font=subtitle_font)

# Save image
output_path = os.path.join(os.path.dirname(__file__), 'splash.png')
img.save(output_path)
print(f"Splash screen created: {output_path}")
