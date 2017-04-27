# class BoardStatus(object):
#     def __init__(self, positions, columns=3, rows=3):
#         self.positions = positions
#         self.columns = columns
#         self.rows = rows
#         self.board = generate_board()
#         self.plot =
#
#     def plot_board(self, x, y):
#         board = self.board
#
#
#
#     def generate_board(self):
#         columns = range(self.columns)
#         rows = [0] * self.rows
#         board = [[x for x in rows] for x in columns]
#
#         return board
#
#     def mark_board(self, x, y):
#
#
#     def print_board(self):
#         for row in generate_board():
#             print(row)

columns = 3
columns_range = range(columns)
rows = 3
rows_list = [0] * rows

input_keys = [x for x in range(1, (columns * rows +1))]
player_one = 1
player_two = 2

board = []


def generate_board():
    global columns
    global rows
    rows = [0] * rows
    board = [[x for x in rows] for x in columns]

    return board


# def print_board(self):
#     for row in plot_board():
#         print(row)


def mark_board(position):
    return plot_board(position)


def plot_board():
    global board
    board = generate_board()


print(plot_board())

