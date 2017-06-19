# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long

from random import randint
import json
import argparse
import tkinter
import tkinter.messagebox
from Eukaryota import Eukaryota


def checkplace(x, y):
    if (x >= XSIZE - 1) or (y >= YSIZE - 1) or (x <= 0) or (y <= 0):
        # fuori dai confini del mondo, non valida
        #drawpoint(x, y, "red")
        return -1
    elif places[x][y] == 1:
        # posizione già occupata, non valida
        #drawpoint(x, y, "red")
        return -1
    elif places[x][y] == 9:
        # posizione occupata da cibo, valida
        return 0
    elif places[x][y] == 8:
        # posizione occupata da cibo, valida
        return 1
    else:
        # posizione libera
        return 2


def addfood(x, y):
    if checkplace(x, y):
        places[x][y] = 9
        drawpoint(x, y, "yellow")
        return True
    else:
        return False


def drawpoint(x, y, color):
    #drw.point((x, y), fill=color)
    return tc.create_oval(x, y, x, y, fill=color)


def move(x, y, prev_x, prev_y, tkid):
    places[prev_x][prev_y] = 0
    places[x][y] = 1
    #drawpoint(prev_x, prev_y, "black")
    #drawpoint(x, y, "DodgerBlue")
    tc.move(tkid, x - prev_x, y - prev_y)


def die(o, tkid):
    places[o.x][o.y] = 8
    drawpoint(o.x, o.y, "DeepPink")
    creatures.remove(o)
    tc.delete(tkid)
    tc.itemconfigure(c_text, text="Creature: " + str(len(creatures)))


def duplicate(x, y):
    t_x = x
    t_y = y
    while not addcreature(t_x, t_y):
        t_x, t_y = randint(t_x - 3, t_x + 3), randint(t_y - 3, t_y + 3)


def addcreature(x, y):
    if checkplace(x, y):
        places[x][y] = 1
        c = Eukaryota(x, y, checkplace, move, die, duplicate, **creature_data["creature"][0])
        creatures.append(c)
        c.tkid = drawpoint(x, y, "DodgerBlue")
        tc.itemconfigure(c_text, text="Creature: " + str(len(creatures)))
        return True
    else:
        return False


parser = argparse.ArgumentParser()
parser.add_argument('--xsize', '-x',
                    type=int, default=300,
                    help="Dimensione x del mondo virtuale")
parser.add_argument('--ysize', '-y',
                    type=int, default=300,
                    help="Dimensione y del mondo virtuale")
parser.add_argument('--creatures', '-c',
                    type=int, default=20,
                    help="Numero di creature esistenti all'inizio")
parser.add_argument('--food', '-f',
                    type=int,
                    help="Quantità di cibo disponibile all'inizio (se non specificato, è uguale al numero delle creature)")
parser.add_argument('--ticks', '-t',
                    type=int, default=100,
                    help="Numero di tick di vita del mondo virtuale")
parser.add_argument('--save', '-s',
                    action="store_true",
                    help="Attiva il salvataggio delle singole immagini")
parser.add_argument('--build', '-b',
                    action="store_true",
                    help="Attiva la creazione della gif animata")
parser.add_argument('--delete', '-d',
                    action="store_true",
                    help="Cancella i file BMP utilizzati per la creazione della gif animata (vale solo epr opzione -b / --build")
parser.add_argument('--inputfile', '-i',
                    type=argparse.FileType('r'),
                    default='default.json',
                    metavar='<inputfile>',
                    help='Specifica il file di inizializzazione delle creature (default: default.json)')
args = parser.parse_args()

XSIZE = args.xsize
YSIZE = args.ysize
CREATURES = args.creatures
if args.food is None:
    FOOD = CREATURES
else:
    FOOD = args.food
TICKS = args.ticks
creature_data = json.load(args.inputfile)

mtk = tkinter.Tk()
tc = tkinter.Canvas(mtk, bg="black", width=XSIZE, height=YSIZE + 30)
tc.pack()
c_text = tc.create_text(10, YSIZE + 15, text="Creature: ", fill="white", anchor="nw")

def do_tick():
    for creature in creatures:
        creature.tick()
    mtk.after(10, do_tick)

creatures = []
places = [[0 for x in range(XSIZE)] for y in range(YSIZE)]

for f_i in range(0, FOOD):
    f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addfood(f_x, f_y):
        f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)

for c_i in range(0, CREATURES):
    c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addcreature(c_x, c_y):
        c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)

mtk.after(10, do_tick)
mtk.mainloop()
