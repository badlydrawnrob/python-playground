from random import randint


keys = [1,2,3,4,5,6,7,8,9]
board = [0,0,0,0,0,0,0,0,0]


def horizontal_board(board):
    board = [board[i:i + 3] for i in range(0, len(board), 3)]
    return board


def vertical_board(board):
    board = [list(i) for i in zip(*horizontal_board(board))]
    return board

def diagonal_board(board):
    ltr = [board[0], board[4], board[8]]
    rtl = [board[2], board[4], board[6]]
    board = [ltr, rtl]
    return board


def print_board(board):
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


def place_marker(board, marker, position):
    board[position - 1] = marker


def win_check(board, marker):
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


def space_check(board, position):
    return board[position -1] == 0


def full_board_check(board):
    # We don't loop through the board itself,
    # but use range() and our space_check()
    # function, passing the index of i

    for i in range(9):
        if space_check(board, i):
            return False
    return True


def player_choice(board):
    # Assign variable before conditional checks
    position = 0
    positions_allowed = [str(n) for n in range(1,10)]

    while position not in positions_allowed or not space_check(board, int(position)):
        position = input('Choose your next position: (1-9) ')
    return int(position)


def replay():
    return input('Do you want to play again? (y/n) ')


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

