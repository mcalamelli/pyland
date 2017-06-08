# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
# -*- coding: utf-8 -*-
from random import randrange


class Eukaryota:
    """Base creature for pyLife"""
    # L'età massima di una creatura (10000 tick)
    MAXAGE = 10000

    # L'energia di partenza di una creatura
    #STARTENERGY = 100

    # ogni 100 tick l'energia cala di una unità (BMR == metabolismo basale)
    BMRTICK = 100
    # ogni 200 tick la creatura si duplica
    DUPTIME = 400
    # se l'energia è minore di 30 non c'è la duplicazione
    MINENERGYFORDUP = 30


    def __init__(self, x, y, check_pos_cb, move_cb, die_cb, duplicate_cb, energy=100, bmrtick=100, age=10000):
        self._age = 0  # l'età iniziale è 0
        self._x = x  # la X della posizione iniziale nel mondo
        self._prev_x = x  # la X della posizione precedente
        self._y = y  # la Y della posizione iniziale nel mondo
        self._prev_y = y  # la Y della posizione precedente
        self._energy = energy  # partiamo con il pieno di energia
        self._dup = 0 # variabile di controllo della duplicazione
        #self.STARTENERGY = energy
        self.BMRTICK = bmrtick
        self.MAXAGE = age

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
    def prev_x(self):
        """
        Imposta oppure ottiene il valore di posizione x precedente
        """
        return self._prev_x

    @prev_x.setter
    def prev_x(self, x):
        self._prev_x = x

    @property
    def prev_y(self):
        """
        Imposta oppure ottiene il valore di posizione y precedente
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
        Imposta oppure ottiene il valore di posizione x
        """
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        """
        Imposta oppure ottiene il valore di posizione y
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
        # potrebbe essere interessante il lasciare crescere l'energia > STARTENERGY
        # if self.energy + x > self.STARTENERGY:
        #    self.energy = self.STARTENERGY
        #else:
        #    self.energy += x
        self.energy += x


    def tick(self):
        """
        L'unità di tempo
        """
        if self.isdead() is False:
            self.age += 1  # incremento l'età della creatura
            self._performinternaltasks()
        else:
            self.die_callback(self)


    def isdead(self):
        """
        Ritorna True se è finita l'energia oppure se si
        è raggiunta l'età massima
        """
        return (self.energy == 0) | (self.age > self.MAXAGE)


    def dupok(self):
        """
        Resetta la variabile di controllo della duplicazione
        (duplicazione avvenuta)
        """
        self.dup = 0


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
            #print("can't move to (", self.x, ",", self.y, "): it's busy")
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
            self.move_callback(self.x, self.y, self.prev_x, self.prev_y)
        else:
            # la posizione è vuota, ci vado
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = t_x
            self.y = t_y
            self.move_callback(self.x, self.y, self.prev_x, self.prev_y)


    def burnfood(self, x=1):
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
        # controllo se l'età è multipla di 10 per consumare in ogni caso
        if self.age % self.BMRTICK == 0:
            d = self.age // self.BMRTICK
            self.burnfood(1 + (1 * d))
            # 1 + (1 * d): l'energia viene scalata in quantità crescente
            # in funzione delle volte in cui l'organismo si è duplicato

        # controllo se la eta' e' multipla di self.DUPTIME e il cibo disponibile
        # e' maggiore di self.MINENERGYFORDUP
        if (self.age % self.DUPTIME == 0) & (self.energy > self.MINENERGYFORDUP):
            # è tempo di duplicarsi!
            # vedere come gestire la cosa.
            # emetto qualcosa che lo segnala al mondo esterno?
            # direi di sì ma c'è da vedere come fare
            self.dup = 1
            self.burnfood(15)  # tolgo 15 punti di energia alla duplicazione
            self.duplicate_callback(self.x, self.y)
            # print("Duplicate @" + str(self.age) + " tick.")

        self.move()
