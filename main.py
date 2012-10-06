#!/usr/bin/python

__appname__ = 'pyCello'
__version__ = "0.1"
__author__  = "Dariusz Dwornikowski"
__licence__ = "LGPL"

import time
import random
import sys
import signal
import argparse

try:
    import curses
except ImportError:
    print("Curses not found")
    print()
    sys.exit(1)

class CellScreen():

    def __init__(self, size_x=50, size_y=20):
        self._cell_sign = "#"
        self.screen = curses.initscr()
        if size_x == "MAX" or size_y == "MAX":
            self.size_x, self.size_y = self.screen.getmaxyx()
            self.size_x, self.size_y = self.size_x-1, self.size_y-1
        else:
            self.size_x, self.size_y = size_x, size_y
       # self.screen.border(0)
        signal.signal(signal.SIGINT, self._sig_hdl)
        self._init_board()

    def set_cell(self, chrnum):
        self._cell_sign = chrnum

    def draw_board(self):
        for cell in self.board:
            #if self.board[cell] == 1: self.screen.addstr(cell[0], cell[1], str(chr(0x25a0)))
            if self.board[cell] == 1: self.screen.addstr(cell[0], cell[1], self._cell_sign)
        self.screen.refresh()
        self.screen.clear()


    def _init_board(self):
        self.board = dict()
        for x in range(self.size_x):
            for y in range(self.size_y):
                if random.random() < 0.25:
                    self.board[(x,y)] = 1
                else:
                    self.board[(x,y)] = 0

    def update_board(self):
        for cell in self.board:
            neighs = self._count_neighs(cell)
            if self.board[cell] == 0 and neighs == 3:
                self.board[cell] = 2
            elif self.board[cell] == 1 and not neighs in [2,3]:
                self.board[cell] = -1
        for cell in self.board:
            if self.board[cell] == 2:
                self.board[cell] = 1
            if self.board[cell] == -1:
                self.board[cell] = 0

    def _count_neighs(self,cell):
        neighs = [ (cell[0]-1,cell[1]), (cell[0]-1,cell[1]-1),(cell[0],cell[1]-1), (cell[0]+1,cell[1]-1), (cell[0]+1,cell[1]), (cell[0]+1,cell[1]+1), (cell[0],cell[1]+1), (cell[0]-1,cell[1]+1) ]
        score = 0
        for nei in neighs:
            if nei in self.board.keys():
                if self.board[nei] in [1,-1]:
                    score += 1
        return score


    def _sig_hdl(self, signal, frame):
        curses.endwin()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="%s by %s" % (__appname__, __author__))
    parser.add_argument("-d", "--delay", help="Delay for drawing, default 1s", action="store", dest="delay", type=int, default=1)
    parser.add_argument("-g", "--geometry", help="Geometry e.g. 50x50 or MAX for maximal", action="store", dest="geom", type=str, default="MAX")
    parser.add_argument("--cell_char", help="Geometry e.g. 50x50 or MAX for maximal", action="store", dest="cell_char", type=str, default="#")
    args = parser.parse_args()
    cs = None
    if args.geom == "MAX":
        cs = CellScreen(args.geom)
        cs.set_cell(args.cell_char)
    else:
        geom = args.geom.split("x")
        cs = CellScreen(int(geom[0]), int(geom[1]))
        cs.set_cell(args.cell_char)
    while True:
        cs.update_board()
        cs.draw_board()
        time.sleep(args.delay)

if __name__ ==  "__main__":
    main()

