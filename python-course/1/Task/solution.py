    quit = False
    cur_room = 0
    
    while quit is False:
        print('')
        print(aryRooms[cur_room].get_title())
        print(aryRooms[cur_room].get_description())
        
        input = raw_input('L to turn left, R to turn right and Q to quit: ')
        if input == 'Q' or input == 'q':
            print('Goodbye')
            quit = True
        elif input == 'L' or input == 'l':
            cur_room += 1
            if cur_room > 3:
                cur_room = 0
        elif input == 'R' or input == 'r':
            cur_room -= 1
            if cur_room < 0:
                cur_room = 3
                
                
                
    aryRooms.append(Page1())
    aryRooms.append(Page2())
    aryRooms.append(Page3())
    aryRooms.append(Page4())