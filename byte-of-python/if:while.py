number = 23
running = True

while running:
    guess = int(input('Enter an integer: '))
    
    if guess == number:
        print('Congratulations!')
        # you must exit the while loop
        running = False
    elif guess < number:
        print('It\'s a little higher than that.')
    else:
        print('It is a little lower than that.')
else:
    print('The while loop is dunzo.')
    
# This will only execute after
# the while/if statement is complete
print('Done')
