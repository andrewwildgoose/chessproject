import copy
from random import randrange, choice
from typing import Any, List, Tuple, Union, Sequence

def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    return ((ord(loc[0].lower()) - 96), int(loc[1:]))

def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    return f"{chr(x+96)}{y}"

# Define board characteristics 
Board = tuple[int, list['Piece']]

class Piece: #Base class for pieces
    pos_x : int
    pos_y : int
    side : bool #True for White and False for Black
    piece_code : Union[list[str], str]
    
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_
        piece_code = ["\u2656", "\u265C", "\u2657", "\u265D", "\u2654", "\u265A"] # full list of piece codes to be narrowed down by subclasses

    def _get_move_list(self, pos_X: int, pos_Y: int) -> list[tuple[int, int]]:
        '''
        abstract method for obtaining the move_list
        '''
        pass

    def can_reach(self, pos_X : int, pos_Y : int, B : Board) -> bool:
        '''
        checks if this Rook or Bishop piece can move to coordinates pos_X, pos_Y
        on board B according to rule ([Rule1] or [Rule2]) and [Rule4](see section Intro)
        '''
        squares = get_squares(B)
        if (pos_X, pos_Y) in self._get_move_list(pos_X, pos_Y) and (pos_X, pos_Y) in squares:
            for pos in self._get_move_list(pos_X, pos_Y):
                if not is_piece_at(pos[0], pos[1], B):
                    continue
                elif is_piece_at(pos[0], pos[1], B):
                    if pos == (pos_X, pos_Y) and piece_at(pos_X, pos_Y, B).side != self.side:
                        return True
                    else:
                        return False
            return True
        else:
            return False

    def can_move_to(self, pos_X : int, pos_Y : int, B : Board) -> bool:
        '''
        checks if this piece can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        '''
        temp_B = copy.deepcopy(B)
        moving_piece = copy.deepcopy(self)
        if self.can_reach(pos_X, pos_Y, B):
            if is_piece_at(pos_X, pos_Y, B) and piece_at(pos_X, pos_Y, B).side != self.side:
                temp_B[1].remove(piece_at(pos_X, pos_Y, temp_B))
            temp_B[1].remove(piece_at(self.pos_x, self.pos_y, temp_B))
            moving_piece.pos_x, moving_piece.pos_y = pos_X, pos_Y
            temp_B[1].append(moving_piece)
            if is_check(moving_piece.side, temp_B):
                return False
            else:
                return True
        else:
            return False
   
    def move_to(self, pos_X : int, pos_Y : int, B : Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B
        assumes this move is valid according to chess rules
        '''
        if self.can_move_to(pos_X, pos_Y, B):
            if is_piece_at(pos_X, pos_Y, B) and piece_at(pos_X, pos_Y, B).side != self.side:
                B[1].remove(piece_at(pos_X, pos_Y, B))
            self.pos_x, self.pos_y = pos_X, pos_Y
        return B

# General functions used throughout other functions & class methods

def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B'''
    for piece in B[1]:
        if pos_X == piece.pos_x:
            if pos_Y == piece.pos_y:
                return True
    return False

def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for piece in B[1]:
        if pos_X == piece.pos_x:
            if pos_Y == piece.pos_y:
                piece_at = piece
    return piece_at

def get_squares(B: Board) -> list[tuple[int, int]]:
    ''' returns a list of all the squares on the board '''
    return [(x, y) for x in range(1, (B[0])+1) for y in range(1, (B[0])+1)]

class Rook(Piece):
    
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
        # unicode sequences for white and black rooks
        piece_code = ["\u2656", "\u265C"]
        # determines which unicode sequence to use
        if self.side:
            self.piece_code = piece_code[0]
        else:
            self.piece_code = piece_code[1]
            
    def __repr__(self):
        return f"Rook, {self.pos_x, self.pos_y, self.side}"
    
    def _get_move_list(self, pos_X : int, pos_Y : int) -> list[tuple[int, int]]:
        ''' gets a list containing a list of tuples for each possible move based on the piece's movement rules'''
        if pos_Y > self.pos_y and self.pos_x == pos_X: # up
            return [(self.pos_x, self.pos_y+i) for i in range(1, pos_Y - self.pos_y + 1)]
        elif pos_Y < self.pos_y and self.pos_x == pos_X: # down
            return [(self.pos_x, self.pos_y-i) for i in range(1, self.pos_y - pos_Y + 1)]
        elif pos_X < self.pos_x and self.pos_y == pos_Y: # left
            return [(self.pos_x-i, self.pos_y) for i in range(1, self.pos_x - pos_X + 1)]
        elif pos_X > self.pos_x and self.pos_y == pos_Y: # right
            return [(self.pos_x+i, self.pos_y) for i in range(1, pos_X - self.pos_x + 1)]
        else: # invalid move
            return []

class Bishop(Piece):
    
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

        # unicode sequences for white and black bishops
        piece_code = ["\u2657", "\u265D"]
        # determines which unicode sequence to use
        if self.side:
            self.piece_code = piece_code[0]
        else:
            self.piece_code = piece_code[1]

    def __repr__(self):
        return f"Bishop, {self.pos_x, self.pos_y, self.side}"
    
    def _get_move_list(self, pos_X : int, pos_Y : int) -> list[tuple[int, int]]:
        ''' gets a list containing a list of tuples for each possible move based on the piece's movement rules'''
        if abs(self.pos_x - pos_X) == abs(self.pos_y - pos_Y):
            if pos_Y > self.pos_y and pos_X < self.pos_x: # up & left
                return [(self.pos_x-i, self.pos_y+i) for i in range(1, abs(pos_Y - self.pos_y) + 1)]
            elif pos_Y > self.pos_y and pos_X > self.pos_x: # up & right
                return [(self.pos_x+i, self.pos_y+i) for i in range(1, abs(pos_Y - self.pos_y) + 1)]
            elif pos_Y < self.pos_y and pos_X < self.pos_x: # down & left
                return [(self.pos_x-i, self.pos_y-i) for i in range(1, abs(pos_Y - self.pos_y) + 1)]
            elif pos_Y < self.pos_y and pos_X > self.pos_x: # down & right
                return [(self.pos_x+i, self.pos_y-i) for i in range(1, abs(pos_Y - self.pos_y) + 1)]
            else:
                return []
        else:
            return []

class King(Piece):
    
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        #inherits from class piece
        super().__init__(pos_X, pos_Y, side_)
        # unicode sequences for white and black kings
        piece_code = ["\u2654", "\u265A"]
        # determines which unicode sequence to use
        if self.side:
            self.piece_code = piece_code[0]
        else:
            self.piece_code = piece_code[1]
            
    def __repr__(self):
        return f"King, {self.pos_x, self.pos_y, self.side}"

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule3] and [Rule4]'''
        squares = get_squares(B)
        if (pos_X, pos_Y) in squares:
            if (abs(pos_X - self.pos_x)) <= 1 and (abs(pos_Y - self.pos_y)) <= 1:
                if not is_piece_at(pos_X, pos_Y, B):
                    return True
                if is_piece_at(pos_X, pos_Y, B) and piece_at(pos_X, pos_Y, B).side != self.side:
                    return True
        return False

# Check & checkmate functions used to inform moving pieces and the flow of play

def is_check(side : bool, B : Board) -> bool:
    ''' checks if configuration of B is check for side '''
    pieces = B[1]
    check_king = [piece for piece in pieces if repr(piece)[0] == "K" and piece.side == side][0]
    for piece in pieces:
        if piece.side != side and piece.can_reach(check_king.pos_x, check_king.pos_y, B):
            return True
        else:
            continue
    return False

def is_checkmate(side : bool, B : Board) -> bool:
    ''' checks if configuration of B is checkmate for side '''
    squares = get_squares(B)
    pieces = [piece for piece in B[1] if piece.side == side]
    for piece in pieces:
        for square in squares:
            if piece.can_reach(square[0], square[1], B):
                temp_piece = copy.deepcopy(piece)
                temp_piece.pos_x, temp_piece.pos_y = square[0], square[1]
                temp_B = copy.deepcopy(B)
                temp_B[1].remove(piece_at(piece.pos_x, piece.pos_y, temp_B))
                temp_B[1].append(temp_piece)
                if is_piece_at(temp_piece.pos_x, temp_piece.pos_y, temp_B) and piece_at(temp_piece.pos_x, temp_piece.pos_y, temp_B).side != temp_piece.side:
                    temp_B[1].remove(piece_at(temp_piece.pos_x, temp_piece.pos_y, temp_B))
                if not is_check(side, temp_B):
                    return False
    return True

# Board reading & saving functions and associated functions

def clean_it(line : str) -> list[str]:
    '''
    Takes a line from the board, cleans it of any unwanted characters and returns a list
    '''
    split_line = line.split(", ")
    cleaned_line = []
    for item in split_line:
        item = item.replace("\n","")
        item = item.replace(" ","")
        item = item.replace(",","")
        cleaned_line.append(item)   
    return cleaned_line

def str2pieces_white(piece_str : list[str]) -> Sequence[Piece]:
    '''
    Takes a clean string and returns the corresponding Piece item for white pieces
    '''
    white_king_str = [piece for piece in piece_str if piece[0] == "K"]
    white_king = [King(location2index(piece[1:])[0], location2index(piece[1:])[1], True) for piece in white_king_str]
    if len(white_king) != 1:
        raise IOError 
    white_rook_str = [piece for piece in piece_str if piece[0] == "R"]
    white_rooks = [Rook(location2index(piece[1:])[0], location2index(piece[1:])[1], True) for piece in white_rook_str]   
    white_bishop_str = [piece for piece in piece_str if piece[0] == "B"]
    white_bishops = [Bishop(location2index(piece[1:])[0], location2index(piece[1:])[1], True) for piece in white_bishop_str]
    white_pieces = white_king + white_rooks + white_bishops
    return white_pieces

def str2pieces_black(piece_str : list[str]) -> Sequence[Piece]:
    '''
    Takes a clean string and returns the corresponding Piece item for black pieces
    '''
    black_king_str = [piece for piece in piece_str if piece[0] == "K"]
    black_king = [King(location2index(piece[1:])[0], location2index(piece[1:])[1], False) for piece in black_king_str]
    if len(black_king) != 1:
        raise IOError
    black_rook_str = [piece for piece in piece_str if piece[0] == "R"]
    black_rooks = [Rook(location2index(piece[1:])[0], location2index(piece[1:])[1], False) for piece in black_rook_str]   
    black_bishop_str = [piece for piece in piece_str if piece[0] == "B"]
    black_bishops = [Bishop(location2index(piece[1:])[0], location2index(piece[1:])[1], False) for piece in black_bishop_str]
    black_pieces = black_king + black_rooks + black_bishops
    return black_pieces

def read_board(filename : str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    board_size : Union[List[str], str, int]
    white_pieces : Union[List[str], str, Sequence[Piece]]
    black_pieces : Union[List[str], str, Sequence[Piece]]

    plain_board = open(filename)

    # cleaning up & preparing the board size & pieces to be read    
    board_size = plain_board.readline()
    board_size = clean_it(board_size)
    board_size = int(board_size[0])
    if type(board_size) != int or 1 > board_size > 26:
        raise IOError
    
    white_pieces = plain_board.readline()
    try:
        white_pieces = clean_it(white_pieces)
        white_pieces = str2pieces_white(white_pieces)
    except ValueError:
        raise IOError
    
    black_pieces = plain_board.readline()
    try:
        black_pieces = clean_it(black_pieces)
        black_pieces = str2pieces_black(black_pieces)
    except ValueError:
        raise IOError
    
    plain_board.close()
    pieces = white_pieces + black_pieces
    B = (board_size, pieces)

    for piece in pieces:
        if is_piece_at(piece.pos_x, piece.pos_y, B) and piece_at(piece.pos_x, piece.pos_y, B) != piece:
            raise IOError
        elif (piece.pos_x, piece.pos_y) not in get_squares(B):
            raise IOError

    return B

def piece2str(piece : Piece) -> str:
    piece_str = ""
    if repr(piece)[0] == "K":
        piece_str += "K"
    elif repr(piece)[0] == "R":
        piece_str += "R"
    elif repr(piece)[0] == "B":
        piece_str += "B"
    piece_str += index2location(piece.pos_x, piece.pos_y)
    return piece_str

def save_board(filename : str, B : Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    board_size = str(B[0])
    white_pieces = [piece2str(piece) for piece in B[1] if piece.side == True]
    black_pieces = [piece2str(piece) for piece in B[1] if piece.side == False]

    save_file = open(filename, "w")
    save_file.write(f"{board_size}\n")
    for piece in white_pieces:
        if piece == white_pieces[-1]:
            save_file.write(f"{piece}\n")
        else:
            save_file.write(f"{piece}, ")
    for piece in black_pieces:
        if piece == black_pieces[-1]:
            save_file.write(f"{piece}\n")
        else:
            save_file.write(f"{piece}, ")
    save_file.close()


def find_black_move(B : Board) -> Tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules
    assumes there is at least one black piece that can move somewhere
    '''
    black_pieces = [piece for piece in B[1] if piece.side == False]
    not_valid_move = True
    while not_valid_move:
        moving_piece = choice(black_pieces)
        move_location = choice(get_squares(B))
        black_can_move = moving_piece.can_move_to(move_location[0], move_location[1], B)
        if black_can_move:
            not_valid_move = False
    return (moving_piece, move_location[0], move_location[1]) 

