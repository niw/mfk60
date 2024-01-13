#!/usr/bin/env python3

import argparse
import pcbnew
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--board', type=str, required=True)
parser.add_argument('-s', '--string', default='JLCJLCJLCJLC', type=str)
parser.add_argument('-x', '--x', default=150, type=float)
parser.add_argument('-y', '--y', default=3, type=float)
args = parser.parse_args()

board_path = args.board

board = pcbnew.LoadBoard(board_path)

def find_text(board, string):
    for drawing in board.GetDrawings():
        if drawing.GetClass() == "PCB_TEXT":
            if drawing.GetShownText() == string:
                return drawing
    return None

settings = board.GetDesignSettings()
origin = settings.GetAuxOrigin()

string = args.string
text = find_text(board, string)
if text:
    position = text.GetPosition()
    position.x = origin.x + pcbnew.FromMM(args.x)
    position.y = origin.y + pcbnew.FromMM(args.y)
    text.SetPosition(position)
else:
    print(f"There are no '{string}' text exists.", file=sys.stderr)
    exit(1)

pcbnew.Refresh()
pcbnew.SaveBoard(board_path, board)
