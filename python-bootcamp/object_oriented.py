## A basic object

class Circle(object):
    pi = 3.14

    def __init__(self, radius=1):
        self.radius = radius

    def area(self):
        return self.radius * self.radius * self.pi

    def setRadius(self, radius):
        self.radius = radius

    def getRadius(self):
        return self.radius


c = Circle()

c.setRadius(2)
print('Radius is: {}'.format(c.getRadius()))
print('Area is: {}'.format(c.area()))



## An inherited object

class Animal(object):
    def __init__(self):
        print("Animal created")

    def whoAmI(self):
        print("Animal")

    def eat(self):
        print("Eating")


class Dog(Animal):
    def __init__(self):
        Animal.__init__(self)
        print("Dog created")

    def whoAmI(self):
        print("Dog")

    def bark(self):
        print("Woof!")


d = Dog()
print(d.whoAmI(), d.bark())


## Special methods

class Book(object):
    def __init__(self, title, author, pages):
        print("A book is created")
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f'Title: {self.title}, author: {self.author}, pages: {self.pages}'

    def __len__(self):
        return self.pages

    def __del__(self):
        print("A book is destroyed")


book = Book("Python rocks!", "Jose Portilla", 159)
print(book)
print(len(book))
del(book)