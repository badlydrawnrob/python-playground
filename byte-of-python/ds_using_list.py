# a shopping list
shoplist = ['apple', 'mango', 'carrot', 'bananna']

print('I have', len(shoplist), 'items to buy')

print('These items are:',)

for i in shoplist:
    print('-', i)
        
print('I also need rice')
shoplist.append('rice')

print('my shoplist is now ...', shoplist)

# sort the list
print('a sorted list', shoplist.sort())

# grab the first item
olditem = shoplist[0]
# and remove it
shoplist.remove('apple')

print('I bought', olditem, 'now the list is', shoplist)