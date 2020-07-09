#!/usr/bin/python3

from Piece import Piece
from engine import *
import curses
import time

BG_BLACK = 1
BG_WHITE = 2
FG_BLACK = 3
FG_WHITE = 4

BLACK_ON_BLACK = 1
BLACK_ON_WHITE = 2
WHITE_ON_BLACK = 3
WHITE_ON_WHITE = 4

selected_piece = None
destination = None

def print_square(i,j):
    p = board[i][j]
    bg = get_square_color(i,j,p)
    if p:
        screen.addstr(i,3*j,f" {p.icon} ",curses.color_pair(bg))
    else:
        screen.addstr(i,3*j,f"   ",curses.color_pair(bg))


def get_square_color(i,j,p):
    if((i % 2 == 1 and j % 2 == 1) or (i % 2 == 0 and j % 2 == 0)):
        if (p and p.color == WHITE):
                return WHITE_ON_WHITE
        return BLACK_ON_WHITE
    if (p and p.color == WHITE):
        return WHITE_ON_BLACK
    return BLACK_ON_BLACK


def print_board():
    for i in range(8):
        for j in range(8):
            print_square(i,j)  

if __name__ == '__main__':
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    screen.keypad(1) 
    curses.mousemask(1)

    # Colors
    curses.init_color(BG_BLACK, 627, 321, 176)
    curses.init_color(BG_WHITE, 770, 721, 529)
    curses.init_color(FG_BLACK, 0, 0, 0)
    curses.init_color(FG_WHITE, 1000, 1000, 1000)

    curses.init_pair(BLACK_ON_BLACK, FG_BLACK, BG_BLACK)
    curses.init_pair(BLACK_ON_WHITE, FG_BLACK, BG_WHITE)
    curses.init_pair(WHITE_ON_BLACK, FG_WHITE, BG_BLACK)
    curses.init_pair(WHITE_ON_WHITE, FG_WHITE, BG_WHITE)

    init_board()

    try:
        print_board()
        screen.refresh()

        while True:
            event = screen.getch() 
            if event == ord("q"): break 
            if event == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                i = my
                j = int(mx/3)
                
                click(i,j)

                print_board()
                screen.refresh()

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()