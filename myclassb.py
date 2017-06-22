# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-
from myclassa import myclassa

class myclassb(myclassa):

    def __init__(self, y=0):
        self._myattry = y
        super().__init__()


    @property
    def myattry(self):
        return self._myattry


    @myattry.setter
    def myattry(self, y):
        self._myattry = y
