# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
# -*- coding: utf-8 -*-

from random import randrange
from a0 import a0


class a1(a0):
    """Creatura che si muove in diagonale"""

    color = "LawnGreen"
    direction = None

    def move(self):
        t_x = self.x
        t_y = self.y

        if self.direction is None:
            self.direction = randrange(0, 4, 1)
            # 0:NE 1:NO 2:SO 3:SE
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

        pos_status = self.check_position_callback(t_x, t_y)
        if pos_status == -1:
            # la posizione è occupata da una altra creatura oppure è fuori
            # dai limiti del mondo - gestire la situazione
            pass
        elif pos_status == 0:
            # la posizione è occupata da cibo
            # la considero come valida, mangio il cibo e ci vado
            self.eat(30) # considero una unità di cibo = 30 punti energia
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = t_x
            self.y = t_y
            self.move_callback(self.x, self.y, self.prev_x, self.prev_y, self.tkid)
        elif pos_status == 1:
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
