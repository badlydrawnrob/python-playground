from __future__ import print_function

class Animal(object):
    def __init__(self, typeofanimal="dog", legs=0, name="unknown"):
        self.animaltype = typeofanimal
        self.legs = legs
        self.name = name

    def what_kind_of_animal(self):
        print("I am a " + self.animaltype)

    def how_many_legs(self):
        print("I have " + str(self.legs) + " legs")

    def what_is_your_name(self):
        print("My name is " + self.name)
