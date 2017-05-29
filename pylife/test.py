# pylint: disable=locally-disabled,missing-docstring,invalid-name

from pylife import Eukaryota

e = Eukaryota(10, 10)

print("Is it dead? ", e.isdead())
print("Food?", e.energy)
print("Burn out now!")
e.burnfood()
print("Food?", e.energy)
for i in range(0, 100):
    e.tick()
print("100 tick in a row!")
print("Food?", e.energy)
for i in range(1, 510):
    e.tick()
    print("[", i, "] [", e.energy, "]", e.DUP)
