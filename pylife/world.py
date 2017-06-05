# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long

# coding: utf-8

# Per la profilazione del codice:
# $ python -m cProfile world.py
# One liner per creazione della gif animata dai file immagine
# $ convert.exe -delay 5 -loop 0 $(ls -v *.bmp) world.gif
# oppure
# $ mplayer.exe mf://*.jpg -mf type=jpg -vo gif89a:fps=5:output=world.gif

#import moviepy.editor as mpy
from random import randint
import time
import os
import argparse
from PIL import Image, ImageDraw
from wand.image import Image as WImage
from pylife import Eukaryota


parser = argparse.ArgumentParser()
parser.add_argument('--xsize',
                    '-x',
                    type=int,
                    default=300,
                    help="Dimensione x del mondo virtuale")
parser.add_argument('--ysize',
                    '-y',
                    type=int,
                    default=300,
                    help="Dimensione y del mondo virtuale")
parser.add_argument('--creatures',
                    '-c',
                    type=int,
                    default=20,
                    help="Numero di creature esistenti all'inizio")
parser.add_argument('--food',
                    '-f',
                    type=int,
                    help="Quantità di cibo disponibile all'inizio (se non specificato, è uguale al numero delle creature)")
parser.add_argument('--ticks',
                    '-t',
                    type=int,
                    default=100,
                    help="Numero di tick di vita del mondo virtuale")
parser.add_argument('--save',
                    '-s',
                    action="store_true",
                    help="Attiva il salvataggio delle singole immagini")
parser.add_argument('--build',
                    '-b',
                    action="store_true",
                    help="Attiva la creazione della gif animata")
args = parser.parse_args()

XSIZE = args.xsize
YSIZE = args.ysize
CREATURES = args.creatures
if args.food is None:
    FOOD = CREATURES
else:
    FOOD = args.food
TICKS = args.ticks


creatures = []
places = [[0 for x in range(XSIZE)] for y in range(YSIZE)]
images = []


#print(args)
#print(args.build)
#quit()

#world_map = Image.new('RGB', (XSIZE, YSIZE), "black")
#pixels = world_map.load()
img = Image.new('RGB', (XSIZE, YSIZE), "black")
drw = ImageDraw.Draw(img)

if args.save is True:
    img_folder = str(int(time.time()))
    os.mkdir(img_folder)


#def addframe():
#    #img = Image.new('RGB', (XSIZE, YSIZE), "black")
#    #pixels = img.load()
#
#    for ii in range(world_map.size[0]):
#        for jj in range(world_map.size[1]):
#            #if getplace(ii, jj) == 1:
#            if places[ii][jj] == 1:
#                pixels[ii, jj] = (0, 0, 255)
#            #elif getplace(ii, jj) == 9:
#            #    pixels[ii, jj] = (255, 255, 0)
#
#    #images.append(world_map)

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
        drawpoint(x, y, "red")
        return False
    elif not places[x][y] == 0:
        drawpoint(x, y, "red")
        return False
    else:
        return True

def move(x, y, prev_x, prev_y):
    places[prev_x][prev_y] = 0
    places[x][y] = 1
    drawpoint(prev_x, prev_y, "black")
    drawpoint(x, y, "DodgerBlue")

def addfood(x, y):
    if checkplace(x, y):
        places[x][y] = 9
        drawpoint(x, y, "yellow")
        return True
    else:
        return False

def addcreature(x, y):
    if checkplace(x, y):
        places[x][y] = 1
        creatures.append(Eukaryota(x, y, checkplace, move))
        drawpoint(x, y, "DodgerBlue")
        return True
    else:
        drawpoint(x, y, "red")
        return False

def drawpoint(x, y, color):
    drw.point((x, y), fill=color)


for f_i in range(0, FOOD):
    f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addfood(f_x, f_y):
        f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)

for c_i in range(0, CREATURES):
    c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addcreature(c_x, c_y):
        c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)


print("Numero di creature: ", len(creatures))
print("Ticks: ", TICKS)

for i in range(TICKS):
    for creature in creatures:
        creature.tick()
    if (args.save is True) or (args.build is True):
        img.save(img_folder + "/" + str(i) + ".bmp")
        

if args.build is True:
    # creare la gif animata
    # convert.exe -delay 5 -loop 0 $(ls -v *.bmp) world.gif
    entries = []
    for entry in os.scandir(img_folder):
        if entry.is_file() is True:
            entries.append(os.path.splitext(entry.name)[0])
    entries.sort(key=int)
    with WImage() as wand:
        for item in entries:
            with WImage(filename=img_folder + "/" + str(item) + ".bmp") as frame:
                frame.delay = 5
                wand.sequence.append(frame)
        wand.type = 'optimize'
        wand.save(filename=img_folder + "/world.gif")

dump()
if args.save is True:
    del drw
# https://pymotw.com/2/threading/index.html#module-threading
