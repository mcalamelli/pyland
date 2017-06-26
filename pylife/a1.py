# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
# -*- coding: utf-8 -*-

from random import randrange
from a0 import a0


class a1(a0):
    """Creatura che si muove in diagonale"""

    color = "LawnGreen"
    direction = None


    @property
    def c_type(self):
        return a1

    def move(self):
        t_x = self.x
        t_y = self.y

        if self.direction is None:
            self.direction = randrange(0, 4, 1) # 0:NE 1:NO 2:SO 3:SE
        if self.direction == 0:
            t_x -= 1
            t_y -= 1
        elif self.direction == 1:
            t_x += 1
            t_y -= 1
        elif self.direction == 2:
            t_x += 1
            t_y += 1
        elif self.direction == 3:
            t_x -= 1
            t_y += 1

        pos_status = self.pos_callback(t_x, t_y)
        if pos_status[0] == -2:
            # la posizione è fuori dai confini del mondo
            # gestire la situazione
            mx, my = pos_status[1]
            if t_x <= 0:
                if self.direction == 3:
                    self.direction = 2
                elif self.direction == 0:
                    self.direction = 1
            elif t_x >= mx - 1:
                if self.direction == 2:
                    self.direction = 3
                elif self.direction == 1:
                    self.direction = 0
            elif t_y <= 0:
                if self.direction == 1:
                    self.direction = 2
                elif self.direction == 0:
                    self.direction = 3
            elif t_y >= my - 1:
                if self.direction == 2:
                    self.direction = 1
                elif self.direction == 3:
                    self.direction = 0
        elif pos_status[0] == -1:
            # la posizione è occupata da una altra creatura
            # gestire la situazione
            self.direction = None
        elif pos_status[0] == 0:
            # la posizione è occupata da cibo
            # la considero come valida, mangio il cibo e ci vado
            self.eat(30) # considero una unità di cibo = 30 punti energia
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = t_x
            self.y = t_y
            self.move_callback(self.x, self.y, self.prev_x, self.prev_y, self.tkid)
        elif pos_status[0] == 1:
            # la posizione è occupata da una creatura morta
            # la considero come valida, mangio il cibo e ci vado
            self.eat(15) # considero una creatura morta = 15 punti energia
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = t_x
            self.y = t_y
            self.move_callback(self.x, self.y, self.prev_x, self.prev_y, self.tkid)
        else:
            # la posizione è vuota, ci vado
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = t_x
            self.y = t_y
            self.move_callback(self.x, self.y, self.prev_x, self.prev_y, self.tkid)
