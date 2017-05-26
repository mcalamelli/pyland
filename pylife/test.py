# pylint: disable=locally-disabled,missing-docstring,invalid-name

import pylife

obj = pylife.Eukaryota(10, 10)

print("Is it dead? ", obj.isdead())
print("Food?", obj.food)
print("Burn out now!")
#obj._burnfood(obj)
obj._bf(obj)
print("Food?", obj.food)
for i in range(0, 100):
    obj.dotick()
print("100 tick in a row!")
print("Food?", obj.food)
for i in range(1, 510):
    obj.dotick()
    print("[", i, "] [", obj.food, "]", obj.DUP)
