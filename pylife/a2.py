# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
# -*- coding: utf-8 -*-

#from random import randrange
from a0 import a0


class a2(a0):
    """Creatura che sente la posizione del cibo"""

    color = "OrangeRed"
    direction = None


    @property
    def c_type(self):
        return a2

    def move(self):
        pass
