"""
Flask server providing REST API for schematic generation and 3D preview.
Serves the web viewer and handles code execution.
"""

from flask import Flask, request, jsonify, send_from_directory, send_file, make_response
from flask_cors import CORS
import traceback
import os
import sys
from io import StringIO
import tempfile

# Import schematic modules
from schematic_api import Schematic
from blocks import get_all_blocks, BLOCK_REGISTRY
from nbt_exporter import NBTExporter
import blocks  # For exec context

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for local development

# Store the current schematic in memory
current_schematic = None


@app.route('/')
def index():
    """Serve the main viewer page."""
    return send_from_directory('static', 'viewer.html')


@app.route('/api/blocks', methods=['GET'])
def get_blocks():
    """Return all available block types."""
    all_blocks = get_all_blocks()
    blocks_data = [
        {
            'id': block.minecraft_id,
            'name': block.name,
            'color': block.color
        }
        for block in all_blocks
    ]
    return jsonify({'blocks': blocks_data})


@app.route('/api/execute', methods=['POST'])
def execute_code():
    """
    Execute Python code and return the resulting schematic data.
    
    Expected JSON:
        {
            "code": "from schematic_api import *\\nfrom blocks import *\\ns = Schematic(10,10,10)\\n..."
        }
    
    Returns:
        {
            "success": true,
            "schematic": {...},
            "message": "Executed successfully"
        }
    """
    global current_schematic
    
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'No code provided'
            }), 400
        
        # Create execution context with all necessary imports
        exec_globals = {
            'Schematic': Schematic,
            'blocks': blocks,
            '__builtins__': __builtins__,
        }
        
        # Add all block constants to the context automatically
        for block_name, block_obj in BLOCK_REGISTRY.items():
            # Create a clean constant name from the block name
            const_name = block_obj.name.upper().replace(' ', '_')
            exec_globals[const_name] = block_obj
        
        
        exec_locals = {}
        
        # Execute the code
        exec(code, exec_globals, exec_locals)
        
        # Look for a Schematic object in the locals
        schematic = None
        for var_name, var_value in exec_locals.items():
            if isinstance(var_value, Schematic):
                schematic = var_value
                break
        
        if schematic is None:
            return jsonify({
                'success': False,
                'error': 'No Schematic object created. Make sure to create a Schematic instance (e.g., s = Schematic(10, 10, 10))'
            }), 400
        
        # Store for export
        current_schematic = schematic
        
        # Convert to dict for JSON response
        schematic_data = schematic.to_dict()
        
        return jsonify({
            'success': True,
            'schematic': schematic_data,
            'message': f'Executed successfully. Created {schematic_data["block_count"]} blocks.'
        })
        
    except Exception as e:
        error_trace = traceback.format_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': error_trace
        }), 500


