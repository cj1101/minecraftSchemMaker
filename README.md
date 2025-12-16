# Minecraft Schematic Builder

A code-driven Python tool for creating Minecraft schematics with real-time 3D preview and export to `.schem` format.

## Features

- 🎨 **Code-Driven Creation** - Write Python scripts to generate schematics programmatically
- 🌐 **Web-Based 3D Viewer** - Real-time preview with Three.js
- 📦 **Export to .schem** - Compatible with WorldEdit and other Minecraft tools
- 🤖 **AI Integration** - REST API for Gemini and other AI assistants
- 🎯 **Shape Generators** - Built-in functions for spheres, cylinders, boxes, and more

## Quick Start

### Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
python server.py
```

The server will start on `http://localhost:5000`. Open this URL in your browser to access the viewer.

### Basic Usage

1. **Write Code** - In the left panel, write Python code using the Schematic API
2. **Run** - Click the "Run" button or press `Ctrl+Enter`
3. **Preview** - View your structure in the 3D viewer (right panel)
4. **Export** - Click "Export .schem" to download the file

### Example Code

```python
from schematic_api import Schematic
from blocks import STONE, GLASS, OAK_PLANKS

# Create a 10x10x10 schematic
s = Schematic(10, 10, 10)

# Build a stone floor
s.fill(0, 0, 0, 9, 0, 9, STONE)

# Create a glass room
s.hollow_box(2, 1, 2, 7, 5, 7, GLASS)

# Add a wooden roof
s.fill(2, 6, 2, 7, 6, 7, OAK_PLANKS)
```

## API Reference

See [API_REFERENCE.md](API_REFERENCE.md) for complete documentation of all available methods and blocks.

### Quick API Overview

**Creating a Schematic:**
```python
s = Schematic(width, height, length)
```

**Placing Blocks:**
```python
s.set_block(x, y, z, block)           # Single block
s.fill(x1, y1, z1, x2, y2, z2, block) # Fill region
```

**Shapes:**
```python
s.hollow_box(x1, y1, z1, x2, y2, z2, block)
s.sphere(cx, cy, cz, radius, block, hollow=False)
s.cylinder(cx, cz, y1, y2, radius, block, hollow=False)
```

## REST API

The server provides a REST API for programmatic access:

### Endpoints

**Execute Code**
```http
POST /api/execute
Content-Type: application/json

{
  "code": "from schematic_api import Schematic\n..."
}
```

**Export Schematic**
```http
POST /api/export
Content-Type: application/json

{
  "filename": "my_structure"
}
```

**Get Available Blocks**
```http
GET /api/blocks
```

**Get Example Scripts**
```http
GET /api/examples
```

## Using with Gemini

You can use Gemini to generate schematic code for you:

1. Provide the [API_REFERENCE.md](API_REFERENCE.md) file to Gemini
2. Ask Gemini to create a structure (e.g., "create a medieval castle")
3. Copy the generated code into the viewer
4. Run and preview the result
5. Export when satisfied

### Example Gemini Prompt

```
Using the Minecraft Schematic Builder API, create a medieval castle with:
- Stone brick walls
- Corner towers
- A main keep
- Windows and battlements
```

## Examples

Check the `examples/` directory for sample scripts:

- `simple_house.py` - Basic house with walls, windows, and roof
- `tower.py` - Tall tower with multiple floors
- `sphere.py` - Nested spheres demonstration

## Project Structure

```
minecraftSchemMaker/
├── server.py              # Flask server
├── schematic_api.py       # Core schematic API
├── blocks.py              # Block type definitions
├── nbt_exporter.py        # .schem file exporter
├── requirements.txt       # Python dependencies
├── static/
│   ├── viewer.html        # Web viewer interface
│   ├── viewer.js          # Three.js visualization
│   └── styles.css         # Styling
├── examples/              # Example scripts
│   ├── simple_house.py
│   ├── tower.py
│   └── sphere.py
└── API_REFERENCE.md       # Complete API documentation
```

## Available Blocks

35+ block types including:
- Building materials (stone, bricks, wood, glass)
- Natural blocks (dirt, grass, sand)
- Decorative blocks (wool, metal blocks)
- Special blocks (glowstone, water, lava)

See [API_REFERENCE.md](API_REFERENCE.md) for the complete list.

## Loading Schematics in Minecraft

1. Export your schematic from the viewer
2. Copy the `.schem` file to your WorldEdit schematics folder:
   - `<minecraft>/config/worldedit/schematics/`
3. In Minecraft with WorldEdit installed:
   ```
   //load <filename>
   //paste
   ```

## Requirements

- Python 3.7+
- Flask
- nbtlib
- numpy
- Modern web browser with WebGL support

## Troubleshooting

**Server won't start:**
- Check if port 5000 is already in use
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**3D viewer is blank:**
- Check browser console for errors
- Ensure WebGL is enabled in your browser
- Try a different browser (Chrome/Firefox recommended)

**Export fails:**
- Make sure you've run code first to create a schematic
- Check the browser console for error messages

**Schematic doesn't load in Minecraft:**
- Verify you're using WorldEdit or a compatible plugin
- Check the Minecraft version compatibility
- Ensure the file is in the correct schematics folder

## License

This project is open source and available for personal and educational use.

## Contributing

Contributions are welcome! Feel free to:
- Add new block types
- Improve the 3D viewer
- Add new shape generators
- Create example scripts
- Improve documentation

## Credits

- Built with Flask, Three.js, and nbtlib
- Sponge Schematic Specification for .schem format
- WorldEdit for Minecraft integration
