"""
NBT exporter for converting schematics to .schem file format.
Handles the Sponge Schematic Specification v3 format used by WorldEdit 7.x.
"""

import nbtlib
from nbtlib.tag import *
from blocks import AIR
import gzip
import io


class NBTExporter:
    """Exports schematics to .schem NBT format (Sponge Schematic v3)."""
    
    @staticmethod
    def export_schematic(schematic, filename):
        """
        Export a schematic to a .schem file using Sponge Schematic v3 format.
        
        Args:
            schematic: Schematic object to export
            filename: Output filename (should end with .schem)
        """
        # Build the palette (unique block types)
        palette = {}
        palette_index = 0
        
        # Air is always index 0
        # Use block_state string for the palette key
        palette[AIR.block_state] = 0
        palette_index = 1
        
        # Scan schematic for unique blocks
        for x in range(schematic.width):
            for y in range(schematic.height):
                for z in range(schematic.length):
                    block = schematic.blocks[x, y, z]
                    state_string = block.block_state
                    if state_string not in palette:
                        palette[state_string] = palette_index
                        palette_index += 1
        
        # Create block data array
        # Sponge schematic format: entries indexed by x + z * Width + y * Width * Length
        block_data = []
        for y in range(schematic.height):
            for z in range(schematic.length):
                for x in range(schematic.width):
                    block = schematic.blocks[x, y, z]
                    block_data.append(palette[block.block_state])
        
        # Convert block data to varint byte array
        block_data_bytes = NBTExporter._encode_varint_array(block_data)
        
        # Create palette NBT structure for blocks
        palette_nbt = Compound()
        for block_state_str, index in palette.items():
            palette_nbt[block_state_str] = Int(index)
        
        # Build the Blocks container (v3 format)
        blocks_container = Compound({
            'Palette': palette_nbt,
            'Data': ByteArray(block_data_bytes),
            'BlockEntities': List[Compound]([])  # No tile entities for now
        })
        
        # Build the schematic compound (v3 format)
        schematic_data = Compound({
            'Version': Int(3),  # Sponge Schematic Specification version 3
            'DataVersion': Int(3465),  # Minecraft 1.20.4 data version
            'Width': Short(schematic.width),
            'Height': Short(schematic.height),
            'Length': Short(schematic.length),
            'Offset': IntArray([0, 0, 0]),  # No offset
            'Blocks': blocks_container,
            'Entities': List[Compound]([])  # No entities
        })
        
        # Create root compound with "Schematic" wrapper (required by v3)
        root = Compound({
            'Schematic': schematic_data
        })
        
        # Write to file with GZIP compression
        nbt_file = nbtlib.File(root)
        nbt_file.save(filename, gzipped=True)
        
        return filename
    
    @staticmethod
    def _encode_varint_array(values):
        """
        Encode an array of integers as varints.
        
        Args:
            values: List of integers
            
        Returns:
            Byte array
        """
        result = []
        for value in values:
            # Encode as varint
            while True:
                if value & ~0x7F == 0:
                    result.append(value)
                    break
                else:
                    result.append((value & 0x7F) | 0x80)
                    value >>= 7
        return result
