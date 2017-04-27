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
        marker = input('Player 1: Do you want to be X or O? ')

    if marker == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')


def mark_board(board, marker, position):
    board[position - 1] = marker
    return board


def check_board(board):
    winner = None

    for row in horizontal_board(board):
        if ['X', 'X', 'X'] in row:
            winner = ('X', 'O')
        elif ['O', 'O', 'O'] in row:
            winner = ('X', 'O')

    if winner == ('X', 'O') or winner == ('O', 'X'):
        return winner
    else:
        return False

    print(horizontal_board)
    print(vertical_board)


def space_check(board, position):
    return board[position -1] == 0


def full_board_check(board):
    for i in board:
        if isinstance(i, int) and space_check(board, i):
            return False
        elif 'X' or 'O':
            print(i)
            return False
    return True


def play_game():
    player_order = player_input()


# print(play_game())
print(space_check(board, 1))
print(mark_board(board, 'X', 1))
print(full_board_check(board)) # String causes error
print(check_board(board))

print(space_check(board, 2))
print(mark_board(board, 'X', 2))
print(full_board_check(board)) # String causes error
print(check_board(board))

print(horizontal_board(board))
print(vertical_board(board))
