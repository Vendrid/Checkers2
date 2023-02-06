class Board:
    def __init__(self, size, open_square):
        self.size = size
        self.open_square = open_square
        self.square = []
        for y in range(self.size):
            self.square.append([open_square])
            for x in range(self.size - 1):
                self.square[y].append(open_square)

    def show(self):
        for y in range(len(self.square)):
            print()
            for x in range(len(self.square[y])):
                print(self.square[x][y], end=' ')
        print()


class GamePiece:
    # moves should be sent as a set of (plus/minus x, plus/minus y) coordinates
    def __init__(self, name, color, piece_coords, moves):
        self.name = name
        self.color = color
        self.piece_coords = piece_coords
        self.moves = moves
        self.available_moves = []

    def __str__(self):
        return f'{self.name[0]}'

    def get_coords(self):
        return self.piece_coords

    def update_coords(self, coords):
        self.piece_coords = coords

    def check_move_range(self, board):
        print(self.color)
        self.available_moves = []
        # get move range only for spaces on the board and open
        for i in self.moves:
            temp_x = i[0] + self.piece_coords[0]
            temp_y = i[1] + self.piece_coords[1]
            if 0 <= temp_x < board.size and 0 <= temp_y < board.size:
                if board.square[temp_x][temp_y] == board.open_square:
                    self.available_moves.append((temp_x, temp_y))

        # check sequential spaces diagonally
        temp_moves = self.available_moves
        for i in range(1, len(self.available_moves)):
            # further coords from current position
            am_x = self.available_moves[i][0]
            am_y = self.available_moves[i][1]
            # closer coords to current position
            tm_x = temp_moves[i - 1][0]
            tm_y = temp_moves[i - 1][1]
            print('check', self.available_moves[i], temp_moves[i - 1])
            if abs(am_x - tm_x) == 1 == abs(am_y - tm_y):
                print("there: ", am_x, am_y)
                print("here: ", tm_x, tm_y)
                if board.square[tm_x][tm_y] == board.open_square:
                    self.available_moves.remove((am_x, am_y))
                    # might not need this lower part. Test after able to move pieces
                # elif board.square[tm_x][tm_y] != self.color:
                #     if board.square[am_x][am_y] == board.open_square:
                #         available_moves.remove((tm_x), (tm_y))
        self.available_moves = self.available_moves
        return self.available_moves

    def move_piece(self, destination_coords, board):
        self.check_move_range(board)
        if destination_coords in self.available_moves:
            board.square[self.piece_coords[0]][self.piece_coords[1]] = board.open_square
            board.square[destination_coords[0]][destination_coords[1]] = self
            self.update_coords(destination_coords)


# getting the board out
checker_board = Board(8, 'o')

# pieces to use this game
black_pawn = []
white_pawn = []

# setting pawns on the board
temp_index = 0
for y_coord in range(0, 3):
    for x_coord in range(y_coord % 2 == 0, len(checker_board.square[y_coord]), 2):
        black_pawn.append(GamePiece('b', 'black', (x_coord, y_coord), ((1, 1), (-1, 1), (2, 2), (-2, 2))))
        checker_board.square[x_coord][y_coord] = black_pawn[temp_index]
        temp_index += 1
temp_index = 0
for y_coord in range(len(checker_board.square) - 1, 4, -1):
    for x_coord in range(y_coord % 2 == 0, len(checker_board.square[y_coord]), 2):
        white_pawn.append(GamePiece('w', 'white', (x_coord, y_coord), ((1, -1), (-1, -1), (2, -2), (-2, -2))))
        checker_board.square[x_coord][y_coord] = white_pawn[temp_index]
        temp_index += 1

checker_board.show()
