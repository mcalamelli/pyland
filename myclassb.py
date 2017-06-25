# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-
from myclassa import myclassa


class myclassb(myclassa):

    def __init__(self, z=0):
        self._z = z
        super().__init__()

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z
