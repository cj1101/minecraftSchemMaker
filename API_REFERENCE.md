# Minecraft Schematic Builder - Enhanced API Reference

Complete documentation for the enhanced Minecraft Schematic Builder API. This reference contains everything an LLM needs to create incredible, complex structures programmatically using the latest Minecraft 1.21.10 blocks.

## Quick Start

```python
from schematic_api import Schematic
from blocks import STONE_BRICKS, GOLD_BLOCK, GLOWSTONE

# Create a schematic (Width, Height, Length)
s = Schematic(20, 30, 20)

# Build a tower with the new advanced API
s.tower(10, 0, 10, radius=8, height=25, wall_block=STONE_BRICKS, floor_block=GOLD_BLOCK, floors=4)

# Add a glowing spiral on top
s.spiral(10, 10, 26, 30, radius=6, block=GLOWSTONE, turns=3)
```

## Schematic Class

### Constructor

```python
Schematic(width, height, length)
```
Creates a new 3D grid with the specified dimensions initiated with AIR.

---

## Core Building Methods

These are the fundamental methods for placing blocks.

### `set_block(x, y, z, block)`
Place a single block.
*   **Returns:** `self`

### `fill(x1, y1, z1, x2, y2, z2, block)`
Fill a solid rectangular region.
*   **Returns:** `self`

### `hollow_box(x1, y1, z1, x2, y2, z2, block)`
Create a box with walls but no interior content.
*   **Returns:** `self`

### `sphere(cx, cy, cz, radius, block, hollow=False)`
Create a sphere or spherical shell.
*   **Returns:** `self`

### `cylinder(cx, cz, y1, y2, radius, block, hollow=False)`
Create a vertical cylinder or tube.
*   **Returns:** `self`

### `circle(cx, y, cz, radius, block, filled=True)`
Create a horizontal circle or ring.
*   **Returns:** `self`

### `clear()`
Remove all blocks (fill with AIR).
*   **Returns:** `self`

---

## Advanced Structure Generation

These powerful methods automate complex geometry creation.

### `pyramid(x, y, z, base_size, height, block, hollow=False)`
Create a pyramid.
*   `base_size`: Width of the square base.

### `dome(cx, cy, cz, radius, block, hollow=False)`
Create a hemisphere dome.

### `arch(x1, y, z1, x2, z2, height, thickness, block)`
Create an arch connecting two points.
*   `height`: Peak height of the arch relative to `y`.

### `spiral(cx, cz, y_start, y_end, radius, block, turns=2)`
Create a helix/spiral structure.
*   `turns`: Number of full rotations.

### `wall(x1, y1, z1, x2, y2, z2, block, thickness=1, battlements=False)`
Create a straight wall, optionally with crenellations (battlements) on top.

### `staircase(x, y, z, direction, length, block, spiral_center=None)`
Create stairs.
*   `direction`: 'north', 'south', 'east', 'west' (for straight stairs).
*   `spiral_center`: Tuple `(cx, cz)` to create a spiral staircase instead.

### `terrace(x, y, z, width, length, levels, level_height, block)`
Create stacked, shrinking platforms (like a ziggurat or rice terrace).

### `pattern_fill(x1, y1, z1, x2, y2, z2, blocks, pattern='checkerboard')`
Fill a region with a pattern of multiple blocks.
*   `pattern`: 'checkerboard', 'stripes_x', 'stripes_z', 'random'.

### `tree(x, y, z, trunk_height, trunk_block, leaves_block, canopy_radius=3)`
Create a simple procedurally generated tree.

### `tower(x, y, z, radius, height, wall_block, floor_block=None, floors=1)`
Create a complete circular tower with internal floors.

### `bridge(x1, y, z1, x2, z2, width, block, railing_block=None)`
Create a bridge connecting two points, optionally with railings.

### roof(x1, y, z1, x2, z2, block, style='pitched')
Create a roof over a rectangular area.
*   `style`: 'pitched', 'flat', 'dome'.

---

## Interior & Detail Generation

These methods allow for fine-grained control over architectural details and interiors.

### `window(x, y, z, width, height, direction, frame_block=None, glass_block=None, style='simple')`
Create a window with optional frame and various styles.
*   `direction`: 'north', 'south', 'east', 'west'.
*   `style`: 'simple', 'cross', 'grid', 'arch'.

### `window_grid(x1, y1, z1, x2, y2, z2, window_width, window_height, spacing, frame_block, glass_block=None)`
Automatically place a grid of windows along a wall.
*   `spacing`: Number of blocks between windows.

### `door(x, y, z, direction, door_block=None, width=1, height=2, frame_block=None)`
Create a door opening, optionally filled with a block (or AIR) and framed.

### `room(x1, y1, z1, x2, y2, z2, wall_block, floor_block, ceiling_block, windows=True, door_pos=None, window_style='simple')`
Create a complete room with walls, floor, ceiling, and automatically placed windows.
*   `door_pos`: Tuple `(x, y, z)` for the door position.
*   `windows`: If `True`, adds windows to valid walls.

