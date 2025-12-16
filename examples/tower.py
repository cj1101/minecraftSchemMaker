"""
Example: Tower
Creates a tall tower with multiple floors and a spiral staircase pattern.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schematic_api import Schematic
from blocks import STONE_BRICKS, OAK_PLANKS, GLASS, GLOWSTONE

# Create a 9x30x9 schematic (tall tower)
s = Schematic(9, 30, 9)

# Main tower structure (hollow)
s.hollow_box(0, 0, 0, 8, 29, 8, STONE_BRICKS)

# Add floors every 5 blocks
for y in range(5, 30, 5):
    s.fill(1, y, 1, 7, y, 7, OAK_PLANKS)
    # Leave a hole for stairs in the center
    s.fill(3, y, 3, 5, y, 5, STONE_BRICKS)

# Windows on each floor
for y in range(3, 30, 5):
    # Four windows per floor (one on each wall)
    s.set_block(0, y, 4, GLASS)  # West
    s.set_block(8, y, 4, GLASS)  # East
    s.set_block(4, y, 0, GLASS)  # North
    s.set_block(4, y, 8, GLASS)  # South

# Corner pillars with glowstone lighting
for x in [1, 7]:
    for z in [1, 7]:
        for y in range(1, 30, 6):
            s.set_block(x, y, z, GLOWSTONE)

# Battlements on top
for x in range(0, 9, 2):
    s.set_block(x, 30, 0, STONE_BRICKS)
    s.set_block(x, 30, 8, STONE_BRICKS)
for z in range(0, 9, 2):
    s.set_block(0, 30, z, STONE_BRICKS)
    s.set_block(8, 30, z, STONE_BRICKS)

print(f"Tower created: {s}")
