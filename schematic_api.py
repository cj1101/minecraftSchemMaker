"""
Schematic API for programmatically creating Minecraft schematics.
Provides a simple interface for building structures with code.
"""

import numpy as np
from blocks import Block, AIR, validate_block


class Schematic:
    """
    Main class for creating Minecraft schematics programmatically.
    
    Example:
        >>> from schematic_api import Schematic
        >>> from blocks import STONE, GLASS
        >>> s = Schematic(10, 10, 10)
        >>> s.fill(0, 0, 0, 9, 0, 9, STONE)  # Floor
        >>> s.hollow_box(2, 1, 2, 7, 5, 7, GLASS)  # Glass room
        >>> s.export("my_structure.schem")
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
        """
        Set a single block at the specified coordinates.
        
        Args:
            x, y, z: Coordinates (0-indexed)
            block: Block object to place
            
        Returns:
            self (for method chaining)
        """
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
        """
        Fill a rectangular region with a block type.
        
        Args:
            x1, y1, z1: Starting corner coordinates
            x2, y2, z2: Ending corner coordinates (inclusive)
            block: Block to fill with
            
        Returns:
            self (for method chaining)
        """
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
        """
        Create a hollow box (only walls, no interior).
        
        Args:
            x1, y1, z1: Starting corner coordinates
            x2, y2, z2: Ending corner coordinates (inclusive)
            block: Block to build walls with
            
        Returns:
            self (for method chaining)
        """
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
    
    def sphere(self, cx, cy, cz, radius, block, hollow=False):
        """
        Create a sphere.
        
        Args:
            cx, cy, cz: Center coordinates
            radius: Radius of the sphere
            block: Block to build with
            hollow: If True, only create the shell
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        for x in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
            for y in range(max(0, cy - radius), min(self.height, cy + radius + 1)):
                for z in range(max(0, cz - radius), min(self.length, cz + radius + 1)):
                    distance = ((x - cx)**2 + (y - cy)**2 + (z - cz)**2)**0.5
                    
                    if hollow:
                        # Only place blocks on the surface (within 1 block of radius)
                        if abs(distance - radius) < 1:
                            self.blocks[x, y, z] = block
                    else:
                        # Fill entire sphere
                        if distance <= radius:
                            self.blocks[x, y, z] = block
        
        return self
    
    def cylinder(self, cx, cz, y1, y2, radius, block, hollow=False):
        """
        Create a vertical cylinder.
        
        Args:
            cx, cz: Center X and Z coordinates
            y1, y2: Bottom and top Y coordinates
            radius: Radius of the cylinder
            block: Block to build with
            hollow: If True, only create the shell
            
        Returns:
            self (for method chaining)
        """
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
        """
        Create a pyramid structure.
        
        Args:
            x, y, z: Base corner coordinates
            base_size: Size of the pyramid base (square)
            height: Height of the pyramid
            block: Block to build with
            hollow: If True, only create the shell
            
        Returns:
            self (for method chaining)
        """
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
                    # Four edges of the square
                    self.set_block(x + offset + i, y + layer, z + offset, block)
                    self.set_block(x + offset + i, y + layer, z + offset + layer_size - 1, block)
                    self.set_block(x + offset, y + layer, z + offset + i, block)
                    self.set_block(x + offset + layer_size - 1, y + layer, z + offset + i, block)
            else:
                # Fill the layer
                self.fill(
                    x + offset, y + layer, z + offset,
                    x + offset + layer_size - 1, y + layer, z + offset + layer_size - 1,
                    block
                )
        
        return self
    
    def dome(self, cx, cy, cz, radius, block, hollow=False):
        """
        Create a dome (hemisphere).
        
        Args:
            cx, cy, cz: Center coordinates (base of dome)
            radius: Radius of the dome
            block: Block to build with
            hollow: If True, only create the shell
            
        Returns:
            self (for method chaining)
        """
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
    
    def arch(self, x1, y, z1, x2, z2, height, thickness, block):
        """
        Create an arch between two points.
        
        Args:
            x1, z1: Start coordinates
            x2, z2: End coordinates
            y: Base Y coordinate
            height: Height of the arch
            thickness: Thickness of the arch
            block: Block to build with
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        # Calculate arch parameters
        dx = x2 - x1
        dz = z2 - z1
        length = (dx**2 + dz**2)**0.5
        
        if length == 0:
            return self
        
        # Create arch using semicircle
        steps = int(length * 2)
        for i in range(steps + 1):
            t = i / steps
            x = x1 + dx * t
            z = z1 + dz * t
            
            # Semicircular height
            arch_y = y + height * (1 - (2 * t - 1)**2)**0.5
            
            # Place blocks with thickness
            for th in range(thickness):
                for ty in range(thickness):
                    bx = int(x)
                    by = int(arch_y) + ty
                    bz = int(z) + th
                    if self._in_bounds(bx, by, bz):
                        self.blocks[bx, by, bz] = block
        
        return self
    
    def spiral(self, cx, cz, y_start, y_end, radius, block, turns=2):
        """
        Create a spiral/helix structure.
        
        Args:
            cx, cz: Center X and Z coordinates
            y_start, y_end: Start and end Y coordinates
            radius: Radius of the spiral
            block: Block to build with
            turns: Number of complete rotations
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        import math
        
        height = abs(y_end - y_start)
        steps = int(height * 4)  # More steps for smoother spiral
        
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
        """
        Create a wall with optional battlements.
        
        Args:
            x1, y1, z1: Start coordinates
            x2, y2, z2: End coordinates
            block: Block to build with
            thickness: Wall thickness
            battlements: If True, add battlements on top
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        # Build main wall
        self.fill(x1, y1, z1, x2, y2, z2, block)
        
        # Add battlements if requested
        if battlements:
            # Determine wall direction
            if abs(x2 - x1) > abs(z2 - z1):
                # Wall runs along X axis
                for x in range(min(x1, x2), max(x1, x2) + 1, 2):
                    for z in range(min(z1, z2), max(z1, z2) + 1):
                        if self._in_bounds(x, y2 + 1, z):
                            self.blocks[x, y2 + 1, z] = block
                            if self._in_bounds(x, y2 + 2, z):
                                self.blocks[x, y2 + 2, z] = block
            else:
                # Wall runs along Z axis
                for z in range(min(z1, z2), max(z1, z2) + 1, 2):
                    for x in range(min(x1, x2), max(x1, x2) + 1):
                        if self._in_bounds(x, y2 + 1, z):
                            self.blocks[x, y2 + 1, z] = block
                            if self._in_bounds(x, y2 + 2, z):
                                self.blocks[x, y2 + 2, z] = block
        
        return self
    
    def staircase(self, x, y, z, direction, length, block, spiral_center=None):
        """
        Create a staircase (straight or spiral).
        
        Args:
            x, y, z: Starting coordinates
            direction: 'north', 'south', 'east', 'west' for straight stairs
            length: Number of steps
            block: Block to build with
            spiral_center: If provided (cx, cz), creates spiral staircase
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        if spiral_center:
            # Spiral staircase
            import math
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
            # Straight staircase
            dx, dz = 0, 0
            if direction == 'north':
                dz = -1
            elif direction == 'south':
                dz = 1
            elif direction == 'east':
                dx = 1
            elif direction == 'west':
                dx = -1
            
            for i in range(length):
                sx = x + dx * i
                sy = y + i
                sz = z + dz * i
                
                if self._in_bounds(sx, sy, sz):
                    self.blocks[sx, sy, sz] = block
        
        return self
    
    def terrace(self, x, y, z, width, length, levels, level_height, block):
        """
        Create terraced platforms.
        
        Args:
            x, y, z: Starting coordinates
            width, length: Dimensions of each terrace
            levels: Number of terrace levels
            level_height: Height of each level
            block: Block to build with
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        for level in range(levels):
            offset = level * 2  # Each level is smaller
            level_y = y + level * level_height
            
            self.fill(
                x + offset, level_y, z + offset,
                x + width - offset - 1, level_y, z + length - offset - 1,
                block
            )
        
        return self
    
    def pattern_fill(self, x1, y1, z1, x2, y2, z2, blocks, pattern='checkerboard'):
        """
        Fill a region with a pattern using multiple blocks.
        
        Args:
            x1, y1, z1: Starting corner
            x2, y2, z2: Ending corner
            blocks: List of blocks to use in pattern
            pattern: 'checkerboard', 'stripes_x', 'stripes_z', 'random'
            
        Returns:
            self (for method chaining)
        """
        import random
        
        for block in blocks:
            if not validate_block(block):
                raise ValueError(f"Invalid block: {block}")
        
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if not self._in_bounds(x, y, z):
                        continue
                    
                    if pattern == 'checkerboard':
                        idx = (x + y + z) % len(blocks)
                    elif pattern == 'stripes_x':
                        idx = x % len(blocks)
                    elif pattern == 'stripes_z':
                        idx = z % len(blocks)
                    elif pattern == 'random':
                        idx = random.randint(0, len(blocks) - 1)
                    else:
                        idx = 0
                    
                    self.blocks[x, y, z] = blocks[idx]
        
        return self
    
    def circle(self, cx, y, cz, radius, block, filled=True):
        """
        Create a horizontal circle or ring.
        
        Args:
            cx, cz: Center coordinates
            y: Y coordinate
            radius: Radius of the circle
            block: Block to build with
            filled: If True, fill the circle; if False, just the outline
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        for x in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
            for z in range(max(0, cz - radius), min(self.length, cz + radius + 1)):
                distance = ((x - cx)**2 + (z - cz)**2)**0.5
                
                if filled:
                    if distance <= radius:
                        self.blocks[x, y, z] = block
                else:
                    if abs(distance - radius) < 1:
                        self.blocks[x, y, z] = block
        
        return self
    
    def tree(self, x, y, z, trunk_height, trunk_block, leaves_block, canopy_radius=3):
        """
        Create a simple tree.
        
        Args:
            x, y, z: Base coordinates
            trunk_height: Height of the trunk
            trunk_block: Block for the trunk
            leaves_block: Block for the leaves
            canopy_radius: Radius of the leaf canopy
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(trunk_block) or not validate_block(leaves_block):
            raise ValueError("Invalid block")
        
        # Create trunk
        for h in range(trunk_height):
            if self._in_bounds(x, y + h, z):
                self.blocks[x, y + h, z] = trunk_block
        
        # Create canopy (sphere of leaves)
        canopy_y = y + trunk_height
        self.sphere(x, canopy_y, z, canopy_radius, leaves_block, hollow=False)
        
        return self
    
    def tower(self, x, y, z, radius, height, wall_block, floor_block=None, floors=1):
        """
        Create a tower with multiple floors.
        
        Args:
            x, y, z: Base center coordinates
            radius: Radius of the tower
            height: Total height
            wall_block: Block for walls
            floor_block: Block for floors (if None, no floors)
            floors: Number of floors to add
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(wall_block):
            raise ValueError(f"Invalid block: {wall_block}")
        
        # Create hollow cylinder for walls
        self.cylinder(x, z, y, y + height - 1, radius, wall_block, hollow=True)
        
        # Add floors
        if floor_block and validate_block(floor_block):
            floor_spacing = height // (floors + 1)
            for i in range(1, floors + 1):
                floor_y = y + i * floor_spacing
                self.circle(x, floor_y, z, radius - 1, floor_block, filled=True)
        
        return self
    
    def bridge(self, x1, y, z1, x2, z2, width, block, railing_block=None):
        """
        Create a bridge between two points.
        
        Args:
            x1, z1: Start coordinates
            x2, z2: End coordinates
            y: Y coordinate of the bridge
            width: Width of the bridge
            block: Block for the bridge deck
            railing_block: Block for railings (if None, no railings)
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        # Determine bridge direction
        dx = x2 - x1
        dz = z2 - z1
        length = max(abs(dx), abs(dz))
        
        if length == 0:
            return self
        
        # Build bridge deck
        for i in range(length + 1):
            t = i / length if length > 0 else 0
            x = int(x1 + dx * t)
            z = int(z1 + dz * t)
            
            # Place deck blocks
            for w in range(width):
                if abs(dx) > abs(dz):
                    # Bridge runs along X
                    bx, bz = x, z + w - width // 2
                else:
                    # Bridge runs along Z
                    bx, bz = x + w - width // 2, z
                
                if self._in_bounds(bx, y, bz):
                    self.blocks[bx, y, bz] = block
                
                # Add railings
                if railing_block and validate_block(railing_block):
                    if w == 0 or w == width - 1:
                        for h in range(1, 3):
                            if self._in_bounds(bx, y + h, bz):
                                self.blocks[bx, y + h, bz] = railing_block
        
        return self
    
    def roof(self, x1, y, z1, x2, z2, block, style='pitched'):
        """
        Create a roof structure.
        
        Args:
            x1, z1: Starting corner
            x2, z2: Ending corner
            y: Base Y coordinate
            block: Block to build with
            style: 'pitched', 'flat', or 'dome'
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        x1, x2 = min(x1, x2), max(x1, x2)
        z1, z2 = min(z1, z2), max(z1, z2)
        
        width = x2 - x1 + 1
        length = z2 - z1 + 1
        
        if style == 'flat':
            self.fill(x1, y, z1, x2, y, z2, block)
        
        elif style == 'pitched':
            # Pitched roof along Z axis
            peak_height = width // 2
            for i in range(peak_height):
                self.fill(
                    x1 + i, y + i, z1,
                    x2 - i, y + i, z2,
                    block
                )
        
        elif style == 'dome':
            cx = (x1 + x2) // 2
            cz = (z1 + z2) // 2
            radius = min(width, length) // 2
            self.dome(cx, y, cz, radius, block, hollow=False)
        
        return self
    
    def window(self, x, y, z, width, height, direction, frame_block=None, glass_block=None, style='simple'):
        """
        Create a window with optional frame and various styles.
        
        Args:
            x, y, z: Bottom-left corner coordinates
            width: Width of the window
            height: Height of the window
            direction: 'north', 'south', 'east', 'west'
            frame_block: Block for the frame (if None, no frame)
            glass_block: Block for the glass (if None, uses AIR for opening)
            style: 'simple', 'cross', 'grid', 'arch'
            
        Returns:
            self (for method chaining)
        """
        from blocks import GLASS, AIR
        
        if glass_block is None:
            glass_block = AIR
        
        if not validate_block(glass_block):
            raise ValueError(f"Invalid glass block: {glass_block}")
        
        if frame_block and not validate_block(frame_block):
            raise ValueError(f"Invalid frame block: {frame_block}")
        
        # Determine window orientation and coordinates
        if direction == 'north':
            # Window faces north (negative Z)
            for wx in range(width):
                for wy in range(height):
                    bx, by, bz = x + wx, y + wy, z
                    if self._in_bounds(bx, by, bz):
                        # Add frame
                        if frame_block and (wx == 0 or wx == width - 1 or wy == 0 or wy == height - 1):
                            self.blocks[bx, by, bz] = frame_block
                        else:
                            self.blocks[bx, by, bz] = glass_block
                            
                        # Add style details
                        if style == 'cross' and frame_block:
                            if wx == width // 2 or wy == height // 2:
                                self.blocks[bx, by, bz] = frame_block
                        elif style == 'grid' and frame_block:
                            if wx % 2 == 0 or wy % 2 == 0:
                                self.blocks[bx, by, bz] = frame_block
                        elif style == 'arch' and frame_block:
                            # Arched top
                            if wy >= height - 2:
                                dx = wx - width // 2
                                arch_radius = width // 2
                                if dx * dx + (wy - (height - arch_radius)) ** 2 > arch_radius ** 2:
                                    self.blocks[bx, by, bz] = frame_block
        
        elif direction == 'south':
            # Window faces south (positive Z)
            for wx in range(width):
                for wy in range(height):
                    bx, by, bz = x + wx, y + wy, z
                    if self._in_bounds(bx, by, bz):
                        if frame_block and (wx == 0 or wx == width - 1 or wy == 0 or wy == height - 1):
                            self.blocks[bx, by, bz] = frame_block
                        else:
                            self.blocks[bx, by, bz] = glass_block
                            
                        if style == 'cross' and frame_block:
                            if wx == width // 2 or wy == height // 2:
                                self.blocks[bx, by, bz] = frame_block
                        elif style == 'grid' and frame_block:
                            if wx % 2 == 0 or wy % 2 == 0:
                                self.blocks[bx, by, bz] = frame_block
        
        elif direction == 'east':
            # Window faces east (positive X)
            for wz in range(width):
                for wy in range(height):
                    bx, by, bz = x, y + wy, z + wz
                    if self._in_bounds(bx, by, bz):
                        if frame_block and (wz == 0 or wz == width - 1 or wy == 0 or wy == height - 1):
                            self.blocks[bx, by, bz] = frame_block
                        else:
                            self.blocks[bx, by, bz] = glass_block
                            
                        if style == 'cross' and frame_block:
                            if wz == width // 2 or wy == height // 2:
                                self.blocks[bx, by, bz] = frame_block
                        elif style == 'grid' and frame_block:
                            if wz % 2 == 0 or wy % 2 == 0:
                                self.blocks[bx, by, bz] = frame_block
        
        elif direction == 'west':
            # Window faces west (negative X)
            for wz in range(width):
                for wy in range(height):
                    bx, by, bz = x, y + wy, z + wz
                    if self._in_bounds(bx, by, bz):
                        if frame_block and (wz == 0 or wz == width - 1 or wy == 0 or wy == height - 1):
                            self.blocks[bx, by, bz] = frame_block
                        else:
                            self.blocks[bx, by, bz] = glass_block
                            
                        if style == 'cross' and frame_block:
                            if wz == width // 2 or wy == height // 2:
                                self.blocks[bx, by, bz] = frame_block
                        elif style == 'grid' and frame_block:
                            if wz % 2 == 0 or wy % 2 == 0:
                                self.blocks[bx, by, bz] = frame_block
        
        return self
    
    def window_grid(self, x1, y1, z1, x2, y2, z2, window_width, window_height, spacing, frame_block, glass_block=None):
        """
        Automatically place a grid of windows in a wall.
        
        Args:
            x1, y1, z1: Wall start coordinates
            x2, y2, z2: Wall end coordinates
            window_width: Width of each window
            window_height: Height of each window
            spacing: Space between windows
            frame_block: Block for window frames
            glass_block: Block for glass (if None, uses GLASS)
            
        Returns:
            self (for method chaining)
        """
        from blocks import GLASS
        
        if glass_block is None:
            glass_block = GLASS
        
        # Determine wall orientation
        if x1 == x2:
            # Wall runs along Z axis (east/west facing)
            direction = 'east' if x1 < self.width // 2 else 'west'
            wall_length = abs(z2 - z1)
            
            # Calculate window positions
            num_windows = (wall_length + spacing) // (window_width + spacing)
            start_z = min(z1, z2) + (wall_length - (num_windows * window_width + (num_windows - 1) * spacing)) // 2
            
            for i in range(num_windows):
                for row_y in range(y1, y2, window_height + spacing):
                    if row_y + window_height <= y2:
                        wz = start_z + i * (window_width + spacing)
                        self.window(x1, row_y, wz, window_width, window_height, direction, frame_block, glass_block)
        
        elif z1 == z2:
            # Wall runs along X axis (north/south facing)
            direction = 'north' if z1 < self.length // 2 else 'south'
            wall_length = abs(x2 - x1)
            
            # Calculate window positions
            num_windows = (wall_length + spacing) // (window_width + spacing)
            start_x = min(x1, x2) + (wall_length - (num_windows * window_width + (num_windows - 1) * spacing)) // 2
            
            for i in range(num_windows):
                for row_y in range(y1, y2, window_height + spacing):
                    if row_y + window_height <= y2:
                        wx = start_x + i * (window_width + spacing)
                        self.window(wx, row_y, z1, window_width, window_height, direction, frame_block, glass_block)
        
        return self
    
    def door(self, x, y, z, direction, door_block=None, width=1, height=2, frame_block=None):
        """
        Create a door opening with optional frame.
        
        Args:
            x, y, z: Bottom-left corner coordinates
            direction: 'north', 'south', 'east', 'west'
            door_block: Block for the door (if None, uses AIR for opening)
            width: Width of the door
            height: Height of the door
            frame_block: Block for the frame (if None, no frame)
            
        Returns:
            self (for method chaining)
        """
        if door_block is None:
            door_block = AIR
        
        if not validate_block(door_block):
            raise ValueError(f"Invalid door block: {door_block}")
        
        if frame_block and not validate_block(frame_block):
            raise ValueError(f"Invalid frame block: {frame_block}")
        
        # Create door opening
        if direction in ['north', 'south']:
            for dx in range(width):
                for dy in range(height):
                    if self._in_bounds(x + dx, y + dy, z):
                        self.blocks[x + dx, y + dy, z] = door_block
            
            # Add frame
            if frame_block:
                for dx in range(-1, width + 1):
                    for dy in range(-1, height + 1):
                        if (dx == -1 or dx == width or dy == -1 or dy == height):
                            if self._in_bounds(x + dx, y + dy, z):
                                self.blocks[x + dx, y + dy, z] = frame_block
        
        elif direction in ['east', 'west']:
            for dz in range(width):
                for dy in range(height):
                    if self._in_bounds(x, y + dy, z + dz):
                        self.blocks[x, y + dy, z + dz] = door_block
            
            # Add frame
            if frame_block:
                for dz in range(-1, width + 1):
                    for dy in range(-1, height + 1):
                        if (dz == -1 or dz == width or dy == -1 or dy == height):
                            if self._in_bounds(x, y + dy, z + dz):
                                self.blocks[x, y + dy, z + dz] = frame_block
        
        return self
    
    def column(self, x, y1, z, y2, block, capital_block=None, base_block=None, width=1):
        """
        Create a column with optional capital and base.
        
        Args:
            x, z: Column center coordinates
            y1, y2: Bottom and top Y coordinates
            block: Block for the column shaft
            capital_block: Block for the capital (top decoration)
            base_block: Block for the base (bottom decoration)
            width: Width of the column (1 for single block, 2+ for wider)
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        y1, y2 = min(y1, y2), max(y1, y2)
        
        # Create column shaft
        offset = width // 2
        for dx in range(-offset, width - offset):
            for dz in range(-offset, width - offset):
                for y in range(y1, y2 + 1):
                    if self._in_bounds(x + dx, y, z + dz):
                        self.blocks[x + dx, y, z + dz] = block
        
        # Add capital (top)
        if capital_block and validate_block(capital_block):
            cap_width = width + 1
            cap_offset = cap_width // 2
            for dx in range(-cap_offset, cap_width - cap_offset):
                for dz in range(-cap_offset, cap_width - cap_offset):
                    if self._in_bounds(x + dx, y2 + 1, z + dz):
                        self.blocks[x + dx, y2 + 1, z + dz] = capital_block
        
        # Add base (bottom)
        if base_block and validate_block(base_block):
            base_width = width + 1
            base_offset = base_width // 2
            for dx in range(-base_offset, base_width - base_offset):
                for dz in range(-base_offset, base_width - base_offset):
                    if self._in_bounds(x + dx, y1 - 1, z + dz):
                        self.blocks[x + dx, y1 - 1, z + dz] = base_block
        
        return self
    
    def floor_pattern(self, x1, y, z1, x2, z2, blocks, pattern='tile', border_block=None):
        """
        Create a floor with advanced patterns.
        
        Args:
            x1, z1: Starting corner
            x2, z2: Ending corner
            y: Y coordinate of the floor
            blocks: List of blocks to use in pattern
            pattern: 'tile', 'checkerboard', 'diagonal', 'circular', 'random'
            border_block: Optional border block
            
        Returns:
            self (for method chaining)
        """
        import random
        import math
        
        for block in blocks:
            if not validate_block(block):
                raise ValueError(f"Invalid block: {block}")
        
        x1, x2 = min(x1, x2), max(x1, x2)
        z1, z2 = min(z1, z2), max(z1, z2)
        
        cx = (x1 + x2) / 2
        cz = (z1 + z2) / 2
        
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if not self._in_bounds(x, y, z):
                    continue
                
                # Border
                if border_block and (x == x1 or x == x2 or z == z1 or z == z2):
                    self.blocks[x, y, z] = border_block
                    continue
                
                # Pattern selection
                if pattern == 'tile':
                    idx = ((x // 2) + (z // 2)) % len(blocks)
                elif pattern == 'checkerboard':
                    idx = (x + z) % len(blocks)
                elif pattern == 'diagonal':
                    idx = (x + z) % len(blocks)
                elif pattern == 'circular':
                    dist = math.sqrt((x - cx)**2 + (z - cz)**2)
                    idx = int(dist) % len(blocks)
                elif pattern == 'random':
                    idx = random.randint(0, len(blocks) - 1)
                else:
                    idx = 0
                
                self.blocks[x, y, z] = blocks[idx]
        
        return self
    
    def fill_if(self, x1, y1, z1, x2, y2, z2, block, condition_func):
        """
        Fill blocks that meet a custom condition.
        
        Args:
            x1, y1, z1: Starting corner
            x2, y2, z2: Ending corner
            block: Block to place
            condition_func: Function that takes (x, y, z) and returns True/False
            
        Returns:
            self (for method chaining)
            
        Example:
            # Fill only blocks where x+y+z is even
            s.fill_if(0, 0, 0, 10, 10, 10, STONE, lambda x,y,z: (x+y+z) % 2 == 0)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if self._in_bounds(x, y, z) and condition_func(x, y, z):
                        self.blocks[x, y, z] = block
        
        return self
    
    def replace(self, x1, y1, z1, x2, y2, z2, old_block, new_block):
        """
        Replace specific blocks in a region.
        
        Args:
            x1, y1, z1: Starting corner
            x2, y2, z2: Ending corner
            old_block: Block to replace
            new_block: Block to replace with
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(old_block) or not validate_block(new_block):
            raise ValueError("Invalid block")
        
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if self._in_bounds(x, y, z) and self.blocks[x, y, z] == old_block:
                        self.blocks[x, y, z] = new_block
        
        return self
    
    def copy_region(self, x1, y1, z1, x2, y2, z2, dest_x, dest_y, dest_z, mirror_x=False, mirror_z=False):
        """
        Copy a region to another location with optional mirroring.
        
        Args:
            x1, y1, z1: Source start coordinates
            x2, y2, z2: Source end coordinates
            dest_x, dest_y, dest_z: Destination start coordinates
            mirror_x: Mirror along X axis
            mirror_z: Mirror along Z axis
            
        Returns:
            self (for method chaining)
        """
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
                    
                    if not self._in_bounds(src_x, src_y, src_z):
                        continue
                    
                    # Calculate destination with mirroring
                    dx = (width - 1 - x) if mirror_x else x
                    dz = (length - 1 - z) if mirror_z else z
                    
                    dest_bx = dest_x + dx
                    dest_by = dest_y + y
                    dest_bz = dest_z + dz
                    
                    if self._in_bounds(dest_bx, dest_by, dest_bz):
                        self.blocks[dest_bx, dest_by, dest_bz] = self.blocks[src_x, src_y, src_z]
        
        return self
    
    def room(self, x1, y1, z1, x2, y2, z2, wall_block, floor_block, ceiling_block, 
             windows=True, door_pos=None, window_style='simple'):
        """
        Create a complete room with walls, floor, ceiling, windows, and door.
        
        Args:
            x1, y1, z1: Starting corner
            x2, y2, z2: Ending corner
            wall_block: Block for walls
            floor_block: Block for floor
            ceiling_block: Block for ceiling
            windows: If True, add windows automatically
            door_pos: Tuple (x, y, z) for door position (if None, no door)
            window_style: Style for windows ('simple', 'cross', 'grid')
            
        Returns:
            self (for method chaining)
        """
        from blocks import GLASS
        
        if not validate_block(wall_block) or not validate_block(floor_block) or not validate_block(ceiling_block):
            raise ValueError("Invalid block")
        
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        
        # Floor
        self.fill(x1, y1, z1, x2, y1, z2, floor_block)
        
        # Ceiling
        self.fill(x1, y2, z1, x2, y2, z2, ceiling_block)
        
        # Walls
        self.hollow_box(x1, y1, z1, x2, y2, z2, wall_block)
        
        # Windows
        if windows:
            room_height = y2 - y1
            window_y = y1 + room_height // 3
            window_height = max(2, room_height // 3)
            
            # North wall
            if x2 - x1 > 6:
                self.window(x1 + 2, window_y, z1, 3, window_height, 'north', wall_block, GLASS, window_style)
            
            # South wall
            if x2 - x1 > 6:
                self.window(x2 - 4, window_y, z2, 3, window_height, 'south', wall_block, GLASS, window_style)
        
        # Door
        if door_pos:
            dx, dy, dz = door_pos
            self.door(dx, dy, dz, 'north', None, 1, 2, wall_block)
        
        return self
    
    def ellipsoid(self, cx, cy, cz, radius_x, radius_y, radius_z, block, hollow=False):
        """
        Create an ellipsoid with different radii for each axis.
        
        Args:
            cx, cy, cz: Center coordinates
            radius_x, radius_y, radius_z: Radii for X, Y, Z axes
            block: Block to build with
            hollow: If True, only create the shell
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        for x in range(max(0, cx - radius_x), min(self.width, cx + radius_x + 1)):
            for y in range(max(0, cy - radius_y), min(self.height, cy + radius_y + 1)):
                for z in range(max(0, cz - radius_z), min(self.length, cz + radius_z + 1)):
                    # Ellipsoid equation: (x/rx)^2 + (y/ry)^2 + (z/rz)^2 <= 1
                    dx = (x - cx) / radius_x if radius_x > 0 else 0
                    dy = (y - cy) / radius_y if radius_y > 0 else 0
                    dz = (z - cz) / radius_z if radius_z > 0 else 0
                    distance = (dx**2 + dy**2 + dz**2)**0.5
                    
                    if hollow:
                        if abs(distance - 1) < 0.15:
                            self.blocks[x, y, z] = block
                    else:
                        if distance <= 1:
                            self.blocks[x, y, z] = block
        
        return self
    
    def cone(self, x, y, z, base_radius, height, block, hollow=False):
        """
        Create a cone structure.
        
        Args:
            x, y, z: Base center coordinates
            base_radius: Radius of the cone base
            height: Height of the cone
            block: Block to build with
            hollow: If True, only create the shell
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        for layer in range(height):
            # Calculate radius for this layer (linear taper)
            layer_radius = base_radius * (1 - layer / height)
            if layer_radius < 0.5:
                # Place single block at tip
                if self._in_bounds(x, y + layer, z):
                    self.blocks[x, y + layer, z] = block
                continue
            
            # Draw circle at this height
            for dx in range(-int(layer_radius) - 1, int(layer_radius) + 2):
                for dz in range(-int(layer_radius) - 1, int(layer_radius) + 2):
                    dist = (dx**2 + dz**2)**0.5
                    
                    if hollow:
                        if abs(dist - layer_radius) < 1:
                            if self._in_bounds(x + dx, y + layer, z + dz):
                                self.blocks[x + dx, y + layer, z + dz] = block
                    else:
                        if dist <= layer_radius:
                            if self._in_bounds(x + dx, y + layer, z + dz):
                                self.blocks[x + dx, y + layer, z + dz] = block
        
        return self
    
    def torus(self, cx, cy, cz, major_radius, minor_radius, block, axis='y'):
        """
        Create a torus (donut shape).
        
        Args:
            cx, cy, cz: Center coordinates
            major_radius: Distance from center to tube center
            minor_radius: Radius of the tube
            block: Block to build with
            axis: 'x', 'y', or 'z' - axis the torus is oriented around
            
        Returns:
            self (for method chaining)
        """
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        import math
        
        # Scan the bounding box
        max_r = major_radius + minor_radius
        
        for x in range(max(0, cx - max_r), min(self.width, cx + max_r + 1)):
            for y in range(max(0, cy - max_r), min(self.height, cy + max_r + 1)):
                for z in range(max(0, cz - max_r), min(self.length, cz + max_r + 1)):
                    dx = x - cx
                    dy = y - cy
                    dz = z - cz
                    
                    # Torus equation depends on axis
                    if axis == 'y':
                        # Torus around Y axis
                        dist_from_center = math.sqrt(dx**2 + dz**2)
                        dist_from_tube = math.sqrt((dist_from_center - major_radius)**2 + dy**2)
                    elif axis == 'x':
                        # Torus around X axis
                        dist_from_center = math.sqrt(dy**2 + dz**2)
                        dist_from_tube = math.sqrt((dist_from_center - major_radius)**2 + dx**2)
                    else:  # axis == 'z'
                        # Torus around Z axis
                        dist_from_center = math.sqrt(dx**2 + dy**2)
                        dist_from_tube = math.sqrt((dist_from_center - major_radius)**2 + dz**2)
                    
                    if dist_from_tube <= minor_radius:
                        self.blocks[x, y, z] = block
        
        return self
    
    def furniture(self, x, y, z, furniture_type, block, direction='north'):
        """
        Create procedural furniture.
        
        Args:
            x, y, z: Base coordinates
            furniture_type: 'table', 'chair', 'bed', 'shelf', 'desk'
            block: Primary block to use
            direction: 'north', 'south', 'east', 'west' (for orientation)
            
        Returns:
            self (for method chaining)
        """
        from blocks import OAK_PLANKS, WOOL_WHITE
        
        if not validate_block(block):
            raise ValueError(f"Invalid block: {block}")
        
        if furniture_type == 'table':
            # Table legs (4 corners)
            for dx, dz in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                if self._in_bounds(x + dx, y, z + dz):
                    self.blocks[x + dx, y, z + dz] = block
            # Table top
            self.fill(x, y + 1, z, x + 2, y + 1, z + 2, block)
        
        elif furniture_type == 'chair':
            # Seat
            self.fill(x, y, z, x + 1, y, z + 1, block)
            # Back legs
            if direction == 'north':
                self.fill(x, y + 1, z, x + 1, y + 2, z, block)
            elif direction == 'south':
                self.fill(x, y + 1, z + 1, x + 1, y + 2, z + 1, block)
            elif direction == 'east':
                self.fill(x + 1, y + 1, z, x + 1, y + 2, z + 1, block)
            else:  # west
                self.fill(x, y + 1, z, x, y + 2, z + 1, block)
        
        elif furniture_type == 'bed':
            # Bed frame
            self.fill(x, y, z, x + 1, y, z + 3, block)
            # Mattress
            self.fill(x, y + 1, z, x + 1, y + 1, z + 3, WOOL_WHITE)
            # Headboard
            if direction == 'north':
                self.fill(x, y + 1, z, x + 1, y + 2, z, block)
            else:
                self.fill(x, y + 1, z + 3, x + 1, y + 2, z + 3, block)
        
        elif furniture_type == 'shelf':
            # Vertical supports
            self.fill(x, y, z, x, y + 4, z, block)
            self.fill(x + 3, y, z, x + 3, y + 4, z, block)
            # Shelves
            for shelf_y in [y + 1, y + 2, y + 3, y + 4]:
                self.fill(x, shelf_y, z, x + 3, shelf_y, z, block)
        
        elif furniture_type == 'desk':
            # Legs
            for dx in [0, 3]:
                for dz in [0, 2]:
                    if self._in_bounds(x + dx, y, z + dz):
                        self.blocks[x + dx, y, z + dz] = block
            # Desktop
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
        
        Returns:
            Dictionary with schematic data
        """
        blocks_list = []
        
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.length):
                    block = self.blocks[x, y, z]
                    if block != AIR:  # Only include non-air blocks
                        blocks_list.append({
                            'x': x,
                            'y': y,
                            'z': z,
                            'type': block.minecraft_id,
                            'name': block.name,
                            'color': block.color
                        })
        
        return {
            'width': self.width,
            'height': self.height,
            'length': self.length,
            'blocks': blocks_list,
            'block_count': len(blocks_list)
        }
    
    def _in_bounds(self, x, y, z):
        """Check if coordinates are within schematic bounds."""
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                0 <= z < self.length)
    
    def __repr__(self):
        block_count = np.sum(self.blocks != AIR)
        return f"Schematic({self.width}x{self.height}x{self.length}, {block_count} blocks)"
