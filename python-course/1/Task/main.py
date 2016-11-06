from __future__ import print_function
#!= from builtins import input

from page1 import Page1
from page2 import Page2
from page3 import Page3
from page4 import Page4

aryRooms = []
curRoom = 0

def main():
    quit = False
    while quit == False:
        room = aryRooms[curRoom]
        print(room.get_title())
        print(room.get_description())

        next_key = raw_input("What would you like to do?")
        if next_key.lower() == "q":
            quit = True
        elif next_key.lower() == 'l':
            curRoom += 1
            if curRoom > len(aryRooms) -1:
                curRoom = 0

# != Convention lookup
if __name__ == "__main__":
    # Setup code
    aryRooms.append(Page1())
    aryRooms.append(Page2())
    aryRooms.append(Page3())
    aryRooms.append(Page4())

    # Main loop
    main()
