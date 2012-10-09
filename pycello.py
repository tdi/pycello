#!/usr/bin/python

__appname__ = 'pyCello'
__version__ = "0.1"
__author__  = "Dariusz Dwornikowski"
__licence__ = "LGPL"


import sys
if sys.version_info[0] != 3:
    print("Works only in python 3")
    exit(1)

import time
import re
import random
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
        self.birth = [int(x) for x in "2"]
        self.survive = [int(x) for x in "23"]
        self.screen = curses.initscr()
        if size_x == "MAX" or size_y == "MAX":
            self.size_x, self.size_y = self.screen.getmaxyx()
            self.size_x, self.size_y = self.size_x-1, self.size_y-1
        else:
            self.size_x, self.size_y = size_x, size_y
        signal.signal(signal.SIGINT, self._sig_hdl)

    def set_cell(self, chrnum):
        self._cell_sign = chrnum

    def set_birth(self, bi):
        self.birth = tuple(bi)

    def set_surv(self, surv):
        self.survive = tuple(surv)

    def draw_board(self):
        for cell in self.board:
            if self.board[cell] == 1: self.screen.addstr(cell[0], cell[1], self._cell_sign)
        self.screen.refresh()
        self.screen.clear()

    def _cell_sign_gen(self):
        return str(("a", "b", "#", "$" , "%", "^", "&", "8", "O", "0")[int(random.random()*10)])

    def init_board(self, rand_factor=0.25):
        self.board = dict()
        for x in range(self.size_x):
            for y in range(self.size_y):
                if random.random() < rand_factor:
                    self.board[(x,y)] = 1
                else:
                    self.board[(x,y)] = 0


    def _sig_hdl(self, signal, frame):
        curses.endwin()
        sys.exit(1)

    def update_board(self):
        for cell in self.board:
            neighs = self._count_neighs(cell)
            if self.board[cell] == 0 and neighs in self.birth:
                self.board[cell] = 2
            elif self.board[cell] == 1 and not neighs in self.survive:
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

def parse_llrule(rule):
    if not re.match('B[0-8]*/S[0-8]*', rule):
        print("Rule's syntax must be e.g. : BXX/SXX, where X is in (0,8)")
        sys.exit(1)
    birth, surv = rule.split("/")
    birth, surv = birth[1:], surv[1:]
    if len(birth) == 0: birth = "0"
    if len(surv) == 0: surv = "0"
    return (birth, surv)

def validate_geom(geom):
    if not re.match('[0-9]+x[0-9]+', geom):
        print("Geometry must be of a form XXxYY, e.g. 50x50")
        sys.exit(1)

def validate_rand_factor(rnd):
    if rnd < 0 or rnd > 1:
        print("Rand factor must be between 0 and 1")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="%s by %s" % (__appname__, __author__))
    parser.add_argument("-d", "--delay", help="Delay for drawing, default 1s", action="store", dest="delay", type=int, default=1)
    parser.add_argument("-g", "--geometry", help="Geometry e.g. 50x50 or MAX for maximal", action="store", dest="geom", type=str, default="MAX")
    parser.add_argument("--cell_char", help="A character depicting a cell", action="store", dest="cell_char", type=str, default=str(chr(0x25a2)))
    parser.add_argument("--rand_factor", help="Randomization factor", action="store", dest="randfact", type=float, default=0.25)
    parser.add_argument("--llrule", help="Lifelike rule e.g. B3/S23 for CGoL", action="store", dest="llrule", type=str, default="B3/S23")
    args = parser.parse_args()
    cs = None

    bi, su = parse_llrule(args.llrule)

    validate_rand_factor(args.randfact)

    if args.geom == "MAX":
        cs = CellScreen(args.geom)
        cs.birth = [int(x) for x in bi]
        cs.survive = [int(x) for x in su]
        cs.init_board(args.randfact)
        cs.set_cell(args.cell_char)
    else:
        validate_geom(args.geom)
        geom = args.geom.split("x")
        cs = CellScreen(int(geom[0]), int(geom[1]))
        cs.birth = [int(x) for x in bi]
        cs.survive = [int(x) for x in su]
        cs.init_board(args.randfact)
        cs.set_cell(args.cell_char)
    while True:
        cs.update_board()
        cs.draw_board()
        time.sleep(args.delay)

if __name__ ==  "__main__":
    main()

