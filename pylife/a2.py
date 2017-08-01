# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
# -*- coding: utf-8 -*-

# from random import randrange
# from a0 import a0
from a1 import a1


class a2(a1):
    """Creatura che sente la posizione del cibo"""

    color = "Orange"
    dup_color = "Lime" # dup_color = "Coral"
    direction = None
    path_to_food = []


    @property
    def c_type(self):
        return a2


    # def build_path_to_food(self, x, y, sz):
    def build_path_to_food(self, sz):
        t_x = self.x
        t_y = self.y

        food_position = self.food_callback(t_x, t_y, sz)
        # return False # TODO: return messo qui per debug
        if food_position is not False:
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
            # else:
            #     # il cibo non è in diagonale
            #     if f_x != t_x:
            #         for i in range(1, abs(f_x - t_x) + 1):
            #             if f_x == max(f_x, t_x):
            #                 tcx = t_x + i
            #             else:
            #                 tcx = t_x - i
            #             self.path_to_food.append((tcx, t_y))
            #     else:
            #         tcx = t_x
            #     for i in range(1, abs(f_y - t_y) + 1):
            #         if f_y == max(f_y, t_y):
            #             tcy = t_y + i
            #         else:
            #             tcy = t_y - i
            #         self.path_to_food.append((tcx, tcy))
            #     return True
        else:
            return False


    def move(self):
        t_x = self.x
        t_y = self.y

        if len(self.path_to_food) > 0:
            # self.color_callback(self.tkid, "DeepPink") # TODO: da rimettere
            # il percorso verso il cibo è già impostato
            p_x, p_y = self.path_to_food.pop(0)
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = p_x
            self.y = p_y
            # t_x = self.x
            # t_y = self.y
        else:
            # self.color_callback(self.tkid, self.color) # TODO: da rimettere
            self.build_path_to_food(3)

        t_x, t_y = self.get_position_from_direction()

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

            t_x, t_y = self.get_position_from_direction()
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = t_x
            self.y = t_y
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
        elif pos_status[0] == 1:
            # la posizione è occupata da una creatura morta
            # la considero come valida, mangio il cibo e ci vado
            self.eat(15) # considero una creatura morta = 15 punti energia
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = t_x
            self.y = t_y
        else:
            # la posizione è vuota, ci vado
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = t_x
            self.y = t_y

        self.move_callback(self.x, self.y, self.prev_x, self.prev_y, self.tkid)
