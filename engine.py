from Piece import Piece
from icons import *

WHITE = 0
BLACK = 1

turn = 0
selected_piece = None

board = [
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None]
]


def end_turn():
    global turn
    global selected_piece
    turn = turn + 1
    selected_piece = None

def init_board():
    board[0][0] = Piece("rook",WHITE_ROOK, WHITE,(0,0))
    board[0][1] = Piece("knight",WHITE_KNIGHT, WHITE,(0,1))
    board[0][2] = Piece("bishop",WHITE_BISHOP, WHITE,(0,2))
    board[0][3] = Piece("king",WHITE_KING, WHITE,(0,3))
    board[0][4] = Piece("queen",WHITE_QUEEN, WHITE,(0,4))
    board[0][5] = Piece("bishop",WHITE_BISHOP, WHITE,(0,5))
    board[0][6] = Piece("knight",WHITE_KNIGHT, WHITE,(0,6))
    board[0][7] = Piece("rook",WHITE_ROOK, WHITE,(0,7))
    for i in range(8):
        board[1][i] = Piece("pawn",WHITE_PAWN, WHITE,(1,i))

    board[7][0] = Piece("rook",BLACK_ROOK, BLACK,(7,0))
    board[7][1] = Piece("knight",BLACK_KNIGHT, BLACK,(7,1))
    board[7][2] = Piece("bishop",BLACK_BISHOP, BLACK,(7,2))
    board[7][3] = Piece("king",BLACK_KING, BLACK,(7,3))
    board[7][4] = Piece("queen",BLACK_QUEEN, BLACK,(7,4))
    board[7][5] = Piece("bishop",BLACK_BISHOP, BLACK,(7,5))
    board[7][6] = Piece("knight",BLACK_KNIGHT, BLACK,(7,6))
    board[7][7] = Piece("rook",BLACK_ROOK, BLACK,(7,7))
    for i in range(8):
        board[6][i] = Piece("pawn",BLACK_PAWN, BLACK,(6,i))

def move_pawn(piece, dest):
    piece.position = dest

def move_rook(piece, dest):
    piece.position = dest

def move_knight(piece, dest):
    piece.position = dest

def move_bishop(piece, dest):
    piece.position = dest

def move_queen(piece, dest):
    piece.position = dest

def move_king(piece, dest):
    piece.position = dest

def click(i,j):
    focused = board[i][j]
    global selected_piece
    if focused:
        # Clicked a piece
        if selected_piece:
            # Trying to eat
            if selected_piece.color != focused.color:
                # Enemy piece
                move(selected_piece, (i,j))
        else:
            # Trying to control a piece
            if focused.color == turn%2:
                selected_piece = focused
    else:
        # Clicked an empty square
        if selected_piece:
            # Move to empty square
            move(selected_piece, (i,j))

    

def move(piece, dest):
    switcher = {
        "pawn": move_pawn,
        "rook": move_rook,
        "knight": move_knight,
        "bishop": move_bishop,
        "queen": move_queen,
        "king": move_king
    }
    move_piece = switcher.get(piece.type)
    i = piece.position[0]
    j = piece.position[1]
    move_piece(piece, dest)
    board[i][j] = None
    board[dest[0]][dest[1]] = piece
    
    end_turn()
    print(f" Turn {turn+1}")
