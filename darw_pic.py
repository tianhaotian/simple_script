from PIL import ImageFont, ImageDraw, Image
from random import randrange, sample, choice
from cStringIO import StringIO
import os


def _draw_verify_pic(verify_code):
    img_width = 58
    img_height = 30
    font_size = 16
    font_color = ['black', 'darkblue', 'darkred']
    background = (randrange(230, 255), randrange(230, 255), randrange(230, 255))
    line_color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))

    sample_file = os.path.join(os.path.dirname(__file__), 'fonts/LucidaSansDemiOblique.ttf')
    font = ImageFont.truetype(sample_file, font_size)
    img = Image.new('RGB', (img_width, img_height), background)

    draw = ImageDraw.Draw(img)

    for i in range(randrange(3, 5)):
        xy = (randrange(0, img_width), randrange(0, img_height),
              randrange(0, img_width), randrange(0, img_height))
        draw.line(xy, fill=line_color, width=1)
        x = 2
    for i in verify_code:
        y = randrange(0, 10)
        draw.text((x, y), i, font=font, fill=choice(font_color))
        x += 14
    buf = StringIO()
    img.save(buf, 'gif')
    buf.seek(0)
    return buf.getvalue()


def gen_code():
    codes = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    verify_code = ''.join(sample(codes, 4))
    verify_pic = _draw_verify_pic(verify_code)
    return verify_pic


def gen_ver_gif(file_name):
    test = gen_code()
    with open(file_name, 'wb')as f:
        f.write(test)


if __name__ == '__main__':
    gen_ver_gif('test.gif')