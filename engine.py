#!/usr/bin/python3

from Piece import Piece
from icons import *
import numpy as np
import copy
import operator

def add(a, b):
    return tuple(map(operator.add, a, b))

def sub(a, b):
    return tuple(map(operator.sub, a, b))

WHITE = 0
BLACK = 1

turn = 0
selected_piece = None
state = "state"

board = np.array([
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None]
])

previous_move = {
    "from": None,
    "to": None
}

KNIGHT_MOVES = [
    (1,2),
    (1,-2),
    (-1,2),
    (-1,-2),
    (2,1),
    (2,-1),
    (-2,1),
    (-2,-1)
]

def get_selected_square():
    if selected_piece:
        return selected_piece.position
    return None

def end_turn():
    global turn
    global selected_piece
    turn = turn + 1
    selected_piece = None

def get_turn():
    if turn%2 == WHITE:
        return "white"
    return "black"

def get_state():
    return state

def init_board():
    global turn
    global selected_piece
    turn = 0
    selected_piece = None

    for i in range(8):
        for j in range(8):
            board[i][j] = None    
    
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

def is_inside(pos):
    i = pos[0]
    j = pos[1]
    return 0 <= i <= 7 and 0 <= j <= 7
    
def get_piece(position):
    if is_inside(position):
        return board[position[0]][position[1]]
    return None

def contains_piece(loc, color, name = None):
    piece = get_piece(loc)
    if piece and piece.color == color:
        if name:
            if piece.name == name:
                return True
            else:
                return False
        return True
    return None

def get_king(color):
    for row in board:
        for col in row:
            if col and col.name == "king" and col.color == color:
                return col
    return None

def is_under_attack(loc, enemy_color):
    y = loc[0]
    x = loc[1]

    # Checks for enemy king, queen, bishop and rook
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            step = (i,j)
            if step == (0,0): continue
            square = add(loc,step)
            if contains_piece(square, enemy_color, "king"):
                return True
            
            while is_inside(square):
                if contains_piece(square, int(not enemy_color)):
                    # Allied piece blocks the path
                    break

                if contains_piece(square, enemy_color, "queen"):
                    return True
                if i == 0 or j == 0:
                    # Horizontal and vertical
                    if contains_piece(square, enemy_color, "rook"):
                        print(square)
                        print(loc)
                        return True
                else:
                    # Diagonal
                    if contains_piece(square, enemy_color, "bishop"):
                        return True
                square = add(square,step)
    
    # Checks for enemy knight
    for knight_move in KNIGHT_MOVES:
        square = add(loc, knight_move)
        if is_inside(square):
            if contains_piece(square, enemy_color, "knight"):
                print("j")
                return True
    
    # Checks for enemy pawn
    dir = 1 if enemy_color == WHITE else -1
    left = (-dir, -1)
    right = (-dir, 1)
    left_square = add(loc,left)
    right_square = add(loc,right)
    if is_inside(left_square):
        if contains_piece(left_square, enemy_color, "pawn"):
            print("ri")
            return True
    if is_inside(right_square):
        if contains_piece(right_square, enemy_color, "pawn"):
            print("le")
            return True

    return False
            

def move_pawn(piece, dest):
    pos = piece.position
    color = piece.color
    dir = 1 if color == WHITE else -1
    if get_piece(dest):
        # Eat en enemy
        if pos[0]+dir == dest[0]:
            if ((pos[1] == dest[1]+1) or
                (pos[1] == dest[1]-1)):
                return True
    else:   
        if pos[1] == dest[1]:
            # One step
            if pos[0]+dir == dest[0]:
                return True
            # Double step
            if ((color == WHITE and dest[0]-2*dir == 1) or 
                (color == BLACK and dest[0]-2*dir == 6)):
                return True
        else:
            # Special move
            adjanced_piece = None
            if (color == WHITE and add(pos,(1,1)) == dest):
                adjanced_piece = get_piece(add(pos,(0,1)))
            if (color == WHITE and add(pos,(1,-1)) == dest):
                adjanced_piece = get_piece(add(pos,(0,-1)))  
            if (color == BLACK and add(pos,(-1,1)) == dest):
                adjanced_piece = get_piece(add(pos,(0,1)))  
            if (color == BLACK and add(pos,(-1,-1)) == dest):
                adjanced_piece = get_piece(add(pos,(0,-1)))  

            if(adjanced_piece and (adjanced_piece.name == "pawn") and  (adjanced_piece.color != color) and (adjanced_piece.get_moves() == 1) and (adjanced_piece.position == previous_move["to"])):
                board[adjanced_piece.position[0]][adjanced_piece.position[1]] = None
                return True
    return False

