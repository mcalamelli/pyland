# -*- coding: utf-8 -*-


class Eukaryota:
    """Base creature for pyLife"""
    # 10000 millisecondi
    MAXAGE = 10000
    # 100 cibo
    MAXFOOD = 100

    # ogni 100 tick il cibo cala di una unità (BMR == metabolismo basale)
    BMRTICK = 100

    # ogni 500 tick la creatura si duplica
    DUPTIME = 500
    # se il cibo è minore di 30 non c'è energia per la duplicazione
    MINFOODFORDUP = 30
    # variabile per segnalare la duplicazione
    DUP = 0

    def __init__(self, x, y):
        self.age = 0  # l'età iniziale è 0

        self.posX = x  # la X della posizione iniziale nel mondo
        self.posY = y  # la Y della posizione iniziale nel mondo

        self.food = self.MAXFOOD  # partiamo con il pieno di energia

    def eat(self, foodqty):
        # potrebbe essere interessante il lasciare crescere l'energia > MAXFOOD
        if self.food + foodqty > 100:
            self.food = self.MAXFOOD
        else:
            self.food += foodqty

    def dotick(self):
        self.age += 1  # incremento l'età della creatura
        self._performinternaltasks(self)

    def isdead(self):
        return (self.food == 0) | (self.age > self.MAXAGE)

    def dupok(self):
        self.DUP = 0

    @staticmethod
    def _performinternaltasks(self):
        # controllo se l'età è multipla di 10 per consumare in ogni caso
        if self.age % self.BMRTICK == 0:
            self._burnfood(self)

        # controllo se la eta' e' multipla di cinquecento e il cibo disponibile
        # e' maggiore di trenta
        if (self.age % self.DUPTIME == 0) & (self.food > self.MINFOODFORDUP):
            # è tempo di duplicarsi!
            # vedere come gestire la cosa.
            # emetto qualcosa che lo segnala al mondo esterno?
            # direi di sì ma c'è da vedere come fare
            self._dup(self)

    @staticmethod
    def _burnfood(self, x=1):
        if self.food - x <= 0:
            self.food = 0
        else:
            self.food -= x

    @staticmethod
    def _dup(self):
        self.DUP = 1
