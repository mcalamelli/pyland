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
    obj.tick()
print("100 tick in a row!")
print("Food?", obj.food)
for i in range(1, 510):
    obj.tick()
    print("[", i, "] [", obj.food, "]", obj.DUP)
