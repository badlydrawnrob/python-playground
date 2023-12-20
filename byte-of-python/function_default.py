# default value of an argument
# must be at end of params list

def say(message, times=1):
    print(message * times)

say('Hello')
say('World', 5)


# using keyword arguments

def func(a, b=5, c=10):
    print('a is', a, ', b is', b, 'c is', c)
    
func(3, 7)
func(25, c=24)
func(c=50, a=100)