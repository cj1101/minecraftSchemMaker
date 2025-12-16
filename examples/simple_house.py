"""
Example: Simple House
Creates a basic house structure with walls, floor, and roof.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schematic_api import Schematic
from blocks import OAK_PLANKS, STONE, GLASS, OAK_LOG, BRICKS

# Create a 12x8x12 schematic
s = Schematic(12, 8, 12)

# Stone foundation
s.fill(0, 0, 0, 11, 0, 11, STONE)

# Wooden walls (hollow box)
s.hollow_box(1, 1, 1, 10, 5, 10, OAK_PLANKS)

# Glass windows on each wall
s.fill(3, 2, 1, 4, 3, 1, GLASS)  # Front
s.fill(3, 2, 10, 4, 3, 10, GLASS)  # Back
s.fill(1, 2, 3, 1, 3, 4, GLASS)  # Left
s.fill(10, 2, 3, 10, 3, 4, GLASS)  # Right

# Door frame (remove blocks for door)
s.fill(7, 1, 1, 8, 2, 1, STONE)  # Door opening

# Oak log corner posts
for x in [1, 10]:
    for z in [1, 10]:
        s.fill(x, 1, z, x, 5, z, OAK_LOG)

# Brick roof (pyramid style)
s.fill(0, 6, 0, 11, 6, 11, BRICKS)
s.fill(1, 7, 1, 10, 7, 10, BRICKS)

print(f"House created: {s}")
