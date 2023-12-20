# Continue skips the rest of statements

while True:
    s = input('Enter something: ')
    if s == 'quit':
        break
    if len(s) < 3:
        print('Too small')
        continue
    print('Input is big enough')
    # other kinds of processing here
    for i in s:
        print(s)