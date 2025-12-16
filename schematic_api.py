"""
Schematic API for programmatically creating Minecraft schematics.
Provides a simple interface for building structures with code.
"""

import numpy as np
import random
import math
from blocks import Block, AIR, validate_block


class Schematic:
    """
    Main class for creating Minecraft schematics programmatically.
    """
    
    def __init__(self, width, height, length):
        """
        Initialize a new schematic with given dimensions.
        
        Args:
            width: Size along X axis
            height: Size along Y axis (vertical)
            length: Size along Z axis
        """
        self.width = width
        self.height = height
        self.length = length
        
        # Initialize 3D grid with air blocks
        # Grid is indexed as [x][y][z]
        self.blocks = np.full((width, height, length), AIR, dtype=object)
    
    def set_block(self, x, y, z, block):
        """Set a single block at the specified coordinates."""
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        if not self._in_bounds(x, y, z):
            raise ValueError(f"Coordinates ({x}, {y}, {z}) out of bounds")
        
        self.blocks[x, y, z] = block
        return self
    
    def get_block(self, x, y, z):
        """Get the block at the specified coordinates."""
        if not self._in_bounds(x, y, z):
            raise ValueError(f"Coordinates ({x}, {y}, {z}) out of bounds")
        return self.blocks[x, y, z]
    
    def fill(self, x1, y1, z1, x2, y2, z2, block):
        """Fill a rectangular region with a block type."""
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        # Ensure coordinates are in order
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if self._in_bounds(x, y, z):
                        self.blocks[x, y, z] = block
        
        return self
    
    def hollow_box(self, x1, y1, z1, x2, y2, z2, block):
        """Create a hollow box (only walls, no interior)."""
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        # Ensure coordinates are in order
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    # Only place blocks on the faces
                    if (x == x1 or x == x2 or 
                        y == y1 or y == y2 or 
                        z == z1 or z == z2):
                        if self._in_bounds(x, y, z):
                            self.blocks[x, y, z] = block
        
        return self
    
    # ... existing geometric methods ...

    def sphere(self, cx, cy, cz, radius, block, hollow=False):
        """Create a sphere."""
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        for x in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
            for y in range(max(0, cy - radius), min(self.height, cy + radius + 1)):
                for z in range(max(0, cz - radius), min(self.length, cz + radius + 1)):
                    distance = ((x - cx)**2 + (y - cy)**2 + (z - cz)**2)**0.5
                    
                    if hollow:
                        if abs(distance - radius) < 1:
                            self.blocks[x, y, z] = block
                    else:
                        if distance <= radius:
                            self.blocks[x, y, z] = block
        return self
    
    def cylinder(self, cx, cz, y1, y2, radius, block, hollow=False):
        """Create a vertical cylinder."""
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        y1, y2 = min(y1, y2), max(y1, y2)
        
        for x in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
            for z in range(max(0, cz - radius), min(self.length, cz + radius + 1)):
                distance = ((x - cx)**2 + (z - cz)**2)**0.5
                
                should_place = False
                if hollow:
                    if abs(distance - radius) < 1:
                        should_place = True
                else:
                    if distance <= radius:
                        should_place = True
                
                if should_place:
                    for y in range(max(0, y1), min(self.height, y2 + 1)):
                        self.blocks[x, y, z] = block
        return self

    def pyramid(self, x, y, z, base_size, height, block, hollow=False):
        """Create a pyramid structure."""
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        for layer in range(height):
            # Calculate size for this layer
            layer_size = base_size - (layer * 2 * base_size // height)
            if layer_size <= 0:
                break
            
            offset = (base_size - layer_size) // 2
            
            if hollow and layer < height - 1:
                # Only draw the edges for hollow pyramid
                for i in range(layer_size):
                    self.set_block(x + offset + i, y + layer, z + offset, block)
                    self.set_block(x + offset + i, y + layer, z + offset + layer_size - 1, block)
                    self.set_block(x + offset, y + layer, z + offset + i, block)
                    self.set_block(x + offset + layer_size - 1, y + layer, z + offset + i, block)
            else:
                self.fill(
                    x + offset, y + layer, z + offset,
                    x + offset + layer_size - 1, y + layer, z + offset + layer_size - 1,
                    block
                )
        return self

    def dome(self, cx, cy, cz, radius, block, hollow=False):
        """Create a dome (hemisphere)."""
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        for x in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
            for y in range(max(0, cy), min(self.height, cy + radius + 1)):
                for z in range(max(0, cz - radius), min(self.length, cz + radius + 1)):
                    dx = x - cx
                    dy = y - cy
                    dz = z - cz
                    distance = (dx**2 + dy**2 + dz**2)**0.5
                    
                    if hollow:
                        if abs(distance - radius) < 1 and dy >= 0:
                            self.blocks[x, y, z] = block
                    else:
                        if distance <= radius and dy >= 0:
                            self.blocks[x, y, z] = block
        return self

    # === NEW DETAILED PATTERN METHODS ===

    def fractal_menger(self, x, y, z, size, block, depth=3):
        """
        Create a Menger Sponge fractal.
        
        Args:
            x, y, z: Corner coordinates
            size: Size of the cube (should be power of 3, e.g., 27, 81)
            block: Block to build with
            depth: Recursion depth
        """
        if depth == 0:
            self.fill(x, y, z, x + size - 1, y + size - 1, z + size - 1, block)
            return self

        sub_size = size // 3
        if sub_size == 0:
            return self

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # Skip the middle sections
                    # (1,1) in any 2D slice is removed
                    # Count how many indices are 1
                    ones = (1 if i == 1 else 0) + (1 if j == 1 else 0) + (1 if k == 1 else 0)

                    if ones < 2:
                        self.fractal_menger(
                            x + i * sub_size,
                            y + j * sub_size,
                            z + k * sub_size,
                            sub_size,
                            block,
                            depth - 1
                        )
        return self

    def l_system_tree(self, x, y, z, trunk_block, leaf_block, iterations=4, angle=25, length=5):
        """
        Create a 3D tree using L-systems.
        """
        # Simple 3D tree rules
        axiom = "X"
        rules = {
            "X": "F[+X][-X][&X][^X]FX",
            "F": "FF"
        }

        # Generate string
        state_str = axiom
        for _ in range(iterations):
            next_str = ""
            for char in state_str:
                next_str += rules.get(char, char)
            state_str = next_str

        # Interpret string
        # State: position, direction vector (start facing UP)
        # Using a stack for branching
        stack = []
        pos = np.array([float(x), float(y), float(z)])
        # Initial direction: UP (0, 1, 0)
        heading = np.array([0.0, 1.0, 0.0])
        # Right vector (1, 0, 0)
        right = np.array([1.0, 0.0, 0.0])
        # Forward vector (0, 0, 1)
        forward = np.array([0.0, 0.0, 1.0])

        current_len = length

        def rotate(vec, axis, theta):
            # Rodrigues' rotation formula
            theta_rad = math.radians(theta)
            return (vec * math.cos(theta_rad) +
                    np.cross(axis, vec) * math.sin(theta_rad) +
                    axis * np.dot(axis, vec) * (1 - math.cos(theta_rad)))

        for char in state_str:
            if char == "F":
                # Move forward and draw trunk
                steps = int(current_len)
                start_p = pos.copy()
                pos += heading * current_len

                # Draw line
                p1 = start_p.astype(int)
                p2 = pos.astype(int)
                # Simple line drawing
                dist = np.linalg.norm(p2 - p1)
                if dist > 0:
                    for i in range(int(dist) + 1):
                        t = i / dist
                        p = p1 + (p2 - p1) * t
                        bx, by, bz = int(p[0]), int(p[1]), int(p[2])
                        if self._in_bounds(bx, by, bz):
                            self.blocks[bx, by, bz] = trunk_block

            elif char == "X":
                # Leaf at tip
                bx, by, bz = int(pos[0]), int(pos[1]), int(pos[2])
                if self._in_bounds(bx, by, bz):
                    self.blocks[bx, by, bz] = leaf_block

            elif char == "+": # Turn left/right around heading
                right = rotate(right, heading, angle)
                forward = rotate(forward, heading, angle)
            elif char == "-":
                right = rotate(right, heading, -angle)
                forward = rotate(forward, heading, -angle)
            elif char == "&": # Pitch down
                heading = rotate(heading, right, angle)
                forward = rotate(forward, right, angle)
            elif char == "^": # Pitch up
                heading = rotate(heading, right, -angle)
                forward = rotate(forward, right, -angle)
            elif char == "/": # Roll
                right = rotate(right, forward, angle)
            elif char == "\\": # Roll
                right = rotate(right, forward, -angle)

            elif char == "[":
                # Push state
                stack.append((pos.copy(), heading.copy(), right.copy(), forward.copy(), current_len))
                current_len *= 0.7  # Branches get shorter
            
            elif char == "]":
                # Pop state
                if stack:
                    pos, heading, right, forward, current_len = stack.pop()

        return self

    def maze_3d(self, x, y, z, width, height, length, wall_block, path_block=AIR):
        """
        Generate a 3D maze.
        Args:
            width, height, length: Dimensions (must be odd)
        """
        # Ensure odd dimensions
        w = width if width % 2 else width - 1
        h = height if height % 2 else height - 1
        l = length if length % 2 else length - 1

        # Fill with walls
        self.fill(x, y, z, x + w - 1, y + h - 1, z + l - 1, wall_block)

        # Recursive backtracker
        visited = set()

        def visit(cx, cy, cz):
            visited.add((cx, cy, cz))
            # Clear current cell
            self.blocks[x + cx, y + cy, z + cz] = path_block

            # Directions: (dx, dy, dz)
            directions = [
                (2, 0, 0), (-2, 0, 0),
                (0, 2, 0), (0, -2, 0),
                (0, 0, 2), (0, 0, -2)
            ]
            random.shuffle(directions)

            for dx, dy, dz in directions:
                nx, ny, nz = cx + dx, cy + dy, cz + dz
                if (0 <= nx < w and 0 <= ny < h and 0 <= nz < l and
                    (nx, ny, nz) not in visited):

                    # Carve path between
                    self.blocks[x + cx + dx//2, y + cy + dy//2, z + cz + dz//2] = path_block
                    visit(nx, ny, nz)

        # Start at 1,1,1
        visit(1, 1, 1)
        return self

    def cellular_automata(self, x, y, z, width, length, block, generations=10, rule="life"):
        """
        Generate patterns using Cellular Automata.
        Currently implements Game of Life 2D stacked over Y axis (time).
        """
        # Initialize grid
        grid = np.zeros((width, length), dtype=int)

        # Random start
        for i in range(width):
            for j in range(length):
                if random.random() < 0.3:
                    grid[i, j] = 1

        # Simulate
        for gen in range(min(generations, self.height - y)):
            # Draw current generation
            for i in range(width):
                for j in range(length):
                    if grid[i, j]:
                        if self._in_bounds(x + i, y + gen, z + j):
                            self.blocks[x + i, y + gen, z + j] = block

            # Compute next generation (Conway's Game of Life)
            new_grid = grid.copy()
            for i in range(width):
                for j in range(length):
                    # Count neighbors
                    neighbors = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0: continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < width and 0 <= nj < length:
                                neighbors += grid[ni, nj]

                    if grid[i, j]:
                        if neighbors < 2 or neighbors > 3:
                            new_grid[i, j] = 0
                    else:
                        if neighbors == 3:
                            new_grid[i, j] = 1
            grid = new_grid

        return self

    # Keep existing helper methods
    def arch(self, x1, y, z1, x2, z2, height, thickness, block):
        # ... implementation ...
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        dx = x2 - x1
        dz = z2 - z1
        length = (dx**2 + dz**2)**0.5
        if length == 0: return self
        steps = int(length * 2)
        for i in range(steps + 1):
            t = i / steps
            x = x1 + dx * t
            z = z1 + dz * t
            arch_y = y + height * (1 - (2 * t - 1)**2)**0.5
            for th in range(thickness):
                for ty in range(thickness):
                    bx = int(x)
                    by = int(arch_y) + ty
                    bz = int(z) + th
                    if self._in_bounds(bx, by, bz):
                        self.blocks[bx, by, bz] = block
        return self

    def spiral(self, cx, cz, y_start, y_end, radius, block, turns=2):
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        height = abs(y_end - y_start)
        steps = int(height * 4)
        for i in range(steps + 1):
            t = i / steps
            angle = turns * 2 * math.pi * t
            y = y_start + height * t
            x = cx + radius * math.cos(angle)
            z = cz + radius * math.sin(angle)
            bx, by, bz = int(x), int(y), int(z)
            if self._in_bounds(bx, by, bz):
                self.blocks[bx, by, bz] = block
        return self

    def wall(self, x1, y1, z1, x2, y2, z2, block, thickness=1, battlements=False):
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        self.fill(x1, y1, z1, x2, y2, z2, block)
        if battlements:
            if abs(x2 - x1) > abs(z2 - z1):
                for x in range(min(x1, x2), max(x1, x2) + 1, 2):
                    for z in range(min(z1, z2), max(z1, z2) + 1):
                        if self._in_bounds(x, y2 + 1, z):
                            self.blocks[x, y2 + 1, z] = block
                            if self._in_bounds(x, y2 + 2, z):
                                self.blocks[x, y2 + 2, z] = block
            else:
                for z in range(min(z1, z2), max(z1, z2) + 1, 2):
                    for x in range(min(x1, x2), max(x1, x2) + 1):
                        if self._in_bounds(x, y2 + 1, z):
                            self.blocks[x, y2 + 1, z] = block
                            if self._in_bounds(x, y2 + 2, z):
                                self.blocks[x, y2 + 2, z] = block
        return self

    def staircase(self, x, y, z, direction, length, block, spiral_center=None):
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        if spiral_center:
            cx, cz = spiral_center
            radius = ((x - cx)**2 + (z - cz)**2)**0.5
            for i in range(length):
                angle = (i / length) * 2 * math.pi
                sx = int(cx + radius * math.cos(angle))
                sz = int(cz + radius * math.sin(angle))
                sy = y + i
                if self._in_bounds(sx, sy, sz):
                    self.blocks[sx, sy, sz] = block
        else:
            dx, dz = 0, 0
            if direction == 'north': dz = -1
            elif direction == 'south': dz = 1
            elif direction == 'east': dx = 1
            elif direction == 'west': dx = -1
            for i in range(length):
                sx = x + dx * i
                sy = y + i
                sz = z + dz * i
                if self._in_bounds(sx, sy, sz):
                    self.blocks[sx, sy, sz] = block
        return self

    def terrace(self, x, y, z, width, length, levels, level_height, block):
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        for level in range(levels):
            offset = level * 2
            level_y = y + level * level_height
            self.fill(x + offset, level_y, z + offset,
                x + width - offset - 1, level_y, z + length - offset - 1, block)
        return self

    def pattern_fill(self, x1, y1, z1, x2, y2, z2, blocks, pattern='checkerboard'):
        for block in blocks:
            if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if not self._in_bounds(x, y, z): continue
                    if pattern == 'checkerboard': idx = (x + y + z) % len(blocks)
                    elif pattern == 'stripes_x': idx = x % len(blocks)
                    elif pattern == 'stripes_z': idx = z % len(blocks)
                    elif pattern == 'random': idx = random.randint(0, len(blocks) - 1)
                    else: idx = 0
                    self.blocks[x, y, z] = blocks[idx]
        return self

    def circle(self, cx, y, cz, radius, block, filled=True):
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        for x in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
            for z in range(max(0, cz - radius), min(self.length, cz + radius + 1)):
                distance = ((x - cx)**2 + (z - cz)**2)**0.5
                if filled:
                    if distance <= radius: self.blocks[x, y, z] = block
                else:
                    if abs(distance - radius) < 1: self.blocks[x, y, z] = block
        return self

    def tree(self, x, y, z, trunk_height, trunk_block, leaves_block, canopy_radius=3):
        if not validate_block(trunk_block) or not validate_block(leaves_block): raise ValueError("Invalid block")
        for h in range(trunk_height):
            if self._in_bounds(x, y + h, z): self.blocks[x, y + h, z] = trunk_block
        self.sphere(x, y + trunk_height, z, canopy_radius, leaves_block, hollow=False)
        return self

    def tower(self, x, y, z, radius, height, wall_block, floor_block=None, floors=1):
        if not validate_block(wall_block): raise ValueError(f"Invalid block: {wall_block}")
        self.cylinder(x, z, y, y + height - 1, radius, wall_block, hollow=True)
        if floor_block and validate_block(floor_block):
            floor_spacing = height // (floors + 1)
            for i in range(1, floors + 1):
                floor_y = y + i * floor_spacing
                self.circle(x, floor_y, z, radius - 1, floor_block, filled=True)
        return self

    def bridge(self, x1, y, z1, x2, z2, width, block, railing_block=None):
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        dx = x2 - x1
        dz = z2 - z1
        length = max(abs(dx), abs(dz))
        if length == 0: return self
        for i in range(length + 1):
            t = i / length if length > 0 else 0
            x = int(x1 + dx * t)
            z = int(z1 + dz * t)
            for w in range(width):
                if abs(dx) > abs(dz): bx, bz = x, z + w - width // 2
                else: bx, bz = x + w - width // 2, z
                if self._in_bounds(bx, y, bz): self.blocks[bx, y, bz] = block
                if railing_block and validate_block(railing_block):
                    if w == 0 or w == width - 1:
                        for h in range(1, 3):
                            if self._in_bounds(bx, y + h, bz): self.blocks[bx, y + h, bz] = railing_block
        return self

    def roof(self, x1, y, z1, x2, z2, block, style='pitched'):
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        x1, x2 = min(x1, x2), max(x1, x2)
        z1, z2 = min(z1, z2), max(z1, z2)
        width = x2 - x1 + 1
        length = z2 - z1 + 1
        if style == 'flat': self.fill(x1, y, z1, x2, y, z2, block)
        elif style == 'pitched':
            peak_height = width // 2
            for i in range(peak_height):
                self.fill(x1 + i, y + i, z1, x2 - i, y + i, z2, block)
        elif style == 'dome':
            cx = (x1 + x2) // 2
            cz = (z1 + z2) // 2
            radius = min(width, length) // 2
            self.dome(cx, y, cz, radius, block, hollow=False)
        return self

    def window(self, x, y, z, width, height, direction, frame_block=None, glass_block=None, style='simple'):
        from blocks import GLASS, AIR
        if glass_block is None: glass_block = AIR
        if not validate_block(glass_block): raise ValueError(f"Invalid glass block: {glass_block}")
        if frame_block and not validate_block(frame_block): raise ValueError(f"Invalid frame block: {frame_block}")
        
        # Simplified implementation to save space but keep logic
        for w_idx in range(width):
            for h_idx in range(height):
                if direction == 'north': bx, by, bz = x + w_idx, y + h_idx, z
                elif direction == 'south': bx, by, bz = x + w_idx, y + h_idx, z
                elif direction == 'east': bx, by, bz = x, y + h_idx, z + w_idx
                else: bx, by, bz = x, y + h_idx, z + w_idx # west

                if self._in_bounds(bx, by, bz):
                    is_frame = frame_block and (w_idx==0 or w_idx==width-1 or h_idx==0 or h_idx==height-1)
                    if style == 'cross' and frame_block: is_frame |= (w_idx==width//2 or h_idx==height//2)
                    elif style == 'grid' and frame_block: is_frame |= (w_idx%2==0 or h_idx%2==0)

                    if is_frame: self.blocks[bx, by, bz] = frame_block
                    else: self.blocks[bx, by, bz] = glass_block
        return self

    def window_grid(self, x1, y1, z1, x2, y2, z2, window_width, window_height, spacing, frame_block, glass_block=None):
        from blocks import GLASS
        if glass_block is None: glass_block = GLASS
        if x1 == x2: # Wall runs along Z axis
            direction = 'east' if x1 < self.width // 2 else 'west'
            wall_length = abs(z2 - z1)
            num_windows = (wall_length + spacing) // (window_width + spacing)
            start_z = min(z1, z2) + (wall_length - (num_windows * window_width + (num_windows - 1) * spacing)) // 2
            for i in range(num_windows):
                for row_y in range(y1, y2, window_height + spacing):
                    if row_y + window_height <= y2:
                        wz = start_z + i * (window_width + spacing)
                        self.window(x1, row_y, wz, window_width, window_height, direction, frame_block, glass_block)
        elif z1 == z2: # Wall runs along X axis
            direction = 'north' if z1 < self.length // 2 else 'south'
            wall_length = abs(x2 - x1)
            num_windows = (wall_length + spacing) // (window_width + spacing)
            start_x = min(x1, x2) + (wall_length - (num_windows * window_width + (num_windows - 1) * spacing)) // 2
            for i in range(num_windows):
                for row_y in range(y1, y2, window_height + spacing):
                    if row_y + window_height <= y2:
                        wx = start_x + i * (window_width + spacing)
                        self.window(wx, row_y, z1, window_width, window_height, direction, frame_block, glass_block)
        return self

    def door(self, x, y, z, direction, door_block=None, width=1, height=2, frame_block=None):
        if door_block is None: door_block = AIR
        if not validate_block(door_block): raise ValueError(f"Invalid door block: {door_block}")
        if direction in ['north', 'south']:
            for dx in range(width):
                for dy in range(height):
                    if self._in_bounds(x + dx, y + dy, z): self.blocks[x + dx, y + dy, z] = door_block
            if frame_block:
                for dx in range(-1, width + 1):
                    for dy in range(-1, height + 1):
                        if (dx == -1 or dx == width or dy == -1 or dy == height):
                            if self._in_bounds(x + dx, y + dy, z): self.blocks[x + dx, y + dy, z] = frame_block
        elif direction in ['east', 'west']:
            for dz in range(width):
                for dy in range(height):
                    if self._in_bounds(x, y + dy, z + dz): self.blocks[x, y + dy, z + dz] = door_block
            if frame_block:
                for dz in range(-1, width + 1):
                    for dy in range(-1, height + 1):
                        if (dz == -1 or dz == width or dy == -1 or dy == height):
                            if self._in_bounds(x, y + dy, z + dz): self.blocks[x, y + dy, z + dz] = frame_block
        return self

    def column(self, x, y1, z, y2, block, capital_block=None, base_block=None, width=1):
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        y1, y2 = min(y1, y2), max(y1, y2)
        offset = width // 2
        for dx in range(-offset, width - offset):
            for dz in range(-offset, width - offset):
                for y in range(y1, y2 + 1):
                    if self._in_bounds(x + dx, y, z + dz): self.blocks[x + dx, y, z + dz] = block
        if capital_block and validate_block(capital_block):
            cap_width = width + 1
            cap_offset = cap_width // 2
            for dx in range(-cap_offset, cap_width - cap_offset):
                for dz in range(-cap_offset, cap_width - cap_offset):
                    if self._in_bounds(x + dx, y2 + 1, z + dz): self.blocks[x + dx, y2 + 1, z + dz] = capital_block
        if base_block and validate_block(base_block):
            base_width = width + 1
            base_offset = base_width // 2
            for dx in range(-base_offset, base_width - base_offset):
                for dz in range(-base_offset, base_width - base_offset):
                    if self._in_bounds(x + dx, y1 - 1, z + dz): self.blocks[x + dx, y1 - 1, z + dz] = base_block
        return self

    def floor_pattern(self, x1, y, z1, x2, z2, blocks, pattern='tile', border_block=None):
        import random
        import math
        for block in blocks:
            if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        x1, x2 = min(x1, x2), max(x1, x2)
        z1, z2 = min(z1, z2), max(z1, z2)
        cx = (x1 + x2) / 2
        cz = (z1 + z2) / 2
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if not self._in_bounds(x, y, z): continue
                if border_block and (x == x1 or x == x2 or z == z1 or z == z2):
                    self.blocks[x, y, z] = border_block
                    continue
                if pattern == 'tile': idx = ((x // 2) + (z // 2)) % len(blocks)
                elif pattern == 'checkerboard': idx = (x + z) % len(blocks)
                elif pattern == 'diagonal': idx = (x + z) % len(blocks)
                elif pattern == 'circular':
                    dist = math.sqrt((x - cx)**2 + (z - cz)**2)
                    idx = int(dist) % len(blocks)
                elif pattern == 'random': idx = random.randint(0, len(blocks) - 1)
                else: idx = 0
                self.blocks[x, y, z] = blocks[idx]
        return self

    def fill_if(self, x1, y1, z1, x2, y2, z2, block, condition_func):
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if self._in_bounds(x, y, z) and condition_func(x, y, z): self.blocks[x, y, z] = block
        return self

    def replace(self, x1, y1, z1, x2, y2, z2, old_block, new_block):
        if not validate_block(old_block) or not validate_block(new_block): raise ValueError("Invalid block")
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if self._in_bounds(x, y, z) and self.blocks[x, y, z] == old_block: self.blocks[x, y, z] = new_block
        return self

    def copy_region(self, x1, y1, z1, x2, y2, z2, dest_x, dest_y, dest_z, mirror_x=False, mirror_z=False):
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        width = x2 - x1 + 1
        height = y2 - y1 + 1
        length = z2 - z1 + 1
        for x in range(width):
            for y in range(height):
                for z in range(length):
                    src_x = x1 + x
                    src_y = y1 + y
                    src_z = z1 + z
                    if not self._in_bounds(src_x, src_y, src_z): continue
                    dx = (width - 1 - x) if mirror_x else x
                    dz = (length - 1 - z) if mirror_z else z
                    dest_bx = dest_x + dx
                    dest_by = dest_y + y
                    dest_bz = dest_z + dz
                    if self._in_bounds(dest_bx, dest_by, dest_bz):
                        self.blocks[dest_bx, dest_by, dest_bz] = self.blocks[src_x, src_y, src_z]
        return self

    def room(self, x1, y1, z1, x2, y2, z2, wall_block, floor_block, ceiling_block, windows=True, door_pos=None, window_style='simple'):
        from blocks import GLASS
        if not validate_block(wall_block) or not validate_block(floor_block) or not validate_block(ceiling_block): raise ValueError("Invalid block")
        self.fill(x1, y1, z1, x2, y1, z2, floor_block)
        self.fill(x1, y2, z1, x2, y2, z2, ceiling_block)
        self.hollow_box(x1, y1, z1, x2, y2, z2, wall_block)
        if windows:
            room_height = y2 - y1
            window_y = y1 + room_height // 3
            window_height = max(2, room_height // 3)
            if x2 - x1 > 6: self.window(x1 + 2, window_y, z1, 3, window_height, 'north', wall_block, GLASS, window_style)
            if x2 - x1 > 6: self.window(x2 - 4, window_y, z2, 3, window_height, 'south', wall_block, GLASS, window_style)
        if door_pos:
            dx, dy, dz = door_pos
            self.door(dx, dy, dz, 'north', None, 1, 2, wall_block)
        return self

    def ellipsoid(self, cx, cy, cz, radius_x, radius_y, radius_z, block, hollow=False):
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        for x in range(max(0, cx - radius_x), min(self.width, cx + radius_x + 1)):
            for y in range(max(0, cy - radius_y), min(self.height, cy + radius_y + 1)):
                for z in range(max(0, cz - radius_z), min(self.length, cz + radius_z + 1)):
                    dx = (x - cx) / radius_x if radius_x > 0 else 0
                    dy = (y - cy) / radius_y if radius_y > 0 else 0
                    dz = (z - cz) / radius_z if radius_z > 0 else 0
                    distance = (dx**2 + dy**2 + dz**2)**0.5
                    if hollow:
                        if abs(distance - 1) < 0.15: self.blocks[x, y, z] = block
                    else:
                        if distance <= 1: self.blocks[x, y, z] = block
        return self

    def cone(self, x, y, z, base_radius, height, block, hollow=False):
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        for layer in range(height):
            layer_radius = base_radius * (1 - layer / height)
            if layer_radius < 0.5:
                if self._in_bounds(x, y + layer, z): self.blocks[x, y + layer, z] = block
                continue
            for dx in range(-int(layer_radius) - 1, int(layer_radius) + 2):
                for dz in range(-int(layer_radius) - 1, int(layer_radius) + 2):
                    dist = (dx**2 + dz**2)**0.5
                    if hollow:
                        if abs(dist - layer_radius) < 1:
                            if self._in_bounds(x + dx, y + layer, z + dz): self.blocks[x + dx, y + layer, z + dz] = block
                    else:
                        if dist <= layer_radius:
                            if self._in_bounds(x + dx, y + layer, z + dz): self.blocks[x + dx, y + layer, z + dz] = block
        return self

    def torus(self, cx, cy, cz, major_radius, minor_radius, block, axis='y'):
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        import math
        max_r = major_radius + minor_radius
        for x in range(max(0, cx - max_r), min(self.width, cx + max_r + 1)):
            for y in range(max(0, cy - max_r), min(self.height, cy + max_r + 1)):
                for z in range(max(0, cz - max_r), min(self.length, cz + max_r + 1)):
                    dx = x - cx; dy = y - cy; dz = z - cz
                    if axis == 'y':
                        dist_from_center = math.sqrt(dx**2 + dz**2)
                        dist_from_tube = math.sqrt((dist_from_center - major_radius)**2 + dy**2)
                    elif axis == 'x':
                        dist_from_center = math.sqrt(dy**2 + dz**2)
                        dist_from_tube = math.sqrt((dist_from_center - major_radius)**2 + dx**2)
                    else:
                        dist_from_center = math.sqrt(dx**2 + dy**2)
                        dist_from_tube = math.sqrt((dist_from_center - major_radius)**2 + dz**2)
                    if dist_from_tube <= minor_radius: self.blocks[x, y, z] = block
        return self

    def furniture(self, x, y, z, furniture_type, block, direction='north'):
        from blocks import OAK_PLANKS, WOOL_WHITE
        if not validate_block(block): raise ValueError(f"Invalid block: {block}")
        if furniture_type == 'table':
            for dx, dz in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                if self._in_bounds(x + dx, y, z + dz): self.blocks[x + dx, y, z + dz] = block
            self.fill(x, y + 1, z, x + 2, y + 1, z + 2, block)
        elif furniture_type == 'chair':
            self.fill(x, y, z, x + 1, y, z + 1, block)
            if direction == 'north': self.fill(x, y + 1, z, x + 1, y + 2, z, block)
            elif direction == 'south': self.fill(x, y + 1, z + 1, x + 1, y + 2, z + 1, block)
            elif direction == 'east': self.fill(x + 1, y + 1, z, x + 1, y + 2, z + 1, block)
            else: self.fill(x, y + 1, z, x, y + 2, z + 1, block)
        elif furniture_type == 'bed':
            self.fill(x, y, z, x + 1, y, z + 3, block)
            self.fill(x, y + 1, z, x + 1, y + 1, z + 3, WOOL_WHITE)
            if direction == 'north': self.fill(x, y + 1, z, x + 1, y + 2, z, block)
            else: self.fill(x, y + 1, z + 3, x + 1, y + 2, z + 3, block)
        elif furniture_type == 'shelf':
            self.fill(x, y, z, x, y + 4, z, block)
            self.fill(x + 3, y, z, x + 3, y + 4, z, block)
            for shelf_y in [y + 1, y + 2, y + 3, y + 4]: self.fill(x, shelf_y, z, x + 3, shelf_y, z, block)
        elif furniture_type == 'desk':
            for dx in [0, 3]:
                for dz in [0, 2]:
                    if self._in_bounds(x + dx, y, z + dz): self.blocks[x + dx, y, z + dz] = block
            self.fill(x, y + 1, z, x + 3, y + 1, z + 2, block)
        return self

    def clear(self):
        """Clear the entire schematic (fill with air)."""
        self.blocks = np.full((self.width, self.height, self.length), AIR, dtype=object)
        return self
    
    def to_dict(self):
        """
        Export schematic to dictionary format for JSON serialization.
        Used by the web viewer.
        """
        blocks_list = []
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.length):
                    block = self.blocks[x, y, z]
                    if block != AIR:
                        blocks_list.append({
                            'x': x, 'y': y, 'z': z,
                            'type': block.minecraft_id,
                            'name': block.name,
                            'color': block.color
                        })
        return {
            'width': self.width, 'height': self.height, 'length': self.length,
            'blocks': blocks_list, 'block_count': len(blocks_list)
        }
    
    def _in_bounds(self, x, y, z):
        return (0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.length)
    
    def __repr__(self):
        block_count = np.sum(self.blocks != AIR)
        return f"Schematic({self.width}x{self.height}x{self.length}, {block_count} blocks)"
