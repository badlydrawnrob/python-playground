from random import randint


keys = [1,2,3,4,5,6,7,8,9]
board = [0,0,0,0,0,0,0,0,0]


def horizontal_board(board):
    board = [board[i:i + 3] for i in range(0, len(board), 3)]
    return board


def vertical_board(board):
    board = [list(i) for i in zip(*horizontal_board(board))]
    return board


def print_board(board):
    for row in horizontal_board(board):
        print(row)


def player_input():
    marker = ''

    while not (marker == 'O' or marker == 'X'):
        marker = input('Player 1: Do you want to be X or O? ').upper()

    if marker == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')


def place_marker(board, marker, position):
    board[position - 1] = marker


# != win_check is missing a `mark` argument

def win_check(board):
    board = horizontal_board(board)

    if ['X', 'X', 'X'] in board:
        return True, 'X'
    elif ['O', 'O', 'O'] in board:
        return True, 'O'
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

    while int(position) not in positions_allowed or not space_check(board, int(position)):
        position = input('Choose your next position: (1-9) ')
    return int(position)


# def play_game():
#     player_order = player_input()


# print(play_game())
print(choose_first())
# print(player_choice(board))

print(space_check(board, 1))
print(place_marker(board, 'X', 1))
print(full_board_check(board)) # String causes error
print(win_check(board))

print(space_check(board, 2))
print(place_marker(board, 'X', 2))
print(full_board_check(board)) # String causes error
print(win_check(board))

print(space_check(board, 3))
print(place_marker(board, 'X', 3))
print(full_board_check(board)) # String causes error
print(win_check(board))

new_board = ['X','X','X','X','X','X','X','X','X']
print(horizontal_board(new_board))
print(win_check(new_board))

print(horizontal_board(board))
print(vertical_board(board))