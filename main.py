from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os, math
from datetime import date, time, datetime


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
    img2 = img2.convert('RGBA')
    img1 = img1.convert('RGBA')
    img2 = img2.resize(img1.size)
    img1 = Image.alpha_composite(img1, img2)
    bg = Image.new("RGB", img1.size, (255, 255, 255))
    bg.paste(img1, img1)
    return bg


def img_crop(img, a):
    width, height = img.size
    img = img.crop((a,a,width-a,height-a))
    return  img

def in_folder(path):

    with open("config.txt", 'r', encoding='utf-8') as f:
        config = f.read()
    f.close()
    config = config.split('\n')
    name = config[1]
    mask_path = config[2]
    flag = config[3]
    name = os.path.basename(path) + '_' +name
    new_dir = os.path.join(path, name)
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    for lists in os.listdir(path):
        path_img = os.path.join(path, lists)

        suffix = ('.png', 'jpg')
        if path_img.endswith(suffix):
            i = os.path.basename(path_img)
            new_img_path = os.path.join(new_dir, i)

            if flag == 1:

                img1 = Image.open(path_img)
                im2 = Image.open(mask_path)  # маска для изображени
                # img1 = img_crop(img1, 10)  # обрезает картинки, второй параметр - колл пикселей
                img1 = img_smart_rotate(img1, 3)  # вращает картинки на угол, указанный вторым параметром + обрезает черные углы
                img1 = mask(img1, im2)
                img1 = size_change(img1)  # делает картинку 800Х600(второй параметр может быть меньше)

                img1.save(new_img_path)
            else:
                if os.path.exists(new_img_path):

                    pass
                else:
                    img1 = Image.open(path_img)
                    im2 = Image.open(mask_path)  # маска для изображени
                    # img1 = img_crop(img1, 10)  # обрезает картинки, второй параметр - колл пикселей
                    img1 = img_smart_rotate(img1, 3)  # вращает картинки на угол, указанный вторым параметром + обрезает черные углы
                    img1 = mask(img1, im2)
                    img1 = size_change(img1)

                    img1.save(new_img_path)


def search_folder(path):
    for lists in os.listdir(path):

        in_right_dir = False
        for file in os.listdir(path):
            suffix = ('.png', 'jpg')
            if file.endswith(suffix):

                in_right_dir= True
                break

        if in_right_dir:
            in_folder(path)
            f = open('log.txt', 'a')
            d = datetime.now()
            d_string = d.strftime("     %d/%m/%Y   %H:%M:%S ")
            print(os.path.basename(path), ' обработан ',d_string)
            f.write(os.path.basename(path))
            f.write(d_string)
            f.write('\n')
            f.close()
            break
        if not in_right_dir:
            path1 = os.path.join(path, lists)
            if os.path.isdir(path1): search_folder(path1)
if __name__ == '__main__':

    with open("config.txt", 'r', encoding='utf-8') as f:
        config = f.read()
    f.close()
    config = config.split('\n')
    path = config[0]

    search_folder(path)





