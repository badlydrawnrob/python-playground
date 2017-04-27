list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

def plot_board(board):
    board = [board[i:i + 3] for i in range(0, len(board), 3)]
    return board

def print_board(board):
    for row in plot_board(board):
        print(row)

def mark_board(player, position):
    global board
    board[int(position) -1] = player

    return print_board(board)

def check_winner(board):
    for row in board:
        if row == ['x', 'x', 'x']:
            return True, 'Player 1 wins!'
        elif row == ['o', 'o', 'o']:
            return True, 'Player 2 wins!'
    else:
        return False

def user_input():
    player = input('Enter your player name: ')
    position = input('Enter your position: ')

    mark_board(player, position)

    if check_winner(board):
        return check_winner(board)[1]
    else:
        return user_input()