from PIL import Image


def reshpe(name1, name2, size_x, size_y):
    im = Image.open(name1)
    im2 = im.resize((size_x, size_y))
    im2.save(name2)

def crop(name1, name2, x_l, y_u, x_r, y_l):
    im = Image.open(name1)
    im2 = im.crop((x_l, y_u, x_r, y_l))
    im2.save(name2)


# reshpe('pictures/gardenWall_1.png', "pictures/gardenWall_2.png", 160, 120)
