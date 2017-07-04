# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
# -*- coding: utf-8 -*-

from random import randrange
from a0 import a0


class a2(a0):
    """Creatura che sente la posizione del cibo"""

    color = "Orange"
    direction = None
    path_to_food = []


    @property
    def c_type(self):
        return a2


    def build_path_to_food(self, x, y, sz):
        t_x = self.x
        t_y = self.y
        food_position = self.food_callback(x, y, sz)
        if food_position:
            # È stato trovato del cibo vicino
            f_x, f_y = food_position[0]
            if abs(f_x - t_x) == abs(f_y - t_y):
                # il cibo è in diagonale rispetto alla creatura
                if f_x != t_x:
                    for i in range(1, abs(f_x - t_x) + 1):
                        if f_x - t_x > 0:
                            s_x = t_x + i
                        else:
                            s_x = t_x - i
                        if f_y - t_y > 0:
                            s_y = t_y + i
                        else:
                            s_y = t_y - i
                        self.path_to_food.append((s_x, s_y))
                else:
                    s_x = t_x
                    s_y = t_y
                    self.path_to_food.append((s_x, s_y))
                return True
            else:
                # il cibo non è in diagonale
                if f_x != t_x:
                    for i in range(1, abs(f_x - t_x) + 1):
                        if f_x == max(f_x, t_x):
                            tcx = t_x + i
                        else:
                            tcx = t_x - i
                        self.path_to_food.append((tcx, t_y))
                else:
                    tcx = t_x
                for i in range(1, abs(f_y - t_y) + 1):
                    if f_y == max(f_y, t_y):
                        tcy = t_y + i
                    else:
                        tcy = t_y - i
                    self.path_to_food.append((tcx, tcy))
        else:
            return False


    def move(self):
        t_x = self.x
        t_y = self.y
        if (t_x >= 300) or (t_x <= 0) or (t_y >= 300) or (t_y <= 0):
            print("DEBUG: movimento fuori dai confini (" + str(t_x) + "," + str(t_y) + ")")

        if len(self.path_to_food) > 0:
            # il percorso verso il cibo è già impostato
            p_x, p_y = self.path_to_food.pop(0)
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = p_x
            self.y = p_y
            t_x = self.x
            t_y = self.y
            # self.move_callback(self.x, self.y, self.prev_x, self.prev_y, self.tkid)
        elif self.build_path_to_food(self.x, self.y, 3) is True:
            # BUG: IndexError: pop from empty list qui sotto
            p_x, p_y = self.path_to_food.pop(0)
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = p_x
            self.y = p_y
            t_x = self.x
            t_y = self.y
            # self.move_callback(self.x, self.y, self.prev_x, self.prev_y, self.tkid)
        else:
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
