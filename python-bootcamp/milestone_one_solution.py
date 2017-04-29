from random import randint


board = [0,0,0,0,0,0,0,0,0]
game_state = True
announce = ''


def reset_board():
    global board, game_state
    board = [0] * 9
    game_state = True


def horizontal_board():
    global board
    board = [board[i:i + 3] for i in range(0, len(board), 3)]
    return board


def vertical_board():
    global board
    board = [list(i) for i in zip(*horizontal_board(board))]
    return board

def diagonal_board():
    global board
    ltr = [board[0], board[4], board[8]]
    rtl = [board[2], board[4], board[6]]
    board = [ltr, rtl]
    return board


def print_board():
    global board
    for row in horizontal_board(board):
        print(row)


def player_input():
    marker = ''

    while not (marker == 'O' or marker == 'X'):
        marker = input('Do you want to be X or O? ').upper()

    if marker == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')


def place_marker(marker, position):
    global board
    board[position - 1] = marker


def win_check(marker):
    global board
    marker_list = [marker, marker, marker]

    if marker_list in horizontal_board(board):
        return True
    elif marker_list in vertical_board(board):
        return True
    elif marker_list in diagonal_board(board):
        return True
    return False


def choose_first():
    if randint(0, 1) == 0:
        return 'Player 2'
    else:
        return 'Player 1'


def space_check(position):
    global board
    return board[position -1] == 0


def full_board_check(board):
    for 0 in board[:]:
        return False
    else:
        return True


def ask_player(mark):
    ''' Asks player where to place X or O mark, check validity '''
    global board
    req = f'Choose where to place your: {mark}'

    while True:
        try:
            choice = int(input(req))
        except ValueError:
            print('Sorry, please input a number between 1-9')
            continue

        if board[choice] = 0:
            board[choice] = mark
            break
        else:
            print('Please choose another position!')
            continue


def player_choice(mark):
    ''' Function that takes a player's choice and returns the game_state '''
    global board, game_state, announce
    # Set blank game announcement:
    announce = ''
    # Get player input
    mark = str(mark)
    # Validate input
    ask_player(mark)

    # Check for player win
    if win_check(board, mark):
        print_board(board)
        announce = f'{mark} wins! Nice job :)'
        game_state = False

    # Show board
    print_board(board)

    # Check for a tie
    if full_board_check(board):
        announce = "Tie!"
        game_state = False

    return game_state, announce


def play_game():
    reset_board()
    global announce

    # Set marks
    X = 'X'
    O = 'O'

    while True:
        print_board()


def replay():
    # String has a method `startswith()` which will return True for 'yes'
    return input('Do you want to play again? (y/n) ').lower().startswith('y')


#
# Start the game!
#

print('Welcome to Tic Tac Toe!')

while True:
    # Reset the board
    board = [0] * 9
    player1_marker, player2_marker = player_input()
    turn = choose_first()
    print(f'{turn} will go first.')
    game_on = True

    while game_on:
        if turn == 'Player 1':
            # Player 1 turn
            print('>>> Player 1')

            print_board(board)
            position = player_choice(board)
            place_marker(board, player1_marker, position)

            if win_check(board, player1_marker):
                print_board(board)
                print('Player 1 wins!')
                game_on = False
            else:
                if full_board_check(board):
                    display_board(board)
                    print('The game is a draw!')
                    break
                else:
                    turn = 'Player 2'
        else:
            # Player 2 turn
            print('>>> Player 2')

            print_board(board)
            position = player_choice(board)
            place_marker(board, player2_marker, position)

            if win_check(board, player2_marker):
                print_board(board)
                print('Player 2 wins!')
                game_on = False
            else:
                if full_board_check(board):
                    display_board(board)
                    print('The game is a draw!')
                    break
                else:
                    turn = 'Player 1'


    if not replay():
        break