### `furniture(x, y, z, furniture_type, block, direction='north')`
Place procedural furniture.
*   `furniture_type`: 'table', 'chair', 'bed', 'shelf', 'desk'.

### `column(x, y1, z, y2, block, capital_block=None, base_block=None, width=1)`
Create a vertical column with optional capital (top) and base (bottom).
*   `width`: Thickness of the column shaft.

### `floor_pattern(x1, y, z1, x2, z2, blocks, pattern='tile', border_block=None)`
Fill a floor region with a specific pattern.
*   `blocks`: List of blocks to cycle through.
*   `pattern`: 'tile', 'checkerboard', 'diagonal', 'circular', 'random'.

---

## Advanced Geometry

Methods for creating complex mathematical shapes.

### `ellipsoid(cx, cy, cz, radius_x, radius_y, radius_z, block, hollow=False)`
Create an ellipsoid (stretched sphere) with different radii for each axis.

### `cone(x, y, z, base_radius, height, block, hollow=False)`
Create a cone structure.

### `torus(cx, cy, cz, major_radius, minor_radius, block, axis='y')`
Create a torus (donut).
*   `major_radius`: Distance from center to the middle of the ring.
*   `minor_radius`: Radius of the ring tube itself.
*   `axis`: 'x', 'y', or 'z'.

---

## Utility & Logic

Powerful tools for conditional placement and manipulation.

### `fill_if(x1, y1, z1, x2, y2, z2, block, condition_func)`
Fill a region only where a condition is met.
*   `condition_func`: A lambda or function receiving `(x, y, z)` and returning `True`/`False`.
    *   Example: `lambda x, y, z: (x + y + z) % 2 == 0`

### `replace(x1, y1, z1, x2, y2, z2, old_block, new_block)`
Replace all instances of `old_block` with `new_block` in the specified region.

### `copy_region(x1, y1, z1, x2, y2, z2, dest_x, dest_y, dest_z, mirror_x=False, mirror_z=False)`
Copy a rectangular region to a new location.
*   `mirror_x`, `mirror_z`: Mirror the content across the specified axis during the copy.

---

## Comprehensive Block Library (Minecraft 1.21.10)

All blocks are available globally. You do NOT need to import them individually if running inside the server environment, but for clarity/strictness you can import them from `blocks`.

### Basic & Stone
`STONE`, `GRANITE`, `POLISHED_GRANITE`, `DIORITE`, `POLISHED_DIORITE`, `ANDESITE`, `POLISHED_ANDESITE`, `COBBLESTONE`, `MOSSY_COBBLESTONE`, `SMOOTH_STONE`, `BEDROCK`

### Deepslate (1.18+)
`DEEPSLATE`, `COBBLED_DEEPSLATE`, `POLISHED_DEEPSLATE`, `DEEPSLATE_BRICKS`, `DEEPSLATE_TILES`, `CHISELED_DEEPSLATE`

### Tuff (1.21+)
`TUFF`, `POLISHED_TUFF`, `TUFF_BRICKS`, `CHISELED_TUFF`, `CHISELED_TUFF_BRICKS`

### Bricks
`BRICKS` (Red), `STONE_BRICKS`, `MOSSY_STONE_BRICKS`, `CRACKED_STONE_BRICKS`, `CHISELED_STONE_BRICKS`, `MUD_BRICKS`

### Wood (Planks, Logs, Leaves)
**Oak:** `OAK_PLANKS`, `OAK_LOG`, `OAK_LEAVES`
**Spruce:** `SPRUCE_PLANKS`, `SPRUCE_LOG`, `SPRUCE_LEAVES`
**Birch:** `BIRCH_PLANKS`, `BIRCH_LOG`, `BIRCH_LEAVES`
**Jungle:** `JUNGLE_PLANKS`, `JUNGLE_LOG`, `JUNGLE_LEAVES`
**Acacia:** `ACACIA_PLANKS`, `ACACIA_LOG`, `ACACIA_LEAVES`
**Dark Oak:** `DARK_OAK_PLANKS`, `DARK_OAK_LOG`, `DARK_OAK_LEAVES`
**Mangrove:** `MANGROVE_PLANKS`, `MANGROVE_LOG`, `MANGROVE_LEAVES`
**Cherry:** `CHERRY_PLANKS`, `CHERRY_LOG`, `CHERRY_LEAVES`
**Bamboo:** `BAMBOO_PLANKS`, `BAMBOO_BLOCK`
**Nether:** `CRIMSON_PLANKS`, `CRIMSON_STEM`, `WARPED_PLANKS`, `WARPED_STEM`, `AZALEA_LEAVES`

### Concrete (All 16 Colors)
`WHITE_CONCRETE`, `ORANGE_CONCRETE`, `MAGENTA_CONCRETE`, `LIGHT_BLUE_CONCRETE`, `YELLOW_CONCRETE`, `LIME_CONCRETE`, `PINK_CONCRETE`, `GRAY_CONCRETE`, `LIGHT_GRAY_CONCRETE`, `CYAN_CONCRETE`, `PURPLE_CONCRETE`, `BLUE_CONCRETE`, `BROWN_CONCRETE`, `GREEN_CONCRETE`, `RED_CONCRETE`, `BLACK_CONCRETE`

