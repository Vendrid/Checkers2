import string


class Board:
    def __init__(self, size, open_square):
        self.size = size
        self.open_square = open_square
        # set empty board
        self.square = [[open_square for y in range(self.size)]for x in range(self.size)]
        # self.square = []
        # for y in range(self.size):
        #     self.square.append([open_square])
        #     for x in range(self.size - 1):
        #         self.square[y].append(open_square)
        self.x_coord_dict = {}
        self.y_coord_dict = {}
        n = self.size
        for dic_name in range(self.size):
            self.x_coord_dict.update({string.ascii_uppercase[dic_name]: dic_name})
            self.y_coord_dict.update({dic_name + 1: n - 1})
            n -= 1

    def show(self):
        print(end='   ')
        for coord_name in string.ascii_uppercase[:self.size]:
            print(coord_name, end=' ')
        coord_name = self.size
        for y in range(len(self.square)):
            print('\n', coord_name, end=' ')
            for x in range(len(self.square[y])):
                print(self.square[x][y], end=' ')
            print(coord_name, end='')
            coord_name -= 1
        print(end='\n   ')
        for coord_name in string.ascii_uppercase[:self.size]:
            print(coord_name, end=' ')
        print()


class GamePiece:
    def __init__(self, name, color, coords, board):
        self.name = name
        self.color = color
        self.coords = coords
        if self.coords[0] < board.size and self.coords[1] < board.size:
            board.square[self.coords[0]][self.coords[1]] = self
        else:
            raise IndexError(f"{self.name}, {self.color} Piece is not on the board")

    def __str__(self):
        return f'{self.name[0]}'

    def get_coords(self):
        return self.coords

    def set_coords(self, new_coords, board):
        board.square[self.coords[0]][self.coords[1]] = board.open_square
        self.coords = new_coords
        board.square[self.coords[0]][self.coords[1]] = self


class CheckersPiece(GamePiece):
    # moves should be sent as a list of tuples of (plus/minus x, plus/minus y)
    def __init__(self, name, color, coords, board, moves):
        self.color = color
        self.moves = moves
        self.moves.sort()

        self.coords = coords
        self.board = board
        self.move_range = []

        GamePiece.__init__(self, name, color, coords, board)

    def init_available_moves(self):
        self.move_range = []

        # get move range only for spaces on the board and open
        for move in self.moves:
            temp_x = move[0] + self.coords[0]
            temp_y = move[1] + self.coords[1]
            if 0 <= temp_x < self.board.size and 0 <= temp_y < self.board.size:
                if self.board.square[temp_x][temp_y] == self.board.open_square:
                    self.move_range.append((temp_x, temp_y))
        # check for possible remaining combos (self - self - open, self - open - open, self - other - open)
        for move in self.move_range[:]:
            if abs(move[0] - self.coords[0]) == 2:
                mid_coord_x = int(self.coords[0] / 2 + move[0] / 2)
                mid_coord_y = int(self.coords[1] / 2 + move[1] / 2)
                mid_coords = (mid_coord_x, mid_coord_y)
                if self.board.square[mid_coord_x][mid_coord_y] == self.board.open_square:
                    self.move_range.remove(move)
                elif self.color == 'black':
                    for o in black_pawn:
                        if mid_coords == o.coords:
                            self.move_range.remove(move)
                elif self.color == 'red':
                    for o in red_pawn:
                        if mid_coords == o.coords:
                            self.move_range.remove(move)
        # piece must jump if able
        jump_move = []
        for move in self.move_range[:]:
            if abs(move[0] - self.coords[0]) == 2:
                jump_move.append(move)
        if jump_move:
            self.move_range = jump_move

    def move(self, new_coords):
        if new_coords in self.move_range:
            if abs(self.coords[0] - new_coords[0]) == 2:
                jumped_coord_x = self.coords[0] / 2 + new_coords[0] / 2
                jumped_coord_y = self.coords[1] / 2 + new_coords[1] / 2
                jumped_coords = (int(jumped_coord_x), int(jumped_coord_y))
                checker_board.square[jumped_coords[0]][jumped_coords[1]] = checker_board.open_square
            else:
                jumped_coords = None

            self.set_coords(new_coords, self.board)


