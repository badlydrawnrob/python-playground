#
# Indexes: functions
#

## .append() method
####################

### 1

letters = ['a', 'b', 'c']
letters.append('d')
print len(letters)
print letters

#### Q: What does len() do here
#### Q: What happens to letters list when we .append('d')


### 2

suitcase = [] # What does this do? 
suitcase.append("sunglasses")

# What are we doing here?
suitcase.append("suncream")
suitcase.append("swimming costume")
suitcase.append("book")

list_length = ________ # How do we set the list length?

print "There are %d items in the suitcase." % (list_length)
print suitcase

#### Q: How do you set an empty list (array)
#### Q: How do we set the `list_length`? 
#### Q: What does %d print out?