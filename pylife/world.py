# pylint: disable=locally-disabled,missing-docstring,invalid-name

# coding: utf-8

from random import randint
from PIL import Image
import pylife

MAXCREATURES = 500  # 10000
XSIZE = 300
YSIZE = 300
MAXFOOD = MAXCREATURES

creatures = []
places = [[0 for x in range(XSIZE)] for y in range(YSIZE)]


def dump():
    img = Image.new('RGB', (XSIZE, YSIZE), "black")
    pixels = img.load()

    for ii in range(img.size[0]):
        for jj in range(img.size[1]):
            if getplace(ii, jj) == 1:
                pixels[ii, jj] = (0, 0, 255)
            elif getplace(ii, jj) == 9:
                pixels[ii, jj] = (255, 255, 0)

    img.show()
    # aggiungere salvataggio su file


def getplace(x, y):
    return places[x][y]


def checkplace(x, y):
    if not places[x][y] == 0:
        return False
    else:
        return True


def addfood(x, y):
    if checkplace(x, y):
        places[x][y] = 9
        return True
    else:
        return False


def addcreature(x, y):
    if checkplace(x, y):
        places[x][y] = 1
        creatures.append(pylife.Eukaryota(x, y))
        return True
    else:
        return False


for f_i in range(0, MAXFOOD):
    f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addfood(f_x, f_y):
        f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)

for c_i in range(0, MAXCREATURES):
    c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addcreature(c_x, c_y):
        c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)


print("Numero di creature: ", len(creatures))

dump()

# https://pymotw.com/2/threading/index.html#module-threading
