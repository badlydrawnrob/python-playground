'''
Classes | Introduction to classes

'''


# class Animal(object):
#     """Makes cute animals."""
#     is_alive = True

#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def description(self):
#         print(
#             '''
#             name: {} \n
#             age:  {}
#             '''.format(self.name, self.age)
#         )


# zebra = Animal("Jeffrey", 2)
# print(zebra.name, zebra.age, zebra.is_alive)
# zebra.description()


class Employee(object):
    """Models real-life employees!"""
    def __init__(self, employee_name):
        self.employee_name = employee_name

    def calculate_wage(self, hours):
        self.hours = hours
        return hours * 20.00


class PartTimeEmployee(Employee):
    """Overrides Employee!"""
    def calculate_wage(self, hours):
        self.hours = hours
        return hours * 12.00


print(PartTimeEmployee('Jeff').calculate_wage(10))
