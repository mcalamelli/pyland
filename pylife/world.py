# pylint: disable=locally-disabled,missing-docstring,invalid-name

# coding: utf-8

# Per la profilazione del codice:
# $ python -m cProfile world.py

from random import randint
import time
import os
from PIL import Image, ImageDraw
#import moviepy.editor as mpy
from pylife import Eukaryota


MAXCREATURES = 10  # 10000
XSIZE = 300
YSIZE = 300
MAXFOOD = MAXCREATURES
TEMPTICKS = 5000 # 5000


creatures = []
places = [[0 for x in range(XSIZE)] for y in range(YSIZE)]
images = []

world_map = Image.new('RGB', (XSIZE, YSIZE), "black")
pixels = world_map.load()
img = Image.new('RGB', (XSIZE, YSIZE), "black")
drw = ImageDraw.Draw(img)

img_folder = str(int(time.time()))
os.mkdir(img_folder)


def addframe():
    #img = Image.new('RGB', (XSIZE, YSIZE), "black")
    #pixels = img.load()

    for ii in range(world_map.size[0]):
        for jj in range(world_map.size[1]):
            #if getplace(ii, jj) == 1:
            if places[ii][jj] == 1:
                pixels[ii, jj] = (0, 0, 255)
            #elif getplace(ii, jj) == 9:
            #    pixels[ii, jj] = (255, 255, 0)

    #images.append(world_map)

#def dump():
#    for ii in range(world_map.size[0]):
#        for jj in range(world_map.size[1]):
#            if places[ii][jj] == 1:
#                pixels[ii, jj] = (0, 0, 255)
#            elif places[ii][jj] == 9:
#                pixels[ii, jj] = (255, 255, 0)
#
#    world_map.show()
#    # aggiungere salvataggio su file

def dump():
    img.show()

def checkplace(x, y):
    if (x >= XSIZE - 1) or (y >= YSIZE - 1):
        #drw.point((x, y), fill="red")
        drawpoint(x, y, "red")
        return False
    elif not places[x][y] == 0:
        #drw.point((x, y), fill="red")
        drawpoint(x, y, "red")
        return False
    else:
        return True

def move(x, y, prev_x, prev_y):
    places[x][y] = 1
    #drw.point((x, y), fill="blue")
    drawpoint(x, y, "blue")

def addfood(x, y):
    if checkplace(x, y):
        places[x][y] = 9
        #drw.point((x, y), fill="yellow")
        drawpoint(x, y, "yellow")
        return True
    else:
        return False

def addcreature(x, y):
    if checkplace(x, y):
        places[x][y] = 1
        creatures.append(Eukaryota(x, y, checkplace, move))
        #drw.point((x, y), fill="blue")
        drawpoint(x, y, "blue")
        return True
    else:
        #drw.point((x, y), fill="red")
        drawpoint(x, y, "red")
        return False

def drawpoint(x, y, color):
    drw.point((x, y), fill=color)
    #img.save(img_folder + "/" + str(int(time.time())) + ".jpg")


for f_i in range(0, MAXFOOD):
    f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addfood(f_x, f_y):
        f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)

for c_i in range(0, MAXCREATURES):
    c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addcreature(c_x, c_y):
        c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)


print("Numero di creature: ", len(creatures))
print("Ticks: ", TEMPTICKS)

for i in range(TEMPTICKS):
    for creature in creatures:
        creature.tick()
        img.save(img_folder + "/" + str(int(time.time())) + ".jpg")
        #addframe()

dump()
del drw
# https://pymotw.com/2/threading/index.html#module-threading
# $ convert.exe -delay 5 -loop 0 *.jpg world.gif
