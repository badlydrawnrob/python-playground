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