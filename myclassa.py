# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-


class myclassa:

    def __init__(self, x=0, y=0, cb=None):
        self._x = x
        self._y = y
        self.cb = cb

        if self.cb is None:
            self.cb = self.my_cb

    def my_cb(self):
        return "Local dummy callback."

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
