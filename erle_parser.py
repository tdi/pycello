#!/usr/bin/python

from pyparsing import Literal, Optional, nums, alphas, restOfLine, ZeroOrMore, Word

def rle_gramma():
    def print_cell(cell):
        if cell == "b":
            print("_", end="")
        elif cell == "o":
            print("X", end="")
        elif cell == "$":
            print()

    def rule(string, lok, tok):
        if len(tok) > 1:
            num = int(tok[0])
            letter = tok[1]
            for i in range(0,num):
                print_cell(letter)
        else:
            letter = tok[0]
            print_cell(letter)

    dolar = Literal('$')
    bang = Literal('!')
    define = Literal('=')
    coma = Literal(',')
    number = Word(nums)
    letter = Literal('b') | Literal ('o')
    comment = '#' + restOfLine
    xdef = 'x' + define + number
    ydef = 'y' + define + number
    ruledef = 'rule' + define + Word(alphas)
    defheader = xdef + coma + ydef + ruledef + restOfLine
    rule = (Optional(number) + (letter | dolar)).setParseAction(rule)
    model = ZeroOrMore(comment) + Optional(defheader) + ZeroOrMore(rule) + bang
    return model

