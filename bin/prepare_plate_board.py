#!/usr/bin/env python3

import argparse
import os
import re
import pcbnew

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--board', type=str, required=True)
parser.add_argument('-p', '--plate', type=str, required=True)
parser.add_argument('--positioning-only', action='store_true')
parser.add_argument('--footprint-pattern', default="^(Gateron_Low_Profile:.*|kikit:Tab|MountingHole.*:MountingHole.*)", type=str)
args = parser.parse_args()

board_path = args.board
plate_path = args.plate
positioning_only = args.positioning_only
footprint_pattern = args.footprint_pattern

board = pcbnew.LoadBoard(board_path)
plate_board = pcbnew.LoadBoard(plate_path) if os.path.exists(plate_path) else pcbnew.CreateEmptyBoard()

# PCB Shape
if not positioning_only:
    for drawing in plate_board.GetDrawings():
        if drawing.GetClass() == "PCB_SHAPE":
            plate_board.RemoveNative(drawing)
    for drawing in board.GetDrawings():
        if drawing.GetClass() == "PCB_SHAPE":
            plate_board.AddNative(drawing)

def find_text(board, string):
    for drawing in board.GetDrawings():
        if drawing.GetClass() == "PCB_TEXT":
            if drawing.GetShownText() == string:
                return drawing
    return None

# JCL Text
jlc_string = "JLCJLCJLCJLC"
jlc_text = find_text(board, jlc_string)
if jlc_text:
    existing_jlc_text = find_text(plate_board, jlc_string)
    if existing_jlc_text is None:
        if not positioning_only:
            plate_board.AddNative(jlc_text)
    else:
        position = jlc_text.GetPosition()
        existing_jlc_text.SetPosition(position)

# Footprints
for footprint in board.GetFootprints():
    name = footprint.GetFPIDAsString()
    if re.match(footprint_pattern, name):
        reference = footprint.GetReference()
        existing_footprint = plate_board.FindFootprintByReference(reference)
        if existing_footprint is None:
            if not positioning_only:
                plate_board.AddNative(footprint)
        else:
            position = footprint.GetPosition()
            existing_footprint.SetPosition(position)
            orientation = footprint.GetOrientation()
            existing_footprint.SetOrientation(orientation)

pcbnew.Refresh()
pcbnew.SaveBoard(plate_path, plate_board)
