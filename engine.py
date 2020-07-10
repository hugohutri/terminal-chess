from Piece import Piece
from icons import *
import operator

def add(a, b):
    return tuple(map(operator.add, a, b))

def sub(a, b):
    return tuple(map(operator.sub, a, b))

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

def get_piece(position):
    return board[position[0]][position[1]]

def move_pawn(piece, dest):
    pos = piece.position
    dir = 1 if piece.color == WHITE else -1
    if pos[1] == dest[1]:
        if(get_piece(dest)): return False
        # One step
        if pos[0]+dir == dest[0]:
            return True
        # Double step
        if ((piece.color == WHITE and dest[0]-2*dir == 1) or 
            (piece.color == BLACK and dest[0]-2*dir == 6)):
            return True
    if get_piece(dest):
        # Eat en enemy
        if pos[0]+dir == dest[0]:
            if ((pos[1] == dest[1]+1) or
                (pos[1] == dest[1]-1)):
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
    move_piece = switcher.get(piece.type)
    i = piece.position[0]
    j = piece.position[1]
    legal_move = move_piece(piece, dest)
    if not legal_move:
        return
    piece.did_move()
    piece.position = dest
    board[i][j] = None
    board[dest[0]][dest[1]] = piece
    
    end_turn()
