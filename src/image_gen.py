import os
from os import path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
import io
from CodeStyle import CustomCodeStyle
from json_loader import load_json

def create_code_image(code, output_file, file_name):
    ext = file_name.split('.')[-1]
    try:
        lexer = get_lexer_by_name(ext)
    except Exception:
        lexer = get_lexer_by_name('text')

    formatter = ImageFormatter(
        font_name='Menlo',
        font_size=24,
        line_numbers=False,
        style='pastie',
        image_pad=20,
        line_pad=15,
        dpi=800,
    )

    highlighted_code = highlight(code, lexer, formatter)
    img_data = io.BytesIO(highlighted_code)
    img = Image.open(img_data).convert("RGBA")

    bg_width, bg_height = img.size
    frosted_bg = Image.new('RGBA', (bg_width + 40, bg_height + 90), (119, 228, 200, 255))
    frosted_bg = frosted_bg.filter(ImageFilter.GaussianBlur(10))

    draw = ImageDraw.Draw(frosted_bg)
    draw.rectangle([20, 50, 20 + bg_width, 50 + bg_height], fill=(239, 98, 159, 128))

    img_resized = Image.new('RGBA', frosted_bg.size, (76, 161, 175, 0))
    img_resized.paste(img, (20, 50))

    final_image = Image.alpha_composite(frosted_bg, img_resized)
    draw = ImageDraw.Draw(final_image)

    bar_height = 30
    draw.rectangle([0, 0, final_image.width, bar_height], fill=(40, 44, 52))
    draw.ellipse([10, 10, 20, 20], fill=(255, 95, 86))
    draw.ellipse([30, 10, 40, 20], fill=(255, 189, 46))
    draw.ellipse([50, 10, 60, 20], fill=(39, 201, 63))

    title_font = ImageFont.truetype("FiraCode.ttf", 20)
    draw.text((75, 5), file_name, font=title_font, fill=(76, 161, 175))
    draw.text((final_image.width - 100, 5), "by _rust.rs 💕", font=title_font, fill=(76, 161, 175))

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    watermark_text = "made BY Anil"
    watermark_font = ImageFont.truetype("FiraCode-SemiBold.ttf", 20)
    text_width, text_height = draw.textbbox((0, 0), watermark_text, font=watermark_font)[2:]
    watermark_position = (final_image.width - text_width - 20, final_image.height - text_height - 10)
    draw.text(watermark_position, watermark_text, font=watermark_font, fill=(255, 127, 62, 128))

    final_image.save(output_file, format='PNG')
    print(f"Code image saved to {output_file}")

def generate_code_images(json_path):
    data = load_json(json_path)
    for key, code in data.items():
        question_number, extension = key.split('.')
        file_name = f"{question_number}.{extension}"
        output_file = os.path.join('./CodeImg', f"{question_number}_{extension}.png")
        if path.exists(output_file):
            print(f"{output_file} exists.")
        else:
            create_code_image(code, output_file, file_name)
