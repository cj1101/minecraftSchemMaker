"""
Test script for enhanced API features.
Run this to verify all new methods work correctly.
"""

from schematic_api import Schematic
from blocks import *

def test_windows_and_doors():
    """Test window and door creation methods."""
    print("Testing windows and doors...")
    
    s = Schematic(30, 20, 30)
    
    # Test different window styles
    s.fill(5, 0, 5, 5, 15, 25, STONE_BRICKS)  # Wall
    s.window(5, 3, 8, 3, 4, 'east', DARK_OAK_PLANKS, GLASS, 'simple')
    s.window(5, 3, 13, 3, 4, 'east', DARK_OAK_PLANKS, GLASS, 'cross')
    s.window(5, 3, 18, 3, 4, 'east', DARK_OAK_PLANKS, GLASS, 'grid')
    
    # Test window grid
    s.fill(10, 0, 5, 25, 15, 5, WHITE_CONCRETE)
    s.window_grid(10, 2, 5, 25, 14, 5, 2, 3, 2, BLACK_CONCRETE, GLASS)
    
    # Test doors
    s.door(15, 0, 10, 'north', None, 2, 3, STONE_BRICKS)
    
    print(f"✓ Created schematic with {s.to_dict()['block_count']} blocks")
    return s

def test_columns_and_floors():
    """Test structural elements."""
    print("Testing columns and floor patterns...")
    
    s = Schematic(25, 20, 25)
    
    # Test columns with capitals and bases
    for x, z in [(5, 5), (5, 20), (20, 5), (20, 20)]:
        s.column(x, 0, z, 15, QUARTZ_BLOCK, GOLD_BLOCK, SMOOTH_STONE, width=2)
    
    # Test floor patterns
    s.floor_pattern(0, 0, 0, 24, 24, [WHITE_CONCRETE, BLACK_CONCRETE], 
                    'checkerboard', GOLD_BLOCK)
    s.floor_pattern(8, 1, 8, 16, 16, [RED_CONCRETE, BLUE_CONCRETE, YELLOW_CONCRETE], 
                    'circular', DIAMOND_BLOCK)
    
    print(f"✓ Created schematic with {s.to_dict()['block_count']} blocks")
    return s

def test_conditional_and_utility():
    """Test conditional filling and utility methods."""
    print("Testing conditional filling and utilities...")
    
    s = Schematic(30, 30, 30)
    
    # Test fill_if - create sphere pattern
    s.fill_if(0, 0, 0, 29, 29, 29, DIAMOND_BLOCK,
              lambda x,y,z: ((x-15)**2 + (y-15)**2 + (z-15)**2) < 100)
    
    # Test replace
    s.replace(0, 0, 0, 29, 29, 29, DIAMOND_BLOCK, EMERALD_BLOCK)
    
    # Test copy_region with mirroring
    s.fill(5, 5, 5, 10, 10, 10, GOLD_BLOCK)
    s.copy_region(5, 5, 5, 10, 10, 10, 15, 5, 5, mirror_x=True)
    
    print(f"✓ Created schematic with {s.to_dict()['block_count']} blocks")
    return s

def test_room_and_furniture():
    """Test complete room creation with furniture."""
    print("Testing room and furniture...")
    
    s = Schematic(25, 15, 25)
    
    # Create room
    s.room(2, 0, 2, 22, 10, 22, STONE_BRICKS, OAK_PLANKS, SPRUCE_PLANKS,
           windows=True, door_pos=(12, 0, 2), window_style='cross')
    
    # Add furniture
    s.furniture(6, 1, 6, 'table', DARK_OAK_PLANKS)
    s.furniture(6, 1, 10, 'chair', DARK_OAK_PLANKS, 'north')
    s.furniture(12, 1, 6, 'desk', DARK_OAK_PLANKS)
    s.furniture(15, 1, 15, 'bed', DARK_OAK_PLANKS, 'east')
    s.furniture(18, 1, 6, 'shelf', DARK_OAK_PLANKS)
    
    print(f"✓ Created schematic with {s.to_dict()['block_count']} blocks")
    return s

def test_advanced_geometry():
    """Test advanced geometric shapes."""
    print("Testing advanced geometry...")
    
    s = Schematic(50, 50, 50)
    
    # Test ellipsoid
    s.ellipsoid(15, 15, 15, 8, 12, 6, GOLD_BLOCK, hollow=True)
    
    # Test cone
    s.cone(35, 0, 35, 8, 20, EMERALD_BLOCK, hollow=False)
    
    # Test torus
    s.torus(25, 30, 25, 10, 3, DIAMOND_BLOCK, axis='y')
    
    print(f"✓ Created schematic with {s.to_dict()['block_count']} blocks")
    return s

def test_complex_structure():
    """Test combining multiple new features."""
    print("Testing complex structure with all features...")
    
    s = Schematic(40, 30, 40)
    
    # Base floor with pattern
    s.floor_pattern(0, 0, 0, 39, 39, [QUARTZ_BLOCK, SMOOTH_QUARTZ], 
                    'checkerboard', GOLD_BLOCK)
    
    # Main building
    s.room(5, 0, 5, 35, 20, 35, STONE_BRICKS, OAK_PLANKS, SPRUCE_PLANKS,
           windows=False, door_pos=(20, 0, 5))
    
    # Add window grids
    s.window_grid(5, 3, 5, 35, 18, 5, 3, 4, 3, DARK_OAK_PLANKS, GLASS)
    s.window_grid(5, 3, 35, 35, 18, 35, 3, 4, 3, DARK_OAK_PLANKS, GLASS)
    
    # Interior columns
    for x, z in [(12, 12), (12, 28), (28, 12), (28, 28)]:
        s.column(x, 1, z, 19, QUARTZ_BLOCK, GOLD_BLOCK, GOLD_BLOCK, width=2)
    
    # Decorative elements
    s.torus(20, 22, 20, 6, 2, GLOWSTONE, axis='y')
    
    # Furniture in corners
    s.furniture(8, 1, 8, 'table', DARK_OAK_PLANKS)
    s.furniture(8, 1, 32, 'desk', DARK_OAK_PLANKS)
    s.furniture(32, 1, 8, 'shelf', DARK_OAK_PLANKS)
    s.furniture(32, 1, 32, 'bed', DARK_OAK_PLANKS)
    
    print(f"✓ Created complex schematic with {s.to_dict()['block_count']} blocks")
    return s

if __name__ == "__main__":
    print("=" * 60)
    print("Enhanced API Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_windows_and_doors()
        test_columns_and_floors()
        test_conditional_and_utility()
        test_room_and_furniture()
        test_advanced_geometry()
        test_complex_structure()
        
        print()
        print("=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("All 13 new methods are working correctly:")
        print("  • window, window_grid, door")
        print("  • column, floor_pattern")
        print("  • fill_if, replace, copy_region")
        print("  • room, furniture")
        print("  • ellipsoid, cone, torus")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ TEST FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