def turn_start(color):
    print(f"It's {color[0].color}'s turn.")
    movable = []
    for i in color[:]:
        i.init_available_moves()
        for n in range(len(i.move_range)):
            if abs(i.coords[0] - i.move_range[n][0]) == 2:
                movable.append(i)
    if movable:
        for i in color[:]:
            if i not in movable:
                i.move_range = []


def get_user_piece():
    user_x, user_y = get_user_coords()
    #print(user_x, user_y)
    if checker_board.square[user_x][user_y] == checker_board.open_square:
        print("That's an empty spot")
    elif checker_board.square[user_x][user_y].color != turn:
        print("It's not that player's turn!")
    elif checker_board.square[user_x][user_y].color == turn:
        if checker_board.square[user_x][user_y].move_range:
            return checker_board.square[user_x][user_y]
        print("That piece can't move.")
    return None


def get_user_coords():
    while True:
        try:
            user_input = input().split(',')
            user_x = checker_board.x_coord_dict[user_input[0]]
            user_y = checker_board.y_coord_dict[int(user_input[1])]
        except (KeyError, ValueError):
            print('Type the row and column of the piece you want to move separated by a comma (X,Y)')
            continue
        return user_x, user_y


# getting the board out
checker_board = Board(8, 'o')

# pieces to use this game
black_pawn = []
red_pawn = []
black_pawn_moves = [(1, 1), (-1, 1), (2, 2), (-2, 2)]
red_pawn_moves = [(1, -1), (-1, -1), (2, -2), (-2, -2)]
king_moves = [(1, -1), (-1, -1), (2, -2), (-2, -2), (1, 1), (-1, 1), (2, 2), (-2, 2)]
# red goes first
turn = 'red'

# setting pawns on the board
temp_index = 0
for y_coord in range(0, 3):
    for x_coord in range(y_coord % 2 == 0, len(checker_board.square[y_coord]), 2):
        black_pawn.append(CheckersPiece('b', 'black', (x_coord, y_coord), checker_board, black_pawn_moves))
        checker_board.square[x_coord][y_coord] = black_pawn[temp_index]
        temp_index += 1
temp_index = 0
for y_coord in range(len(checker_board.square) - 1, 4, -1):
    for x_coord in range(y_coord % 2 == 0, len(checker_board.square[y_coord]), 2):
        red_pawn.append(
            CheckersPiece('r', 'red', (x_coord, y_coord), checker_board, red_pawn_moves))
        checker_board.square[x_coord][y_coord] = red_pawn[temp_index]
        temp_index += 1


while black_pawn and red_pawn:

    if turn == 'red':
        turn_start(red_pawn)
    else:
        turn_start(black_pawn)
    checker_board.show()
    jumped = False
    while True:
        print("Type the row and column of the piece you want to move: ", end='')
        user_piece = get_user_piece()
        if user_piece:
            break
    old_coords = user_piece.coords
    while True:
        print("Type the row and column of the open spot to move that piece: ", end='')
        user_move = get_user_coords()
        if user_move in user_piece.move_range:
            break
    user_piece.move(user_move)

    if turn == 'red':
        for i in black_pawn:
            if i.coords == (int(old_coords[0] / 2 + user_move[0] / 2), int(old_coords[1] / 2 + user_move[1] / 2)):
                black_pawn.remove(i)
                jumped = True
        turn = 'black'
    elif turn == 'black':
        for i in red_pawn:
            if i.coords == (int(old_coords[0] / 2 + user_move[0] / 2), int(old_coords[1] / 2 + user_move[1] / 2)):
                red_pawn.remove(i)
                jumped = True
        turn = 'red'
    user_piece.init_available_moves()
    for i in user_piece.move_range[:]:
        if abs(i[0] - user_piece.coords[0]) == 2 and jumped:
            if user_piece.color == 'black':
                turn = 'black'
            elif user_piece.color == 'red' and jumped:
                turn = 'red'
    for o in red_pawn[:]:
        if o.coords[1] == 0:
            o.name = 'R'
            o.moves = king_moves
    for o in black_pawn[:]:
        if o.coords[1] == 7:
            o.name = 'B'
            o.moves = king_moves

if red_pawn:
    print(
        '''
           *************
           * RED WINS! *
           *************''')
elif black_pawn:
    print(
        '''
           ***************
           * BLACK WINS! *
           ***************'''
    )
else:
    while True:
        print("********ERROR********")
