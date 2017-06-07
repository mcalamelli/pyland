# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long

# coding: utf-8

# Per la profilazione del codice:
# $ python -m cProfile world.py
# One liner per creazione della gif animata dai file immagine
# $ convert.exe -delay 5 -loop 0 $(ls -v *.bmp) world.gif
# oppure
# $ mplayer.exe mf://*.jpg -mf type=jpg -vo gif89a:fps=5:output=world.gif

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
parser.add_argument('--delete',
                    '-d',
                    action="store_true",
                    help="Cancella i file BMP utilizzati per la creazione della gif animata (vale solo epr opzione -b / --build")
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

#print(args)
#print(args.build)
#quit()

img = Image.new('RGB', (XSIZE, YSIZE), "black")
drw = ImageDraw.Draw(img)
wand = WImage()

if (args.save is True) or (args.build is True):
    img_folder = str(int(time.time()))
    os.mkdir(img_folder)

def dump():
    img.show()

def checkplace(x, y):
    if (x >= XSIZE - 1) or (y >= YSIZE - 1) or (x <= 0) or (y <= 0):
        # fuori dai confini del mondo, non valida
        drawpoint(x, y, "red")
        return -1  # return False
    elif places[x][y] == 1:
        # posizione già occupata, non valida
        drawpoint(x, y, "red")
        return -1  # return False
    elif places[x][y] == 9:
        # posizione occupata da cibo, valida
        return 0
    else:
        # posizione libera
        return 1  # return True

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

def dead(o):
    places[o.x][o.y] = 0
    drawpoint(o.x, o.y, "DeepPink")
    creatures.remove(o)

def addcreature(x, y):
    if checkplace(x, y):
        places[x][y] = 1
        creatures.append(Eukaryota(x, y, checkplace, move, dead))
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
print("Cibo disponibile: ", FOOD)
print("Ticks: ", TICKS)

for i in range(TICKS):
    for creature in creatures:
        creature.tick()
    if (args.save is True) or (args.build is True):
        # salvo i file BMP relativi ad ogni tick
        img_path = img_folder + "/" + str(i).zfill(len(str(TICKS - 1))) + ".bmp"
        img.save(img_path)
        with WImage(filename=img_path) as frame:
            frame.delay = 5
            wand.sequence.append(frame)
        os.remove(img_path) # funziona, vedere come gestire la cosa


if args.build is True:
    # crearo la gif animata
    # entries = []
    # for entry in os.scandir(img_folder):
    #     if entry.is_file() is True:
    #         entries.append(os.path.splitext(entry.name)[0])
    # entries.sort(key=int)
    # with WImage() as wand1:
    #     for item in entries:
    #         with WImage(filename=img_folder + "/" + str(item) + ".bmp") as frame:
    #             frame.delay = 5
    #             wand1.sequence.append(frame)
    #     wand1.type = 'optimize'
    #     wand1.save(filename=img_folder + "/world.gif")
    # if args.delete is True:
    #     # elimino i file BMP utilizzati per creare la GIF
    #     entries = list(entries)
    #     for bmp in entries:
    #         os.remove(img_folder + "/" + str(bmp) + ".bmp")
    print("Salvataggio sequenza...")
    wand.save(filename=img_folder + "/world.gif")


#dump()

for c in creatures:
    print(c)

if args.save is True:
    del drw
# https://pymotw.com/2/threading/index.html#module-threading
