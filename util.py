import random
# pillow模块
from PIL import Image, ImageFont, ImageDraw, ImageFilter

# 随机颜色
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# 生成一张图片
def generate_image(length):
    s = 'qwerQWERTYUIOtyuiopas123456dfghjklPASDFGHJKLZXCVBNMxcvbnm7890'
    size = (130, 35)
    # 创建画布背景 mode, size, color
    im = Image.new('RGB', size, color=get_random_color())
    # im.show()
    # 创建字体 font, size=1, index, encoding, layout_engine windows C:\Windows\Fonts
    font = ImageFont.truetype('font/GILLUBCD.TTF', size=25)
    # 创建ImageDraw对象
    draw = ImageDraw.Draw(im)
    # 绘制验证码
    code = ''
    for i in range(length):
        # 选择其中一个字母
        c = random.choice(s)
        # 拼接
        code += c
        # 位置 内容 颜色 字体
        draw.text((9+random.randint(4,7)+25*i, 1),
                  text=c,
                  fill=get_random_color(),
                  font=font)
    # 绘制干扰线
    for i in range(5):
        x1 = random.randint(0, 130)
        y1 = random.randint(0, 50 / 2)
        x2 = random.randint(0, 130)
        y2 = random.randint(50 / 2, 50)
        # xy, fill
        draw.line(((x1, y1), (x2, y2)), fill=get_random_color())

    # im.show( )
    # 加滤镜 增强EDGE_ENHANCE 模糊BLUR
    im = im.filter(ImageFilter.EDGE_ENHANCE)
    # im.show( )
    return im, code

if __name__ == '__main__':
    generate_image(4)
