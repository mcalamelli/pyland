# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-

class myclassa:

    def __init__(self, x=0):
        self._myattrx = x


    @property
    def myattrx(self):
        return self._myattrx


    @myattrx.setter
    def myattrx(self, x):
        self._myattrx = x
