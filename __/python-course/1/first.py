from __future__ import print_function
from animal import Animal

print(time.time())

aryAnimals = []
aryAnimals.append(Animal())
aryAnimals.append(Animal("Snake", 0, "Dave"))
aryAnimals.append(Animal("Goat", 4, "Billy"))

for a in aryAnimals:
    a.what_kind_of_animal()
    a.how_many_legs()
    a.what_is_your_name()
