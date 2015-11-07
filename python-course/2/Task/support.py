### Below are the descriptions and headings for the game. Feel free to change the text around to make your own version

body_texts = [
    "Blank", 
    "Welcome to Campus North - this interactive tour should show you all there is to see from this one spot in which we are now stood. As we face west we are confronted with a door which could have been used by King George during his brief tenure - it wasn't, but it could have done!",
    "As we turn the South West we can see some magnificent bookshelves. This lovely example of Victorian woodworking can store up to 16 bottles of water!", 
    "We turn to the south to be confronted with radiator. Legend has it that you can cook a sausage over this radiator, in fact many people in Campus North have tried but, in living memory at least, all have failed.", 
    "The south easterly direction of this spot of Campus North shows use the earliest known cave paintings in Newcastle, many are dotted throughout the building. This one is believed to be a depiction of the artists Mother-In-Law!", 
    "To the east of our fixed position we can see the entrance to the famous mushroom caves. Many budding entrepreneurs wander into the caves to pick mushrooms to garnish their ramen. It is rumoured that some entrepreneurs lurk there for days down there, waiting for their next great idea before resurfacing.", 
    "The north easterly view is one of the dining area. This great hall of food production, while empty at the moment, can feed up to 4000 people in a single day. The cutlery however can only serve 6!", 
    "Facing North we are reminded of the direction from which Campus North takes it's name. An otherwise unremarkable direction, it holds the highest honour on most maps, always pointing towards Campus North.", 
    "Facing north west we can see a tattered parchment loftily stuck to one of the many supporting pillars in Campus North. A wise old man once told me that this parchment could lead to the greatest treasure he had ever known. Sadly, upon inspection it was just the wifi password!"
]

header_texts = [
    'Blank', 
    'West', 
    'South-West', 
    'South', 
    'South-East', 
    'East', 
    'North-East', 
    'North', 
    'North-West'
]

# Helper functions for getting the items out of the arrays
def get_name(index):
    return header_texts[index]

def get_description(index):
    return body_texts[index]