def move_rook(piece, dest):
    pos = piece.position
    if pos[0] == dest[0]:
        dist = dest[1]-pos[1]
        step = 1 if dist > 0 else -1
        for i in range(step,dist,step):
            if get_piece((pos[0],pos[1]+i)):
                return False
        return True
    if pos[1] == dest[1]:
        dist = dest[0]-pos[0]
        step = 1 if dist > 0 else -1
        for i in range(step,dist,step):
            if get_piece((pos[0]+i,pos[1])):
                return False
        return True
    return False

def move_knight(piece, dest):
    pos = piece.position
    if add(pos,(1,2)) == dest:
        return True       
    if add(pos,(2,1)) == dest:
        return True    
    if add(pos,(-1,2)) == dest:
        return True       
    if add(pos,(-2,1)) == dest:
        return True   
    if add(pos,(1,-2)) == dest:
        return True       
    if add(pos,(2,-1)) == dest:
        return True 
    if add(pos,(-1,-2)) == dest:
        return True       
    if add(pos,(-2,-1)) == dest:
        return True  
    return False

def move_bishop(piece, dest):
    pos = piece.position
    dir = sub(dest,pos)
    uy = 1 if dir[0] > 0 else -1
    ux = 1 if dir[1] > 0 else -1
    if(abs(dir[0]) == abs(dir[1])):
        step_pos = pos
        while True:
            step_pos = add(step_pos, (uy,ux))
            if(step_pos == dest):
                return True
            if(get_piece(step_pos)):
                # Obstacle
                return False
    return False

def move_queen(piece, dest):
    return move_bishop(piece, dest) or move_rook(piece, dest)

def move_king(piece, dest):
    pos = piece.position
    dir = sub(dest,pos)
    if(-1 <= dir[0] <= 1) and (-1 <= dir[1] <= 1):
        return True
    if(piece.get_moves() == 0):
        if(add(pos,(0,2)) == dest):
            square_for_rook = add(pos,(0,1))
            if(not get_piece(square_for_rook)):
                rook = get_piece(add(pos,(0,4)))
                if(rook and rook.get_moves() == 0):
                    rook.did_move()
                    rook.position = square_for_rook
                    board[pos[0]][pos[1]+1] = rook
                    board[pos[0]][pos[1]+4] = None
                    return True
        if(add(pos,(0,-2)) == dest):
            square_for_rook = add(pos,(0,-1))
            if(not get_piece(square_for_rook)):
                rook = get_piece(add(pos,(0,-3)))
                if(rook and rook.get_moves() == 0):
                    rook.did_move()
                    rook.position = square_for_rook
                    board[pos[0]][pos[1]-1] = rook
                    board[pos[0]][pos[1]-3] = None
                    return True
    return False

def click(i,j):
    if i > 7 or i < 0 or j > 7 or j < 0: return 
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
                if focused.color == turn%2:
                    # Choose other piece
                    selected_piece = focused
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
    global board
    global state
    old_board = copy.deepcopy(board)
    move_piece = switcher.get(piece.name)
    i = piece.position[0]
    j = piece.position[1]
    legal_move = move_piece(piece, dest)
    check = is_under_attack(get_king(turn%2).position,(turn+1)%2)
    if not legal_move or check:
        board = copy.deepcopy(old_board)
        if check:
            state = "check"
        return
    piece.did_move()
    piece.position = dest
    board[i][j] = None
    board[dest[0]][dest[1]] = piece

    global previous_move
    previous_move = {
        "from": (i,j),
        "to": (dest[0],dest[1])
    }
    
    end_turn()
    enemy_check = is_under_attack(get_king(turn%2).position,(turn+1)%2)
    if enemy_check:
        state = "check"
