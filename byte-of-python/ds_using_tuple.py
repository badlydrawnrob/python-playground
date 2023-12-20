# I would recommend always using parentheses
# to indicate start and end of tuple

zoo = ('python', 'elephant', 'penguin')
print('number of animals in the zoo is ..', len(zoo))

new_zoo = 'monkey', 'camel', zoo
print('Number of cages in the new zoo is', len(new_zoo))
print('All animals in the new zoo are', new_zoo)
print('Animals brought from the old zoo are', new_zoo[2])
print('Last animal brought from old zoo is', new_zoo[2][2])
print('Number of animals in the new zoo is', \
      len(new_zoo)-1+len(new_zoo[2]))