#
# Indexes: functions
#

## String slices
####################

### 1

animals = "catdogfrog"
cat  = animals[:3]   # The first three characters of animals
dog  = animals[3:6]  # The fourth through sixth characters
frog = animals[6:] # From the seventh character to the end

#### Q: Explain what's happening here.
####    - How we're using [:end] [3:6] (why it's end-1) and [start:] without the end+1



## Search for item, insert item
###############################

animals = ["aardvark", "badger", "duck", "emu", "fennec fox"]
duck_index = animals.index("duck")  # Use index() to find "duck"
animals.insert(duck_index,"cobra")

print animals # Observe what prints after the insert operation

#### Q: Explain what .index() is doing
#### Q: Explain what .insert() does, and at what index we're inserting it
####	e.g: animals.insert(1, "dog")
####	- Note you're not replacing the current string, but **inserting** at that index!
#### Q: Explain what `print animals` will return
####	- It prints out the full list array `[1,2,3,4]` etc
