# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-

from myclassa import myclassa
from myclassb import myclassb

mc1 = myclassa(5)
mc2 = myclassb(2)

# print("mc1.globvar: ", mc1.__hidglobvar)
# ^-- AttributeError: 'myclass' object has no attribute '__hidglobvar'
print("mc1.myattrx: ", mc1.myattrx)
mc1.myattrx = 10
print("mc1.myattrx: ", mc1.myattrx)
print("mc2.myattrx: ", mc2.myattrx)
print("mc2.myattry: ", mc2.myattry)
mc2.myattrx = 7
print("mc2.myattrx: ", mc2.myattrx)
print("mc2.myattry: ", mc2.myattry)