# Board display functions for UI

def make_board_matrix(B : Board) -> List[List[Tuple[int, int]]]:
    '''converts list of squares on the board to a matrix representing the board'''
    board = []
    squares = get_squares(B)
    for rows in range(1, B[0]+1):
        row = [square for square in squares if square[1] == rows]
        board.append(row)
    board.reverse() 
    return board

def conf2unicode(B : Board) -> str:
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    square : Any
    empty_board : List[List[Tuple[int, int]]]

    empty_board = make_board_matrix(B)
    pieces_and_spaces = []
    for row in empty_board:
        for square in row:
            if is_piece_at(square[0], square[1], B):
                square = piece_at(square[0], square[1], B).piece_code
                pieces_and_spaces.append(square)
            else:
                square = "\u2001"
                pieces_and_spaces.append(square)
        pieces_and_spaces.append("\n")
    board = "".join([str(square) for square in pieces_and_spaces])
    board = board.rstrip("\n") # removes the trailing newline on the last row
    return board

def split_player_move(move_string : str) -> list[str]:
    '''
    splits the player move input string into start location and desired end location in chess format
    '''
    alpha_count = 0
    for char in range(len(move_string)):
        if move_string[char].isalpha() and alpha_count < 2:
            alpha_count += 1
            end_col = char
    if alpha_count == 0 or len(move_string) < 4:
        raise IOError
    start_loc = move_string[:end_col]
    end_loc = move_string[end_col:]
    return [start_loc, end_loc]

