def maximum(x, y):
    if x > y:
        return x
    elif x == y:
        return 'The numbers are equal'
    else:
        return y
    
print(maximum(2, 3))


# An empty block of statements
def some_function():
    pass


# really you should use this ...
print(max(2, 3))