# pylint: disable=locally-disabled,missing-docstring,invalid-name

# coding: utf-8

# Per la profilazione del codice:
# $ python -m cProfile world.py

from random import randint
from PIL import Image
#import moviepy.editor as mpy
from pylife import Eukaryota


MAXCREATURES = 20  # 10000
XSIZE = 300
YSIZE = 300
MAXFOOD = MAXCREATURES
TEMPTICKS = 10 # 5000

creatures = []
places = [[0 for x in range(XSIZE)] for y in range(YSIZE)]
images = []

world_map = Image.new('RGB', (XSIZE, YSIZE), "black")
pixels = world_map.load()


def addframe():
    #img = Image.new('RGB', (XSIZE, YSIZE), "black")
    #pixels = img.load()

    for ii in range(world_map.size[0]):
        for jj in range(world_map.size[1]):
            if getplace(ii, jj) == 1:
                pixels[ii, jj] = (0, 0, 255)
            #elif getplace(ii, jj) == 9:
            #    pixels[ii, jj] = (255, 255, 0)

    images.append(world_map)


def dump():
    #img = Image.new('RGB', (XSIZE, YSIZE), "black")
    #pixels = img.load()

    for ii in range(world_map.size[0]):
        for jj in range(world_map.size[1]):
            if getplace(ii, jj) == 1:
                pixels[ii, jj] = (0, 0, 255)
            elif getplace(ii, jj) == 9:
                pixels[ii, jj] = (255, 255, 0)

    #img.show()
    world_map.show()
    # aggiungere salvataggio su file


def getplace(x, y):
    return places[x][y]


def checkplace(x, y):
    if (x >= XSIZE - 1) or (y >= YSIZE - 1):
        return False
    elif not places[x][y] == 0:
        #print("checkplace(", x, ",", y, ") is busy")
        return False
    else:
        return True

def move(x, y):
    places[x][y] = 1


def addfood(x, y):
    if checkplace(x, y):
        places[x][y] = 9
        return True
    else:
        return False


def addcreature(x, y):
    if checkplace(x, y):
        places[x][y] = 1
        creatures.append(Eukaryota(x, y, checkplace, move))
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

for i in range(TEMPTICKS):
    for creature in creatures:
        creature.tick()
        addframe()

dump()

#gif = Image.new('RGB', (XSIZE, YSIZE), "black")  # Image.fromarray(images)
#gif.show()
#print(images[3].tobytes())
# https://pymotw.com/2/threading/index.html#module-threading
