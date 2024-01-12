#!/usr/bin/env python3

import argparse
import os
import re
import pcbnew

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--board', type=str, required=True)
parser.add_argument('-p', '--plate', type=str, required=True)
parser.add_argument('--footprint-positioning-only', action='store_true')
parser.add_argument('--footprint-pattern', default="^(Gateron_Low_Profile:.*|kikit:Tab|MountingHole.*:MountingHole.*)", type=str)
args = parser.parse_args()

board_path = args.board
plate_path = args.plate
footprint_positioning_only = args.footprint_positioning_only
footprint_pattern = args.footprint_pattern

board = pcbnew.LoadBoard(board_path)
plate_board = pcbnew.LoadBoard(plate_path) if os.path.exists(plate_path) else pcbnew.CreateEmptyBoard()

if not footprint_positioning_only:
    for drawing in plate_board.GetDrawings():
        if drawing.GetClass() == "PCB_SHAPE":
            plate_board.RemoveNative(drawing)
    for drawing in board.GetDrawings():
        if drawing.GetClass() == "PCB_SHAPE":
            plate_board.AddNative(drawing)

# Update position and orientation only if there is a footprint that has the same reference.
# Otherwise, copy the one on board.
for footprint in board.GetFootprints():
    name = footprint.GetFPIDAsString()
    if re.match(footprint_pattern, name):
        reference = footprint.GetReference()
        existing_footprint = plate_board.FindFootprintByReference(reference)
        if existing_footprint is None:
            if not footprint_positioning_only:
                plate_board.AddNative(footprint)
        else:
            position = footprint.GetPosition()
            existing_footprint.SetPosition(position)
            orientation = footprint.GetOrientation()
            existing_footprint.SetOrientation(orientation)

pcbnew.Refresh()
pcbnew.SaveBoard(plate_path, plate_board)