### Terracotta (All 16 Colors)
`TERRACOTTA`, `WHITE_TERRACOTTA`, `ORANGE_TERRACOTTA`, ... (same standard colors as concrete)

### Wool (All 16 Colors)
`WOOL_WHITE`, `WOOL_ORANGE`, `WOOL_MAGENTA`, ... (same standard colors as concrete)

### Glass (All 16 Colors)
`GLASS`, `WHITE_STAINED_GLASS`, `ORANGE_STAINED_GLASS`, ... (same standard colors), plus `TINTED_GLASS`

### Metals & Ores
`IRON_BLOCK`, `GOLD_BLOCK`, `DIAMOND_BLOCK`, `EMERALD_BLOCK`, `NETHERITE_BLOCK`, `COAL_BLOCK`, `REDSTONE_BLOCK`, `LAPIS_BLOCK`, `QUARTZ_BLOCK`, `AMETHYST_BLOCK`

### Copper (1.21+)
`COPPER_BLOCK`, `EXPOSED_COPPER`, `WEATHERED_COPPER`, `OXIDIZED_COPPER`

### Nether
`NETHERRACK`, `NETHER_BRICKS`, `RED_NETHER_BRICKS`, `BASALT`, `BLACKSTONE`, `POLISHED_BLACKSTONE`, `GLOWSTONE`, `SHROOMLIGHT`, `SOUL_SAND`, `QUARTZ_BLOCK`

### End
`END_STONE`, `END_STONE_BRICKS`, `PURPUR_BLOCK`, `PURPUR_PILLAR`

### Aquatic & Nature
`PRISMARINE`, `PRISMARINE_BRICKS`, `DARK_PRISMARINE`, `SEA_LANTERN`, `SPONGE`, `SAND`, `RED_SAND`, `GRAVEL`, `CLAY`, `ICE`, `PACKED_ICE`, `BLUE_ICE`, `SNOW_BLOCK`, `SLIME_BLOCK`, `HONEY_BLOCK`

### Liquids
`WATER`, `LAVA`

---

## Example: The Ultimate Castle

```python
from schematic_api import Schematic
from blocks import *

# 1. Initialize
s = Schematic(60, 40, 60)

# 2. Main Castle Keep (Central Tower)
s.tower(30, 0, 30, radius=10, height=35, wall_block=STONE_BRICKS, floor_block=SPRUCE_PLANKS, floors=5)
# Add a roof to the keep
s.roof(20, 35, 20, 40, 40, DARK_PRISMARINE, style='cone') # Or use pyramid/dome logic

# 3. Outer Walls with Battlements
s.wall(5, 0, 5, 55, 12, 5, STONE_BRICKS, thickness=2, battlements=True)
s.wall(5, 0, 55, 55, 12, 55, STONE_BRICKS, thickness=2, battlements=True)
s.wall(5, 0, 5, 5, 12, 55, STONE_BRICKS, thickness=2, battlements=True)
s.wall(55, 0, 5, 55, 12, 55, STONE_BRICKS, thickness=2, battlements=True)

# 4. Corner Watchtowers
for x, z in [(5, 5), (5, 55), (55, 5), (55, 55)]:
    s.tower(x, 0, z, radius=5, height=18, wall_block=COBBLED_DEEPSLATE, floor_block=OAK_PLANKS, floors=2)
    s.dome(x, 18, z, 5, OXIDIZED_COPPER, hollow=True)

# 5. Gatehouse with Arch
s.hollow_box(25, 0, 5, 35, 12, 10, STONE_BRICKS)
s.arch(27, 0, 5, 33, 5, height=8, thickness=6, block=AIR) # Cut out the gate

# 6. Gardens with Trees
s.tree(15, 0, 15, 5, OAK_LOG, CHERRY_LEAVES)
s.tree(45, 0, 15, 6, BIRCH_LOG, BIRCH_LEAVES)
s.tree(15, 0, 45, 5, SPRUCE_LOG, SPRUCE_LEAVES)
s.tree(45, 0, 45, 7, JUNGLE_LOG, JUNGLE_LEAVES)

# 7. Decorative Paths
s.fill(28, 0, 10, 32, 0, 30, DIRT_PATH)
```

## Tips for Best Results

*   **Combine Primitives:** Don't just make a box. Make a box, then add a `roof`, then add `towers` at the corners, then cut out `arches` for windows.
*   **Use the New Blocks:** Use `COPPER` that oxidizes, or `DEEPSLATE` for a darker, sturdier feel, or `CHERRY` wood for a pink aesthetic.
*   **Layering:** Build the terrain first (if any), then the foundations, then the walls, then the roof, then the details.
*   **Method Chaining:** `s.fill(...).tower(...).dome(...)` works perfectly and keeps code clean.
