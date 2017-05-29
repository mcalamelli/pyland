# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-

class myclass:

    def __init__(self, x=0):
        self._myattr = x


    @property
    def myattr(self):
        return self._myattr


    @myattr.setter
    def myattr(self, x):
        self._myattr = x
