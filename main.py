from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os, math


def size_change(img_change):
    width, height = img_change.size
    fixed_width = 800
    width_percent = fixed_width / width
    height = width_percent * height
    img_change = img_change.resize((fixed_width, int(height)))

    return img_change


def img_rotate(img_change, angle):
    img_change = img_change.rotate(angle)

    return img_change


def img_smart_rotate(img_change, angle):
    img_change = img_change.rotate(angle)
    width, height = img_change.size
    w = abs(height*math.sin(math.radians(angle))/2)
    h = abs(width*math.sin(math.radians(angle))/2)
    img_change = img_change.crop((w, h, width -w, height-h))

    return img_change


def mask(img1, img2):
    img2 = img2.convert('L').resize(img1.size)

    img1.putalpha(img2)
    return img1

def img_crop(img, a):
    width, height = img.size
    img = img.crop((a,a,width-a,height-a))
    return  img

if __name__ == '__main__':

    with open("config.txt", 'r', encoding='utf-8') as f:
        config = f.read()
    f.close()
    config = config.split('\n')
    path = config[0]

    new_dir = os.path.join(path, os.path.basename(path))
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    for lists in os.listdir(path):
        path_img = os.path.join(path, lists)

        suffix = ('.png', 'jpg')
        if path_img.endswith(suffix):
            i = os.path.basename(path_img)
            new_img_path = os.path.join(new_dir, i)
            img1 = Image.open(path_img)



            im2 = Image.open('маска.jpg')  # маска для изображения
            fill_color = 'black'
            im2 = ImageOps.invert(im2)  # если накладывается картинка на белом фоне, эту строку закоментить
            img1 = mask(img1, im2)           #накладывает прозрачное изображение(изображение на черном фоне)

            fill_color = 'black'
            if img1.mode in ('RGBA', 'LA'):  # это для нормальной работы маски
                background = Image.new(img1.mode[:-1], img1.size, fill_color)
                background.paste(img1, img1.split()[-1])
                img1 = background

            img1 = img_crop(img1, 10) #обрезает картинки, второй параметр - колл пикселей
            img1 = img_smart_rotate(img1, 3) #вращает картинки на угол, указанный вторым параметром + обрезает черные углы
            img1 = size_change(img1) #делает картинку 800Х600(второй параметр может быть меньше)

            img1.save(new_img_path)















