# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-


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
    # variabile per segnalare la duplicazione
    DUP = 0


    def __init__(self, x, y):
        self._age = 0  # l'età iniziale è 0
        self._x = x  # la X della posizione iniziale nel mondo
        self._y = y  # la Y della posizione iniziale nel mondo
        self._energy = self.MAXENERGY  # partiamo con il pieno di energia


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
        self.age = x


    def eat(self, x):
        # potrebbe essere interessante il lasciare crescere l'energia > MAXENERGY
        if self._energy + x > self.MAXENERGY:
            self._energy = self.MAXENERGY
        else:
            self._energy += x


    def tick(self):
        self._age += 1  # incremento l'età della creatura
        self._performinternaltasks()


    def isdead(self):
        return (self._energy == 0) | (self._age > self.MAXAGE)


    def dupok(self):
        self.DUP = 0


    def _performinternaltasks(self):
        # controllo se l'età è multipla di 10 per consumare in ogni caso
        if self._age % self.BMRTICK == 0:
            self.burnfood()

        # controllo se la eta' e' multipla di cinquecento e il cibo disponibile
        # e' maggiore di trenta
        if (self._age % self.DUPTIME == 0) & (self._energy > self.MINENERGYFORDUP):
            # è tempo di duplicarsi!
            # vedere come gestire la cosa.
            # emetto qualcosa che lo segnala al mondo esterno?
            # direi di sì ma c'è da vedere come fare
            self.DUP = 1

    def burnfood(self, x=1):
        if self.energy - x <= 0:
            self.energy = 0
        else:
            self.energy -= x

