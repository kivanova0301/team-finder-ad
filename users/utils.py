import random
from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

AVATAR_SIZE = 200
AVATAR_COLORS = (
    '#6C8EBF',
    '#82B366',
    '#D6A76C',
    '#B85450',
    '#9673A6',
    '#5B9AA0',
    '#C27BA0',
    '#7A8B99',
)
TEXT_COLOR = '#FFFFFF'
FONTS_DIR = settings.BASE_DIR / 'static' / 'fonts'


def get_font(size):
    """Берёт первый шрифт .ttf/.otf из static/fonts, иначе стандартный."""
    for pattern in ('*.ttf', '*.otf'):
        font_files = sorted(FONTS_DIR.glob(pattern))
        if font_files:
            return ImageFont.truetype(str(font_files[0]), size)
    return ImageFont.load_default(size=size)


def generate_avatar(name):
    """Создаёт картинку с первой буквой имени на однотонном фоне."""
    letter = (name[:1] or '?').upper()
    image = Image.new(
        'RGB', (AVATAR_SIZE, AVATAR_SIZE), random.choice(AVATAR_COLORS)
    )
    draw = ImageDraw.Draw(image)
    draw.text(
        (AVATAR_SIZE / 2, AVATAR_SIZE / 2),
        letter,
        fill=TEXT_COLOR,
        font=get_font(AVATAR_SIZE // 2),
        anchor='mm',
    )
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'{uuid4().hex}.png')
