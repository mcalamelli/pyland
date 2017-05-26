# -*- coding: utf-8 -*-


import pylife
from random import randint
from PIL import Image

MAXCREATURES = 500  # 10000
XSIZE = 300
YSIZE = 300
MAXFOOD = MAXCREATURES

creatures = []
places = [[0 for x in range(XSIZE)] for y in range(YSIZE)]


def dump():
    img = Image.new('RGB', (XSIZE, YSIZE), "black")
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if getplace(i, j) == 1:
                pixels[i, j] = (0, 0, 255)
            elif getplace(i, j) == 9:
                pixels[i, j] = (255, 255, 0)

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


for i in range(0, MAXFOOD):
    x, y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addfood(x, y):
        x, y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)

for i in range(0, MAXCREATURES):
    x, y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addcreature(x, y):
        x, y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)


print("Numero di creature: ", len(creatures))

dump()

# https://pymotw.com/2/threading/index.html#module-threading
