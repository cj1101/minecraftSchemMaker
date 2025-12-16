"""
Example: Sphere
Demonstrates the sphere shape generator with different materials.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schematic_api import Schematic
from blocks import GOLD_BLOCK, DIAMOND_BLOCK, GLOWSTONE, GLASS

# Create a 31x31x31 schematic (large enough for spheres)
s = Schematic(31, 31, 31)

# Large golden sphere (solid)
s.sphere(15, 15, 15, 12, GOLD_BLOCK, hollow=False)

# Hollow diamond sphere inside
s.sphere(15, 15, 15, 8, DIAMOND_BLOCK, hollow=True)

# Small glowstone core
s.sphere(15, 15, 15, 3, GLOWSTONE, hollow=False)

# Glass accent spheres at cardinal points
s.sphere(15, 15, 3, 2, GLASS, hollow=False)   # North
s.sphere(15, 15, 27, 2, GLASS, hollow=False)  # South
s.sphere(3, 15, 15, 2, GLASS, hollow=False)   # West
s.sphere(27, 15, 15, 2, GLASS, hollow=False)  # East

print(f"Sphere structure created: {s}")