# Implementation of play

def main() -> None:
    ''' runs the play '''
    looking_for_valid_board = True
    filename = input("File name for initial configuration: ")

    while looking_for_valid_board:
        if filename == "QUIT": # if user types "QUIT" terminate the programme
            quit()
        else:
            try: # if valid file -> store file in plain board configuration
                current_board = read_board(filename)
                save_board(filename, current_board)
                print("The initial configuration is:")
                print(conf2unicode(current_board))
                looking_for_valid_board = False
            except IOError:
                filename = input("This is not a valid file. File name for initial configuration: ")
    
    in_play = True
    white_turn = True
    
    # process for each side taking turns
    while in_play:
        # determing if only kings left on each side. If so, end play and call a draw
        if len(current_board[1]) == 2 and repr(current_board[1][0])[:4] == repr(current_board[1][1])[:4]:
           in_play = False
        
        # white move process
        elif white_turn:
            white_move = input("Next move of White: ")
            
            if white_move == "QUIT": # if user types "QUIT" terminate the programme
                savename = input("File name to store the configuration: ")
                save_board(savename, current_board)
                quit()         
            try:
                start_loc = split_player_move(white_move)[0] # location of piece to move
                end_loc = split_player_move(white_move)[1] # desired end location

                start_x = location2index(start_loc)[0]
                start_y = location2index(start_loc)[1]
                end_x = location2index(end_loc)[0]
                end_y = location2index(end_loc)[1]

                if not is_piece_at(start_x, start_y, current_board): # check is piece is at start location
                    raise IOError

                white_move_piece = piece_at(start_x, start_y, current_board) # moving piece
    
                if not white_move_piece.can_move_to(end_x, end_y, current_board): # check valid move
                    raise IOError
                
                current_board = white_move_piece.move_to(end_x, end_y, current_board) # update the board
                print("The configuration after White's move is: ")
                print(conf2unicode(current_board))
                white_turn = False

                if is_checkmate(False, current_board): # check if Black is in checkmate
                    print("Game over. White wins.")
                    quit()

            except IOError:
                print("This is not a valid move.")

    # Black move process
        else:
            black_move = find_black_move(current_board)
            black_move_piece = black_move[0]
            black_move_str = index2location(black_move_piece.pos_x, black_move_piece.pos_y) + index2location(black_move[1], black_move[2])
            current_board = black_move_piece.move_to(black_move[1], black_move[2], current_board)
            print(f"Next move of Black is {black_move_str}. The configuration after Black's move is: ")
            print(conf2unicode(current_board))
            white_turn = True

            if is_checkmate(True, current_board): # check if White is in checkmate
                print("Game over. Black wins.")
                quit()
    
    print("Game over. It's a draw.")

if __name__ == '__main__': #keep this in
   main()
