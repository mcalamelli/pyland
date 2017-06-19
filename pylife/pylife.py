# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
# -*- coding: utf-8 -*-
from random import randrange


class Eukaryota():
    """Base creature for pyLife"""


    def __init__(self, x, y,
                 check_pos_cb, move_cb, die_cb, duplicate_cb,
                 energy, bmrtick, age, minenergyfordup, duptime):
        self._age = 0  # l'età iniziale è 0
        self._x = x  # la X della posizione iniziale nel mondo
        self._prev_x = x  # la X della posizione precedente
        self._y = y  # la Y della posizione iniziale nel mondo
        self._prev_y = y  # la Y della posizione precedente
        self._energy = energy  # partiamo con il pieno di energia
        self._dup = 0 # variabile di controllo della duplicazione
        self.BMRTICK = bmrtick
        self.MAXAGE = age
        self.MINENERGYFORDUP = minenergyfordup
        self.DUPTIME = duptime
        self._tkid = None

        if check_pos_cb is None:
            self.check_position_callback = self.my_pos_cb
        else:
            self.check_position_callback = check_pos_cb
        if move_cb is None:
            self.move_callback = self.my_move_cb
        else:
            self.move_callback = move_cb
        if die_cb is None:
            self.die_callback = self.my_die_cb
        else:
            self.die_callback = die_cb
        if duplicate_cb is None:
            self.duplicate_callback = self.my_duplicate_cb
        else:
            self.duplicate_callback = duplicate_cb


    @property
    def tkid(self):
        """
        Imposta oppure ottiene l'ID Tk
        """
        return self._tkid

    @tkid.setter
    def tkid(self, x):
        self._tkid = x

    @property
    def prev_x(self):
        """
        Imposta oppure ottiene il valore della posizione x precedente
        """
        return self._prev_x

    @prev_x.setter
    def prev_x(self, x):
        self._prev_x = x

    @property
    def prev_y(self):
        """
        Imposta oppure ottiene il valore della posizione y precedente
        """
        return self._prev_y

    @prev_y.setter
    def prev_y(self, y):
        self._prev_y = y

    @property
    def dup(self):
        """
        Imposta oppure ottiene la variabile di duplicazione
        """
        return self._dup

    @dup.setter
    def dup(self, x):
        self._dup = x

    @property
    def x(self):
        """
        Imposta oppure ottiene il valore della posizione x
        """
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        """
        Imposta oppure ottiene il valore della posizione y
        """
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def energy(self):
        """
        Imposta oppure ottiene il valore corrente di energia
        """
        return self._energy

    @energy.setter
    def energy(self, x):
        self._energy = x

    @property
    def age(self):
        """
        Imposta oppure ottiene il valore corrente di età
        """
        return self._age

    @age.setter
    def age(self, x):
        self._age = x


    def eat(self, x):
        self.energy += x


    def tick(self):
        """
        L'unità di tempo
        """
        if self.isdead() is False:
            self.age += 1  # incremento l'età della creatura
            self._performinternaltasks()
        else:
            self.die_callback(self, self.tkid)


    def isdead(self):
        """
        Ritorna True se è finita l'energia oppure se si
        è raggiunta l'età massima
        """
        return (self.energy == 0) | (self.age > self.MAXAGE)


    def move(self):
        """
        Muove l'entità nella direzione specificata
        direction: 0 -> N, 1 -> E, 2 -> S, 3 -> O
        direction è generata casualmente tra 0 e 3
        """
        t_x = self.x
        t_y = self.y

        direction = randrange(0, 4, 1)
        if direction == 0:
            t_y -= 1
        elif direction == 1:
            t_x += 1
        elif direction == 2:
            t_y += 1
        elif direction == 3:
            t_x -= 1

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


    def burnenergy(self, x=1):
        if self.energy - x <= 0:
            self.energy = 0
        else:
            self.energy -= x


    def my_move_cb(self):
        pass

    def my_pos_cb(self):
        pass

    def my_die_cb(self):
        pass

    def my_duplicate_cb(self):
        pass

    def _performinternaltasks(self):
        # controllo se l'età è multipla di BMRTICK per consumare in ogni caso
        if self.age % self.BMRTICK == 0:
            #d = self.age // self.DUPTIME
            #to_burn = 1 + (1 * d)
            # 1 + (1 * d): l'energia viene scalata in quantità crescente
            to_burn = 1
            if (self.age % self.DUPTIME == 0) & (self.energy > self.MINENERGYFORDUP):
                # controllo se la eta' e' multipla di self.DUPTIME e il cibo disponibile
                # e' maggiore di self.MINENERGYFORDUP
                to_burn += 15
                self.duplicate_callback(self.x, self.y)
                self.dup = 1
            self.burnenergy(to_burn)

        self.move()
