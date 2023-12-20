# Address book
ab = { 'Swaroop' : 'swaroop@swaaroopch.com',
       'Larry'   : 'larry@wall.org',
       'Matsumo' : 'matz@ruby-lang.org',
       'Spammer' : 'spammer@hotmail.com' }

print("Swaroop's address is", ab['Swaroop'])

# Remove
print('removed', ab.pop('Spammer'))

# loop through the address book
for name, address in ab.items():
    print('Contact {} at {}'.format(name, address))
    

print('There are {} contacts'.format(len(ab)))

# Adding a key-value pair
ab['Guido'] = 'guido@python.org'

if 'Guido' in ab:
    print("\nGuido's address is", ab['Guido'])