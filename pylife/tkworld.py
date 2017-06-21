# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long

from random import randint
import json
import argparse
import tkinter
import tkinter.messagebox
from a0 import a0
from a1 import a1

c_type = None

def checkplace(x, y):
    if (x >= XSIZE - 1) or (y >= YSIZE - 1) or (x <= 0) or (y <= 0):
        # fuori dai confini del mondo, non valida
        #drawpoint(x, y, "red")
        return (-2, (XSIZE, YSIZE))
    elif places[x][y] == 1:
        # posizione già occupata, non valida
        #drawpoint(x, y, "red")
        return (-1, (None, None))
    elif places[x][y] == 9:
        # posizione occupata da cibo, valida
        return (0, (None, None))
    elif places[x][y] == 8:
        # posizione occupata da cibo, valida
        return (1, (None, None))
    else:
        # posizione libera
        return (2, (None, None))


def addfood(x, y):
    if checkplace(x, y):
        places[x][y] = 9
        food = drawpoint(x, y, "DimGrey")
        tc.itemconfig(food, tags=(str(x) + "x" + str(y)))
        return True
    else:
        return False


def drawpoint(x, y, color):
    #drw.point((x, y), fill=color)
    return tc.create_oval(x - 2, y - 2, x + 2, y + 2, fill=color)


def move(x, y, prev_x, prev_y, tkid):
    places[prev_x][prev_y] = 0
    if (places[x][y] == 9) or (places[x][y] == 8):
        tc.delete(tc.find_withtag(str(x) + "x" + str(y)))
    places[x][y] = 1
    #drawpoint(prev_x, prev_y, "black")
    #drawpoint(x, y, "DodgerBlue")
    tc.move(tkid, x - prev_x, y - prev_y)


def die(o, tkid):
    places[o.x][o.y] = 8
    body = drawpoint(o.x, o.y, "DimGrey")
    tc.itemconfig(body, tags=(str(o.x) + "x" + str(o.y)))
    creatures.remove(o)
    tc.delete(tkid)
    tc.itemconfigure(c_text, text="Creature: " + str(len(creatures)))


def duplicate(x, y, z):
    t_x = x
    t_y = y
    while not addcreature(t_x, t_y, z): # da sistemare
        t_x, t_y = randint(t_x - 3, t_x + 3), randint(t_y - 3, t_y + 3)


def addcreature(x, y, z):
    if checkplace(x, y):
        places[x][y] = 1
        #if not x % 2 == 0:
        #    c = a0(x, y, checkplace, move, die, duplicate, **creature_data["creature"][0])
        #else:
        #    c = a1(x, y, checkplace, move, die, duplicate, **creature_data["creature"][0])
        c = z(x, y, checkplace, move, die, duplicate, **creature_data["creature"][0])
        creatures.append(c)
        #c.tkid = drawpoint(x, y, "DodgerBlue")
        c.tkid = drawpoint(x, y, c.color)
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
tc.pack(expand=1)
c_text = tc.create_text(10, YSIZE + 15, text="Creature: ", fill="white", anchor="nw")

def do_tick():
    for creature in creatures:
        creature.tick()
    mtk.after(100, do_tick)

creatures = []
places = [[0 for x in range(XSIZE)] for y in range(YSIZE)]

for f_i in range(0, FOOD):
    f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    while not addfood(f_x, f_y):
        f_x, f_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)

for c_i in range(0, CREATURES):
    c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
    if c_x % 2 == 0:
        c_type = a0
    else:
        c_type = a1
    while not addcreature(c_x, c_y, c_type):
        c_x, c_y = randint(0, XSIZE - 1), randint(0, YSIZE - 1)
        if c_x % 2 == 0:
            c_type = a0
        else:
            c_type = a1

mtk.after(100, do_tick)
mtk.mainloop()
