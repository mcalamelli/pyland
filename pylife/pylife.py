# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-
from random import randrange


class Eukaryota:
    """Base creature for pyLife"""
    # 10000 millisecondi
    MAXAGE = 10000
    # 100 cibo
    MAXENERGY = 100
    # ogni 100 tick il cibo cala di una unità (BMR == metabolismo basale)
    BMRTICK = 100
    # ogni 500 tick la creatura si duplica
    DUPTIME = 500
    # se il cibo è minore di 30 non c'è energia per la duplicazione
    MINENERGYFORDUP = 30


    def __init__(self, x, y, check_pos_cb, move_cb, energy=100, bmrtick=100, age=10000):
        self._age = 0  # l'età iniziale è 0
        self._x = x  # la X della posizione iniziale nel mondo
        self._y = y  # la Y della posizione iniziale nel mondo
        self._energy = energy  # partiamo con il pieno di energia
        self._dup = 0 # variabile di controllo della duplicazione
        self.MAXENERGY = energy
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
        # potrebbe essere interessante il lasciare crescere l'energia > MAXENERGY
        if self.energy + x > self.MAXENERGY:
            self.energy = self.MAXENERGY
        else:
            self.energy += x


    def tick(self):
        """
        L'unità di tempo
        """
        self.age += 1  # incremento l'età della creatura
        self._performinternaltasks()


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
        direction = randrange(0, 3, 1)
        if direction == 0:
            self.y -= 1
        elif direction == 1:
            self.x += 1
        elif direction == 2:
            self.y += 1
        elif direction == 3:
            self.x -= 1

        if self.check_position_callback(self.x, self.y) is False:
            #print("can't move to (", self.x, ",", self.y, "): it's busy")
            # la posizione è occupata da una altra creatura oppure da cibo
            # oppure è fuori dai limiti del mondo
            # gestire la situazione
            pass
        else:
            self.move_callback(self.x, self.y)


    def burnfood(self, x=1):
        if self.energy - x <= 0:
            self.energy = 0
        else:
            self.energy -= x


    def my_move_cb(self):
        pass


    def my_pos_cb(self):
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

        self.move()

