# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-

from myclass import myclass

mc1 = myclass(5)

# print("mc1.globvar: ", mc1.__hidglobvar)
# ^-- AttributeError: 'myclass' object has no attribute '__hidglobvar'
print("mc1.myattr: ", mc1.myattr)
mc1.myattr = 10
print("mc1.myattr: ", mc1.myattr)
