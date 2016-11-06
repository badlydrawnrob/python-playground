'''
Classes review | Classes lesson

'''


class Car(object):
    condition = "new"

    def __init__(self, model, color, mpg):
        self.model = model
        self.color = color
        self.mpg = mpg

    def display_car(self):
        print(
            """
            This is a {} {} with {} MPG.
            """.format(self.color, self.model, self.mpg)
        )

    def drive_car(self):
        self.condition = 'used'


class ElectricCar(Car):
    def __init__(self, model, color, mpg, battery_type):
        super(ElectricCar, self).__init__(model, color, mpg)
        self.battery_type = battery_type


my_car = ElectricCar('Volvo', 'black', 102, 'molten salt')
print(my_car.display_car())



class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "(%d, %d, %d)" % (self.x, self.y, self.z)


my_point = Point3D(1, 2, 3)
print(my_point)
