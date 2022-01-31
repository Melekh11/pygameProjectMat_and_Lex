from PIL import Image


def hide_pic(name1, name2):
    im_rgb = Image.open(name1)
    im_rgba = im_rgb.copy()
    im_rgba.putalpha(128)
    im_rgba.save(f'pictures/{name2}.png')


def reshpe(name1, name2, size_x, size_y):
    im = Image.open(name1)
    im2 = im.resize((size_x, size_y))
    im2.save(name2)

def crop(name1, name2, x_l, y_u, x_r, y_l):
    im = Image.open(name1)
    im2 = im.crop((x_l, y_u, x_r, y_l))
    im2.save(name2)


# hide_pic("pictures/dog.png", "dog_hide")
reshpe("pictures/gameover.png", "pictures/gameover.png", 1000, 800)