@app.route('/api/export', methods=['POST'])
def export_schematic():
    """
    Export the current schematic to a .schem file.
    
    Expected JSON:
        {
            "filename": "my_structure"  // .schem will be added automatically
        }
    
    Returns:
        The .schem file as a download
    """
    global current_schematic
    
    print("[EXPORT] Export endpoint called")
    
    if current_schematic is None:
        print("[EXPORT] Error: No schematic available")
        return jsonify({
            'success': False,
            'error': 'No schematic to export. Execute code first.'
        }), 400
    
    try:
        data = request.get_json()
        filename = data.get('filename', 'schematic')
        print(f"[EXPORT] Requested filename: {filename}")
        
        # Ensure .schem extension
        if not filename.endswith('.schem'):
            filename += '.schem'
        print(f"[EXPORT] Final filename: {filename}")
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)
        print(f"[EXPORT] Temp file path: {filepath}")
        
        # Export to file
        print(f"[EXPORT] Exporting schematic: {current_schematic.width}x{current_schematic.height}x{current_schematic.length}")
        NBTExporter.export_schematic(current_schematic, filepath)
        print(f"[EXPORT] Export complete, file size: {os.path.getsize(filepath)} bytes")
        
        # Read the file content
        with open(filepath, 'rb') as f:
            file_content = f.read()
        
        # Create response with explicit headers
        print(f"[EXPORT] Sending file to client ({len(file_content)} bytes)...")
        response = make_response(file_content)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Length'] = len(file_content)
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"[EXPORT] ERROR: {str(e)}")
        print(f"[EXPORT] Traceback:\n{error_trace}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': error_trace
        }), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Return example scripts showcasing the enhanced API."""
    examples = [
        {
            'name': 'Simple Box',
            'description': 'A basic stone box with glass window',
            'code': '''from schematic_api import Schematic
from blocks import STONE, GLASS

s = Schematic(10, 10, 10)
s.hollow_box(0, 0, 0, 9, 9, 9, STONE)
s.fill(2, 2, 2, 7, 7, 7, GLASS)'''
        },
        {
            'name': 'Pyramid',
            'description': 'A sandstone pyramid',
            'code': '''from schematic_api import Schematic
from blocks import SANDSTONE, GOLD_BLOCK

s = Schematic(30, 20, 30)
s.pyramid(0, 0, 0, 30, 15, SANDSTONE)
# Add gold cap
s.fill(13, 15, 13, 16, 16, 16, GOLD_BLOCK)'''
        },
        {
            'name': 'Dome Temple',
            'description': 'A quartz dome with pillars',
            'code': '''from schematic_api import Schematic
from blocks import QUARTZ_BLOCK, SMOOTH_QUARTZ, GOLD_BLOCK

s = Schematic(40, 25, 40)
# Base platform
s.fill(0, 0, 0, 39, 0, 39, SMOOTH_QUARTZ)
# Dome
s.dome(20, 1, 20, 18, QUARTZ_BLOCK, hollow=True)
# Pillars at corners
for x, z in [(5, 5), (5, 35), (35, 5), (35, 35)]:
    s.fill(x, 1, z, x, 15, z, GOLD_BLOCK)'''
        },
        {
            'name': 'Castle',
            'description': 'A medieval castle with towers and walls',
            'code': '''from schematic_api import Schematic
from blocks import STONE_BRICKS, COBBLESTONE, OAK_PLANKS

s = Schematic(50, 30, 50)
# Walls with battlements
s.wall(5, 0, 5, 45, 10, 5, STONE_BRICKS, battlements=True)
s.wall(5, 0, 45, 45, 10, 45, STONE_BRICKS, battlements=True)
s.wall(5, 0, 5, 5, 10, 45, STONE_BRICKS, battlements=True)
s.wall(45, 0, 5, 45, 10, 45, STONE_BRICKS, battlements=True)

# Corner towers
for x, z in [(5, 5), (5, 45), (45, 5), (45, 45)]:
    s.tower(x, 0, z, 4, 20, COBBLESTONE, OAK_PLANKS, floors=3)'''
        },
        {
            'name': 'Modern Building',
            'description': 'A modern building with terraces',
            'code': '''from schematic_api import Schematic
from blocks import WHITE_CONCRETE, GLASS, LIGHT_GRAY_CONCRETE

s = Schematic(30, 40, 30)
# Main structure
s.hollow_box(0, 0, 0, 29, 35, 29, WHITE_CONCRETE)
# Glass windows
for y in range(2, 35, 4):
    s.fill(1, y, 1, 28, y+1, 28, GLASS)
# Terraces
s.terrace(5, 36, 5, 20, 20, 3, 1, LIGHT_GRAY_CONCRETE)'''
        },
        {
            'name': 'Bridge',
            'description': 'A stone bridge with railings',
            'code': '''from schematic_api import Schematic
from blocks import STONE_BRICKS, OAK_PLANKS, IRON_BLOCK

s = Schematic(50, 15, 20)
# Bridge deck
s.bridge(5, 5, 10, 45, 10, 5, STONE_BRICKS, OAK_PLANKS)
# Support pillars
for x in range(10, 45, 8):
    s.fill(x, 0, 10, x, 4, 10, IRON_BLOCK)'''
        },
        {
            'name': 'Spiral Tower',
            'description': 'A tower with spiral staircase',
            'code': '''from schematic_api import Schematic
from blocks import BRICKS, GLOWSTONE, STONE_BRICKS

s = Schematic(25, 50, 25)
# Hollow tower
s.cylinder(12, 12, 0, 45, 10, BRICKS, hollow=True)
# Spiral staircase
s.spiral(12, 12, 0, 45, 8, STONE_BRICKS, turns=6)
# Glowing top
s.circle(12, 46, 12, 10, GLOWSTONE, filled=True)'''
        },
        {
            'name': 'Colorful Pattern',
            'description': 'A floor with checkerboard pattern',
            'code': '''from schematic_api import Schematic
from blocks import *

s = Schematic(30, 5, 30)
# Checkerboard floor
blocks = [WHITE_CONCRETE, BLACK_CONCRETE]
s.pattern_fill(0, 0, 0, 29, 0, 29, blocks, 'checkerboard')
# Striped walls
wall_blocks = [RED_CONCRETE, BLUE_CONCRETE, YELLOW_CONCRETE]
s.pattern_fill(0, 1, 0, 29, 4, 0, wall_blocks, 'stripes_x')'''
        },
        {
            'name': 'Detailed House',
            'description': 'A house with windows, door, and interior',
            'code': '''from schematic_api import Schematic
from blocks import STONE_BRICKS, OAK_PLANKS, SPRUCE_PLANKS, DARK_OAK_PLANKS, GLASS

s = Schematic(25, 15, 25)
# Create main room
s.room(2, 0, 2, 22, 8, 22, STONE_BRICKS, OAK_PLANKS, SPRUCE_PLANKS, 
       windows=True, door_pos=(12, 0, 2), window_style='cross')

# Add decorative floor pattern
s.floor_pattern(4, 1, 4, 20, 20, [OAK_PLANKS, SPRUCE_PLANKS], 'checkerboard', DARK_OAK_PLANKS)

# Add furniture
s.furniture(6, 1, 6, 'table', DARK_OAK_PLANKS)
s.furniture(6, 1, 10, 'chair', DARK_OAK_PLANKS, 'north')
s.furniture(15, 1, 15, 'bed', DARK_OAK_PLANKS, 'east')
s.furniture(18, 1, 6, 'shelf', DARK_OAK_PLANKS)'''
        },
        {
            'name': 'Cathedral',
            'description': 'A cathedral with columns and arched windows',
            'code': '''from schematic_api import Schematic
from blocks import STONE_BRICKS, QUARTZ_BLOCK, GOLD_BLOCK, BLUE_STAINED_GLASS

s = Schematic(40, 35, 60)
# Floor
s.fill(0, 0, 0, 39, 0, 59, QUARTZ_BLOCK)

# Walls
s.hollow_box(2, 0, 2, 37, 25, 57, STONE_BRICKS)

# Columns along the sides
for z in range(8, 52, 8):
    s.column(5, 1, z, 24, QUARTZ_BLOCK, GOLD_BLOCK, GOLD_BLOCK, width=2)
    s.column(34, 1, z, 24, QUARTZ_BLOCK, GOLD_BLOCK, GOLD_BLOCK, width=2)

# Arched windows
for z in range(10, 50, 12):
    s.window(2, 8, z, 4, 8, 'west', STONE_BRICKS, BLUE_STAINED_GLASS, 'arch')
    s.window(37, 8, z, 4, 8, 'east', STONE_BRICKS, BLUE_STAINED_GLASS, 'arch')

# Dome roof
s.dome(20, 26, 30, 18, STONE_BRICKS, hollow=True)'''
        },
        {
            'name': 'Modern Office',
            'description': 'A modern office building with glass walls',
            'code': '''from schematic_api import Schematic
from blocks import WHITE_CONCRETE, GLASS, LIGHT_GRAY_CONCRETE, BLACK_CONCRETE

s = Schematic(35, 25, 35)
# Base and structure
s.fill(0, 0, 0, 34, 0, 34, LIGHT_GRAY_CONCRETE)
s.hollow_box(2, 0, 2, 32, 20, 32, WHITE_CONCRETE)

# Window grid on all sides
s.window_grid(2, 2, 2, 2, 18, 32, 3, 3, 2, BLACK_CONCRETE, GLASS)
s.window_grid(32, 2, 2, 32, 18, 32, 3, 3, 2, BLACK_CONCRETE, GLASS)
s.window_grid(2, 2, 2, 32, 18, 2, 3, 3, 2, BLACK_CONCRETE, GLASS)
s.window_grid(2, 2, 32, 32, 18, 32, 3, 3, 2, BLACK_CONCRETE, GLASS)

# Entrance
s.door(15, 0, 2, 'north', None, 3, 4, BLACK_CONCRETE)

# Interior columns
for x, z in [(10, 10), (10, 24), (24, 10), (24, 24)]:
    s.column(x, 1, z, 19, LIGHT_GRAY_CONCRETE, width=1)'''
        },
        {
            'name': 'Geometric Art',
            'description': 'Abstract geometric shapes',
            'code': '''from schematic_api import Schematic
from blocks import GOLD_BLOCK, DIAMOND_BLOCK, EMERALD_BLOCK, REDSTONE_BLOCK

s = Schematic(50, 50, 50)
# Torus
s.torus(25, 15, 25, 12, 3, GOLD_BLOCK, axis='y')

# Ellipsoid
s.ellipsoid(25, 35, 25, 8, 12, 6, DIAMOND_BLOCK, hollow=True)

# Cone
s.cone(10, 0, 10, 8, 20, EMERALD_BLOCK, hollow=False)

# Conditional fill - sphere pattern
s.fill_if(30, 0, 30, 45, 15, 45, REDSTONE_BLOCK, 
          lambda x,y,z: ((x-37.5)**2 + (y-7.5)**2 + (z-37.5)**2) < 64)'''
        },
        {
            'name': 'Furnished Room',
            'description': 'A cozy room with all furniture',
            'code': '''from schematic_api import Schematic
from blocks import BRICKS, OAK_PLANKS, DARK_OAK_PLANKS, SPRUCE_PLANKS, GLASS

s = Schematic(20, 12, 20)
# Create room
s.room(1, 0, 1, 18, 8, 18, BRICKS, OAK_PLANKS, SPRUCE_PLANKS,
       windows=True, door_pos=(9, 0, 1), window_style='grid')

# Add patterned floor
s.floor_pattern(2, 1, 2, 17, 17, [OAK_PLANKS, DARK_OAK_PLANKS], 
                'tile', DARK_OAK_PLANKS)

# Furniture arrangement
s.furniture(4, 1, 4, 'desk', DARK_OAK_PLANKS)
s.furniture(4, 1, 8, 'chair', DARK_OAK_PLANKS, 'north')
s.furniture(12, 1, 4, 'table', DARK_OAK_PLANKS)
s.furniture(10, 1, 7, 'chair', DARK_OAK_PLANKS, 'south')
s.furniture(14, 1, 7, 'chair', DARK_OAK_PLANKS, 'north')
s.furniture(4, 1, 14, 'bed', DARK_OAK_PLANKS, 'east')
s.furniture(14, 1, 14, 'shelf', DARK_OAK_PLANKS)'''
        }
    ]
    
    return jsonify({'examples': examples})




if __name__ == '__main__':
    print("=" * 60)
    print("Minecraft Schematic Builder Server")
    print("=" * 60)
    print("\nServer starting on http://localhost:5000")
    print("\nOpen your browser to http://localhost:5000 to use the viewer")
    print("\nAPI Endpoints:")
    print("  GET  /api/blocks    - List all available blocks")
    print("  POST /api/execute   - Execute schematic code")
    print("  POST /api/export    - Export schematic to .schem file")
    print("  GET  /api/examples  - Get example scripts")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
