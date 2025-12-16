"""
Block type definitions and registry for Minecraft schematics.
Comprehensive block library for Minecraft 1.21.10 with accurate colors.
"""

class Block:
    """Represents a Minecraft block type with its properties."""
    
    def __init__(self, minecraft_id, name, color, properties=None):
        """
        Initialize a block type.
        
        Args:
            minecraft_id: Minecraft namespaced ID (e.g., "minecraft:stone")
            name: Human-readable name
            color: RGB tuple for 3D rendering (0-255)
            properties: Dictionary of block state properties (e.g., {'facing': 'north'})
        """
        self.minecraft_id = minecraft_id
        self.name = name
        self.color = color
        self.properties = properties or {}
    
    @property
    def block_state(self):
        """Returns the full block state string for palettes (e.g., minecraft:stone[variant=andesite])."""
        if not self.properties:
            return self.minecraft_id

        props = ",".join(f"{k}={v}" for k, v in sorted(self.properties.items()))
        return f"{self.minecraft_id}[{props}]"

    def with_properties(self, **kwargs):
        """
        Create a new Block instance with updated properties.

        Args:
            **kwargs: Properties to set or override.

        Returns:
            A new Block instance.
        """
        new_props = self.properties.copy()
        new_props.update(kwargs)
        # Create new instance with same ID, name, color, but new properties
        return Block(self.minecraft_id, self.name, self.color, new_props)

    def __repr__(self):
        if self.properties:
            return f"Block({self.name}, {self.properties})"
        return f"Block({self.name})"

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return (self.minecraft_id == other.minecraft_id and
                self.properties == other.properties)

    def __hash__(self):
        # Convert properties dict to a sorted tuple of items for hashing
        props_tuple = tuple(sorted(self.properties.items()))
        return hash((self.minecraft_id, props_tuple))


# ===== BASIC BLOCKS =====
AIR = Block("minecraft:air", "Air", (0, 0, 0))
STONE = Block("minecraft:stone", "Stone", (128, 128, 128))
GRANITE = Block("minecraft:granite", "Granite", (150, 103, 85))
POLISHED_GRANITE = Block("minecraft:polished_granite", "Polished Granite", (156, 109, 91))
DIORITE = Block("minecraft:diorite", "Diorite", (188, 188, 188))
POLISHED_DIORITE = Block("minecraft:polished_diorite", "Polished Diorite", (200, 200, 200))
ANDESITE = Block("minecraft:andesite", "Andesite", (136, 136, 136))
POLISHED_ANDESITE = Block("minecraft:polished_andesite", "Polished Andesite", (145, 145, 145))

# ===== DEEPSLATE (1.18+) =====
DEEPSLATE = Block("minecraft:deepslate", "Deepslate", (85, 85, 85))
COBBLED_DEEPSLATE = Block("minecraft:cobbled_deepslate", "Cobbled Deepslate", (80, 80, 80))
POLISHED_DEEPSLATE = Block("minecraft:polished_deepslate", "Polished Deepslate", (90, 90, 90))
DEEPSLATE_BRICKS = Block("minecraft:deepslate_bricks", "Deepslate Bricks", (75, 75, 75))
DEEPSLATE_TILES = Block("minecraft:deepslate_tiles", "Deepslate Tiles", (70, 70, 70))
CHISELED_DEEPSLATE = Block("minecraft:chiseled_deepslate", "Chiseled Deepslate", (82, 82, 82))

# ===== TUFF (1.21+) =====
TUFF = Block("minecraft:tuff", "Tuff", (108, 109, 102))
POLISHED_TUFF = Block("minecraft:polished_tuff", "Polished Tuff", (115, 116, 109))
TUFF_BRICKS = Block("minecraft:tuff_bricks", "Tuff Bricks", (110, 111, 104))
CHISELED_TUFF = Block("minecraft:chiseled_tuff", "Chiseled Tuff", (112, 113, 106))
CHISELED_TUFF_BRICKS = Block("minecraft:chiseled_tuff_bricks", "Chiseled Tuff Bricks", (108, 109, 102))

# ===== DIRT & GRASS =====
GRASS_BLOCK = Block("minecraft:grass_block", "Grass Block", (106, 156, 84))
DIRT = Block("minecraft:dirt", "Dirt", (134, 96, 67))
COARSE_DIRT = Block("minecraft:coarse_dirt", "Coarse Dirt", (120, 85, 60))
PODZOL = Block("minecraft:podzol", "Podzol", (90, 65, 40))
MYCELIUM = Block("minecraft:mycelium", "Mycelium", (110, 90, 110))
DIRT_PATH = Block("minecraft:dirt_path", "Dirt Path", (150, 110, 75))

# ===== STONE VARIANTS =====
COBBLESTONE = Block("minecraft:cobblestone", "Cobblestone", (127, 127, 127))
MOSSY_COBBLESTONE = Block("minecraft:mossy_cobblestone", "Mossy Cobblestone", (100, 120, 100))
STONE_BRICKS = Block("minecraft:stone_bricks", "Stone Bricks", (122, 122, 122))
MOSSY_STONE_BRICKS = Block("minecraft:mossy_stone_bricks", "Mossy Stone Bricks", (100, 115, 100))
CRACKED_STONE_BRICKS = Block("minecraft:cracked_stone_bricks", "Cracked Stone Bricks", (115, 115, 115))
CHISELED_STONE_BRICKS = Block("minecraft:chiseled_stone_bricks", "Chiseled Stone Bricks", (120, 120, 120))
SMOOTH_STONE = Block("minecraft:smooth_stone", "Smooth Stone", (160, 160, 160))

# ===== BRICKS =====
BRICKS = Block("minecraft:bricks", "Bricks", (150, 97, 83))
MUD_BRICKS = Block("minecraft:mud_bricks", "Mud Bricks", (140, 105, 90))

# ===== WOOD PLANKS =====
OAK_PLANKS = Block("minecraft:oak_planks", "Oak Planks", (162, 130, 78))
SPRUCE_PLANKS = Block("minecraft:spruce_planks", "Spruce Planks", (114, 84, 48))
BIRCH_PLANKS = Block("minecraft:birch_planks", "Birch Planks", (192, 175, 121))
JUNGLE_PLANKS = Block("minecraft:jungle_planks", "Jungle Planks", (160, 115, 80))
ACACIA_PLANKS = Block("minecraft:acacia_planks", "Acacia Planks", (168, 90, 50))
DARK_OAK_PLANKS = Block("minecraft:dark_oak_planks", "Dark Oak Planks", (66, 43, 20))
MANGROVE_PLANKS = Block("minecraft:mangrove_planks", "Mangrove Planks", (117, 54, 48))
CHERRY_PLANKS = Block("minecraft:cherry_planks", "Cherry Planks", (230, 180, 170))
BAMBOO_PLANKS = Block("minecraft:bamboo_planks", "Bamboo Planks", (196, 176, 96))
CRIMSON_PLANKS = Block("minecraft:crimson_planks", "Crimson Planks", (101, 48, 70))
WARPED_PLANKS = Block("minecraft:warped_planks", "Warped Planks", (43, 104, 99))

# ===== WOOD LOGS =====
OAK_LOG = Block("minecraft:oak_log", "Oak Log", (108, 85, 50))
SPRUCE_LOG = Block("minecraft:spruce_log", "Spruce Log", (58, 37, 16))
BIRCH_LOG = Block("minecraft:birch_log", "Birch Log", (216, 216, 216))
JUNGLE_LOG = Block("minecraft:jungle_log", "Jungle Log", (91, 68, 32))
ACACIA_LOG = Block("minecraft:acacia_log", "Acacia Log", (106, 106, 106))
DARK_OAK_LOG = Block("minecraft:dark_oak_log", "Dark Oak Log", (54, 41, 23))
MANGROVE_LOG = Block("minecraft:mangrove_log", "Mangrove Log", (109, 72, 48))
CHERRY_LOG = Block("minecraft:cherry_log", "Cherry Log", (46, 32, 32))
BAMBOO_BLOCK = Block("minecraft:bamboo_block", "Bamboo Block", (154, 153, 50))
CRIMSON_STEM = Block("minecraft:crimson_stem", "Crimson Stem", (104, 61, 74))
WARPED_STEM = Block("minecraft:warped_stem", "Warped Stem", (58, 90, 84))

# ===== LEAVES =====
OAK_LEAVES = Block("minecraft:oak_leaves", "Oak Leaves", (70, 115, 45))
SPRUCE_LEAVES = Block("minecraft:spruce_leaves", "Spruce Leaves", (55, 95, 55))
BIRCH_LEAVES = Block("minecraft:birch_leaves", "Birch Leaves", (90, 130, 70))
JUNGLE_LEAVES = Block("minecraft:jungle_leaves", "Jungle Leaves", (60, 120, 50))
ACACIA_LEAVES = Block("minecraft:acacia_leaves", "Acacia Leaves", (70, 110, 40))
DARK_OAK_LEAVES = Block("minecraft:dark_oak_leaves", "Dark Oak Leaves", (50, 90, 30))
MANGROVE_LEAVES = Block("minecraft:mangrove_leaves", "Mangrove Leaves", (65, 105, 45))
CHERRY_LEAVES = Block("minecraft:cherry_leaves", "Cherry Leaves", (255, 182, 193))
AZALEA_LEAVES = Block("minecraft:azalea_leaves", "Azalea Leaves", (75, 120, 50))

# ===== SAND & SANDSTONE =====
SAND = Block("minecraft:sand", "Sand", (219, 211, 160))
RED_SAND = Block("minecraft:red_sand", "Red Sand", (190, 102, 33))
SANDSTONE = Block("minecraft:sandstone", "Sandstone", (216, 203, 155))
SMOOTH_SANDSTONE = Block("minecraft:smooth_sandstone", "Smooth Sandstone", (222, 209, 161))
CHISELED_SANDSTONE = Block("minecraft:chiseled_sandstone", "Chiseled Sandstone", (218, 205, 157))
CUT_SANDSTONE = Block("minecraft:cut_sandstone", "Cut Sandstone", (220, 207, 159))
RED_SANDSTONE = Block("minecraft:red_sandstone", "Red Sandstone", (186, 99, 30))
SMOOTH_RED_SANDSTONE = Block("minecraft:smooth_red_sandstone", "Smooth Red Sandstone", (192, 105, 36))

# ===== GLASS =====
GLASS = Block("minecraft:glass", "Glass", (200, 220, 255))
TINTED_GLASS = Block("minecraft:tinted_glass", "Tinted Glass", (60, 50, 50))
WHITE_STAINED_GLASS = Block("minecraft:white_stained_glass", "White Stained Glass", (255, 255, 255))
BLACK_STAINED_GLASS = Block("minecraft:black_stained_glass", "Black Stained Glass", (25, 25, 25))
RED_STAINED_GLASS = Block("minecraft:red_stained_glass", "Red Stained Glass", (153, 51, 51))
BLUE_STAINED_GLASS = Block("minecraft:blue_stained_glass", "Blue Stained Glass", (51, 76, 178))
GREEN_STAINED_GLASS = Block("minecraft:green_stained_glass", "Green Stained Glass", (102, 127, 51))
YELLOW_STAINED_GLASS = Block("minecraft:yellow_stained_glass", "Yellow Stained Glass", (229, 229, 51))

# ===== WOOL =====
WOOL_WHITE = Block("minecraft:white_wool", "White Wool", (233, 236, 236))
WOOL_ORANGE = Block("minecraft:orange_wool", "Orange Wool", (216, 127, 51))
WOOL_MAGENTA = Block("minecraft:magenta_wool", "Magenta Wool", (178, 76, 216))
WOOL_LIGHT_BLUE = Block("minecraft:light_blue_wool", "Light Blue Wool", (102, 153, 216))
WOOL_YELLOW = Block("minecraft:yellow_wool", "Yellow Wool", (248, 198, 39))
WOOL_LIME = Block("minecraft:lime_wool", "Lime Wool", (127, 204, 25))
WOOL_PINK = Block("minecraft:pink_wool", "Pink Wool", (237, 141, 172))
WOOL_GRAY = Block("minecraft:gray_wool", "Gray Wool", (76, 76, 76))
WOOL_LIGHT_GRAY = Block("minecraft:light_gray_wool", "Light Gray Wool", (153, 153, 153))
WOOL_CYAN = Block("minecraft:cyan_wool", "Cyan Wool", (76, 127, 153))
WOOL_PURPLE = Block("minecraft:purple_wool", "Purple Wool", (127, 63, 178))
WOOL_BLUE = Block("minecraft:blue_wool", "Blue Wool", (53, 57, 157))
WOOL_BROWN = Block("minecraft:brown_wool", "Brown Wool", (127, 84, 56))
WOOL_GREEN = Block("minecraft:green_wool", "Green Wool", (85, 109, 27))
WOOL_RED = Block("minecraft:red_wool", "Red Wool", (160, 39, 34))
WOOL_BLACK = Block("minecraft:black_wool", "Black Wool", (20, 21, 25))

# ===== CONCRETE =====
WHITE_CONCRETE = Block("minecraft:white_concrete", "White Concrete", (207, 213, 214))
ORANGE_CONCRETE = Block("minecraft:orange_concrete", "Orange Concrete", (224, 97, 1))
MAGENTA_CONCRETE = Block("minecraft:magenta_concrete", "Magenta Concrete", (169, 48, 159))
LIGHT_BLUE_CONCRETE = Block("minecraft:light_blue_concrete", "Light Blue Concrete", (36, 137, 199))
YELLOW_CONCRETE = Block("minecraft:yellow_concrete", "Yellow Concrete", (240, 175, 21))
LIME_CONCRETE = Block("minecraft:lime_concrete", "Lime Concrete", (94, 168, 24))
PINK_CONCRETE = Block("minecraft:pink_concrete", "Pink Concrete", (214, 101, 143))
GRAY_CONCRETE = Block("minecraft:gray_concrete", "Gray Concrete", (55, 58, 62))
LIGHT_GRAY_CONCRETE = Block("minecraft:light_gray_concrete", "Light Gray Concrete", (125, 125, 115))
CYAN_CONCRETE = Block("minecraft:cyan_concrete", "Cyan Concrete", (21, 119, 136))
PURPLE_CONCRETE = Block("minecraft:purple_concrete", "Purple Concrete", (100, 32, 156))
BLUE_CONCRETE = Block("minecraft:blue_concrete", "Blue Concrete", (45, 47, 143))
BROWN_CONCRETE = Block("minecraft:brown_concrete", "Brown Concrete", (96, 60, 32))
GREEN_CONCRETE = Block("minecraft:green_concrete", "Green Concrete", (73, 91, 36))
RED_CONCRETE = Block("minecraft:red_concrete", "Red Concrete", (142, 33, 33))
BLACK_CONCRETE = Block("minecraft:black_concrete", "Black Concrete", (8, 10, 15))

# ===== TERRACOTTA =====
TERRACOTTA = Block("minecraft:terracotta", "Terracotta", (152, 94, 67))
WHITE_TERRACOTTA = Block("minecraft:white_terracotta", "White Terracotta", (209, 178, 161))
ORANGE_TERRACOTTA = Block("minecraft:orange_terracotta", "Orange Terracotta", (161, 83, 37))
YELLOW_TERRACOTTA = Block("minecraft:yellow_terracotta", "Yellow Terracotta", (186, 133, 36))
LIME_TERRACOTTA = Block("minecraft:lime_terracotta", "Lime Terracotta", (103, 117, 53))
GREEN_TERRACOTTA = Block("minecraft:green_terracotta", "Green Terracotta", (76, 83, 42))
CYAN_TERRACOTTA = Block("minecraft:cyan_terracotta", "Cyan Terracotta", (86, 91, 91))
LIGHT_BLUE_TERRACOTTA = Block("minecraft:light_blue_terracotta", "Light Blue Terracotta", (113, 108, 137))
BLUE_TERRACOTTA = Block("minecraft:blue_terracotta", "Blue Terracotta", (74, 60, 91))
PURPLE_TERRACOTTA = Block("minecraft:purple_terracotta", "Purple Terracotta", (118, 70, 86))
MAGENTA_TERRACOTTA = Block("minecraft:magenta_terracotta", "Magenta Terracotta", (149, 88, 108))
PINK_TERRACOTTA = Block("minecraft:pink_terracotta", "Pink Terracotta", (161, 78, 78))
RED_TERRACOTTA = Block("minecraft:red_terracotta", "Red Terracotta", (143, 61, 47))
BROWN_TERRACOTTA = Block("minecraft:brown_terracotta", "Brown Terracotta", (77, 51, 36))

# ===== METAL BLOCKS =====
IRON_BLOCK = Block("minecraft:iron_block", "Iron Block", (220, 220, 220))
GOLD_BLOCK = Block("minecraft:gold_block", "Gold Block", (255, 215, 0))
DIAMOND_BLOCK = Block("minecraft:diamond_block", "Diamond Block", (93, 236, 229))
EMERALD_BLOCK = Block("minecraft:emerald_block", "Emerald Block", (80, 220, 108))
NETHERITE_BLOCK = Block("minecraft:netherite_block", "Netherite Block", (68, 61, 62))
COPPER_BLOCK = Block("minecraft:copper_block", "Copper Block", (192, 107, 78))
EXPOSED_COPPER = Block("minecraft:exposed_copper", "Exposed Copper", (161, 125, 103))
WEATHERED_COPPER = Block("minecraft:weathered_copper", "Weathered Copper", (108, 153, 110))
OXIDIZED_COPPER = Block("minecraft:oxidized_copper", "Oxidized Copper", (82, 164, 132))

# ===== ORES & MINERALS =====
COAL_BLOCK = Block("minecraft:coal_block", "Coal Block", (25, 25, 25))
REDSTONE_BLOCK = Block("minecraft:redstone_block", "Redstone Block", (170, 24, 0))
LAPIS_BLOCK = Block("minecraft:lapis_block", "Lapis Block", (31, 67, 140))
QUARTZ_BLOCK = Block("minecraft:quartz_block", "Quartz Block", (235, 229, 222))
SMOOTH_QUARTZ = Block("minecraft:smooth_quartz", "Smooth Quartz", (240, 234, 227))
CHISELED_QUARTZ_BLOCK = Block("minecraft:chiseled_quartz_block", "Chiseled Quartz", (237, 231, 224))
AMETHYST_BLOCK = Block("minecraft:amethyst_block", "Amethyst Block", (133, 97, 191))

# ===== SPECIAL BLOCKS =====
GLOWSTONE = Block("minecraft:glowstone", "Glowstone", (255, 198, 140))
SEA_LANTERN = Block("minecraft:sea_lantern", "Sea Lantern", (172, 199, 190))
SHROOMLIGHT = Block("minecraft:shroomlight", "Shroomlight", (255, 154, 73))
OBSIDIAN = Block("minecraft:obsidian", "Obsidian", (20, 18, 30))
CRYING_OBSIDIAN = Block("minecraft:crying_obsidian", "Crying Obsidian", (40, 20, 60))
BEDROCK = Block("minecraft:bedrock", "Bedrock", (85, 85, 85))
END_STONE = Block("minecraft:end_stone", "End Stone", (221, 224, 165))
END_STONE_BRICKS = Block("minecraft:end_stone_bricks", "End Stone Bricks", (218, 221, 162))
PURPUR_BLOCK = Block("minecraft:purpur_block", "Purpur Block", (169, 125, 169))
PURPUR_PILLAR = Block("minecraft:purpur_pillar", "Purpur Pillar", (171, 127, 171))

# ===== NETHER BLOCKS =====
NETHERRACK = Block("minecraft:netherrack", "Netherrack", (97, 38, 38))
NETHER_BRICKS = Block("minecraft:nether_bricks", "Nether Bricks", (44, 22, 26))
RED_NETHER_BRICKS = Block("minecraft:red_nether_bricks", "Red Nether Bricks", (70, 7, 9))
CHISELED_NETHER_BRICKS = Block("minecraft:chiseled_nether_bricks", "Chiseled Nether Bricks", (46, 24, 28))
CRACKED_NETHER_BRICKS = Block("minecraft:cracked_nether_bricks", "Cracked Nether Bricks", (42, 20, 24))
BASALT = Block("minecraft:basalt", "Basalt", (71, 71, 78))
SMOOTH_BASALT = Block("minecraft:smooth_basalt", "Smooth Basalt", (75, 75, 82))
POLISHED_BASALT = Block("minecraft:polished_basalt", "Polished Basalt", (78, 78, 85))
BLACKSTONE = Block("minecraft:blackstone", "Blackstone", (42, 35, 40))
POLISHED_BLACKSTONE = Block("minecraft:polished_blackstone", "Polished Blackstone", (54, 47, 54))
POLISHED_BLACKSTONE_BRICKS = Block("minecraft:polished_blackstone_bricks", "Polished Blackstone Bricks", (50, 43, 50))
CHISELED_POLISHED_BLACKSTONE = Block("minecraft:chiseled_polished_blackstone", "Chiseled Polished Blackstone", (56, 49, 56))

# ===== PRISMARINE =====
PRISMARINE = Block("minecraft:prismarine", "Prismarine", (99, 156, 151))
PRISMARINE_BRICKS = Block("minecraft:prismarine_bricks", "Prismarine Bricks", (99, 180, 170))
DARK_PRISMARINE = Block("minecraft:dark_prismarine", "Dark Prismarine", (52, 90, 79))

# ===== MISC =====
GRAVEL = Block("minecraft:gravel", "Gravel", (131, 127, 126))
CLAY = Block("minecraft:clay", "Clay", (160, 166, 179))
SNOW_BLOCK = Block("minecraft:snow_block", "Snow Block", (240, 251, 251))
ICE = Block("minecraft:ice", "Ice", (145, 166, 255))
PACKED_ICE = Block("minecraft:packed_ice", "Packed Ice", (141, 180, 250))
BLUE_ICE = Block("minecraft:blue_ice", "Blue Ice", (116, 168, 253))
SPONGE = Block("minecraft:sponge", "Sponge", (195, 195, 77))
HONEYCOMB_BLOCK = Block("minecraft:honeycomb_block", "Honeycomb Block", (229, 148, 29))
SLIME_BLOCK = Block("minecraft:slime_block", "Slime Block", (112, 192, 87))
HONEY_BLOCK = Block("minecraft:honey_block", "Honey Block", (252, 163, 38))

# ===== LIQUIDS =====
WATER = Block("minecraft:water", "Water", (64, 96, 255))
LAVA = Block("minecraft:lava", "Lava", (255, 100, 0))


# Build the comprehensive block registry (Base blocks)
BLOCK_REGISTRY = {block.minecraft_id: block for block in [
    AIR, STONE, GRANITE, POLISHED_GRANITE, DIORITE, POLISHED_DIORITE, ANDESITE, POLISHED_ANDESITE,
    DEEPSLATE, COBBLED_DEEPSLATE, POLISHED_DEEPSLATE, DEEPSLATE_BRICKS, DEEPSLATE_TILES, CHISELED_DEEPSLATE,
    TUFF, POLISHED_TUFF, TUFF_BRICKS, CHISELED_TUFF, CHISELED_TUFF_BRICKS,
    GRASS_BLOCK, DIRT, COARSE_DIRT, PODZOL, MYCELIUM, DIRT_PATH,
    COBBLESTONE, MOSSY_COBBLESTONE, STONE_BRICKS, MOSSY_STONE_BRICKS, CRACKED_STONE_BRICKS, 
    CHISELED_STONE_BRICKS, SMOOTH_STONE, BRICKS, MUD_BRICKS,
    OAK_PLANKS, SPRUCE_PLANKS, BIRCH_PLANKS, JUNGLE_PLANKS, ACACIA_PLANKS, DARK_OAK_PLANKS,
    MANGROVE_PLANKS, CHERRY_PLANKS, BAMBOO_PLANKS, CRIMSON_PLANKS, WARPED_PLANKS,
    OAK_LOG, SPRUCE_LOG, BIRCH_LOG, JUNGLE_LOG, ACACIA_LOG, DARK_OAK_LOG,
    MANGROVE_LOG, CHERRY_LOG, BAMBOO_BLOCK, CRIMSON_STEM, WARPED_STEM,
    OAK_LEAVES, SPRUCE_LEAVES, BIRCH_LEAVES, JUNGLE_LEAVES, ACACIA_LEAVES, DARK_OAK_LEAVES,
    MANGROVE_LEAVES, CHERRY_LEAVES, AZALEA_LEAVES,
    SAND, RED_SAND, SANDSTONE, SMOOTH_SANDSTONE, CHISELED_SANDSTONE, CUT_SANDSTONE,
    RED_SANDSTONE, SMOOTH_RED_SANDSTONE,
    GLASS, TINTED_GLASS, WHITE_STAINED_GLASS, BLACK_STAINED_GLASS, RED_STAINED_GLASS,
    BLUE_STAINED_GLASS, GREEN_STAINED_GLASS, YELLOW_STAINED_GLASS,
    WOOL_WHITE, WOOL_ORANGE, WOOL_MAGENTA, WOOL_LIGHT_BLUE, WOOL_YELLOW, WOOL_LIME,
    WOOL_PINK, WOOL_GRAY, WOOL_LIGHT_GRAY, WOOL_CYAN, WOOL_PURPLE, WOOL_BLUE,
    WOOL_BROWN, WOOL_GREEN, WOOL_RED, WOOL_BLACK,
    WHITE_CONCRETE, ORANGE_CONCRETE, MAGENTA_CONCRETE, LIGHT_BLUE_CONCRETE, YELLOW_CONCRETE,
    LIME_CONCRETE, PINK_CONCRETE, GRAY_CONCRETE, LIGHT_GRAY_CONCRETE, CYAN_CONCRETE,
    PURPLE_CONCRETE, BLUE_CONCRETE, BROWN_CONCRETE, GREEN_CONCRETE, RED_CONCRETE, BLACK_CONCRETE,
    TERRACOTTA, WHITE_TERRACOTTA, ORANGE_TERRACOTTA, YELLOW_TERRACOTTA, LIME_TERRACOTTA,
    GREEN_TERRACOTTA, CYAN_TERRACOTTA, LIGHT_BLUE_TERRACOTTA, BLUE_TERRACOTTA, PURPLE_TERRACOTTA,
    MAGENTA_TERRACOTTA, PINK_TERRACOTTA, RED_TERRACOTTA, BROWN_TERRACOTTA,
    IRON_BLOCK, GOLD_BLOCK, DIAMOND_BLOCK, EMERALD_BLOCK, NETHERITE_BLOCK,
    COPPER_BLOCK, EXPOSED_COPPER, WEATHERED_COPPER, OXIDIZED_COPPER,
    COAL_BLOCK, REDSTONE_BLOCK, LAPIS_BLOCK, QUARTZ_BLOCK, SMOOTH_QUARTZ, CHISELED_QUARTZ_BLOCK,
    AMETHYST_BLOCK, GLOWSTONE, SEA_LANTERN, SHROOMLIGHT,
    OBSIDIAN, CRYING_OBSIDIAN, BEDROCK, END_STONE, END_STONE_BRICKS, PURPUR_BLOCK, PURPUR_PILLAR,
    NETHERRACK, NETHER_BRICKS, RED_NETHER_BRICKS, CHISELED_NETHER_BRICKS, CRACKED_NETHER_BRICKS,
    BASALT, SMOOTH_BASALT, POLISHED_BASALT, BLACKSTONE, POLISHED_BLACKSTONE,
    POLISHED_BLACKSTONE_BRICKS, CHISELED_POLISHED_BLACKSTONE,
    PRISMARINE, PRISMARINE_BRICKS, DARK_PRISMARINE,
    GRAVEL, CLAY, SNOW_BLOCK, ICE, PACKED_ICE, BLUE_ICE, SPONGE,
    HONEYCOMB_BLOCK, SLIME_BLOCK, HONEY_BLOCK, WATER, LAVA
]}


def get_all_blocks():
    """Return a list of all available blocks."""
    return list(BLOCK_REGISTRY.values())


def get_block_by_id(minecraft_id):
    """
    Get a block by its Minecraft ID.
    
    Args:
        minecraft_id: The Minecraft namespaced ID
        
    Returns:
        Block object or None if not found
    """
    return BLOCK_REGISTRY.get(minecraft_id)


def create_block(minecraft_id, properties=None):
    """
    Create a new block dynamically.

    Args:
        minecraft_id: Minecraft ID
        properties: Optional properties dict

    Returns:
        Block instance
    """
    # Check if we have a base block definition for color
    base = BLOCK_REGISTRY.get(minecraft_id)
    color = base.color if base else (255, 0, 255)  # Default magenta for unknown
    name = base.name if base else minecraft_id.split(':')[-1].replace('_', ' ').title()

    return Block(minecraft_id, name, color, properties)


def validate_block(block):
    """
    Validate that a block is a valid Block instance.
    
    Args:
        block: Block to validate
        
    Returns:
        True if valid, False otherwise
    """
    return isinstance(block, Block)

# === DYNAMIC BLOCK HELPERS ===
# These allow creating variations of blocks easily

def stair(material_block, facing='north', half='bottom', shape='straight'):
    """Create a stair block."""
    if not isinstance(material_block, Block):
        raise ValueError("Invalid material block")

    # Determine ID (replace _planks or _block with _stairs usually, or just append _stairs)
    # This is a heuristic. For OAK_PLANKS -> OAK_STAIRS.
    # For STONE -> STONE_STAIRS.
    base_id = material_block.minecraft_id
    if 'planks' in base_id:
        stair_id = base_id.replace('planks', 'stairs')
    elif 'bricks' in base_id:
        stair_id = base_id.replace('bricks', 'brick_stairs') # specific case
        if 'stone_brick_stairs' in stair_id:
            stair_id = stair_id.replace('brick_stairs', 'stairs') # stone_stairs correction
    else:
        stair_id = base_id + "_stairs"

    # Correct some common ones manually if needed, or rely on user passing the correct Stair Block
    # But better: Use the material block's color and name to make a new block

    return Block(
        stair_id,
        f"{material_block.name} Stairs",
        material_block.color,
        {'facing': facing, 'half': half, 'shape': shape}
    )

# For user convenience, we will populate the registry with complex blocks now.
# This list matches 1.21.10 common items.

# Helper to register a list of blocks
def _reg(id_base, name_base, color, variants=None):
    b = Block(f"minecraft:{id_base}", name_base, color)
    BLOCK_REGISTRY[b.minecraft_id] = b
    return b

# Additional 1.21 blocks and variants
CRAFTER = _reg("crafter", "Crafter", (100, 100, 100))
TRIAL_SPAWNER = _reg("trial_spawner", "Trial Spawner", (150, 100, 50))
VAULT = _reg("vault", "Vault", (150, 100, 50))
COPPER_BULB = _reg("copper_bulb", "Copper Bulb", (200, 150, 100))
HEAVY_CORE = _reg("heavy_core", "Heavy Core", (200, 200, 220))

# Redstone
REDSTONE_WIRE = _reg("redstone_wire", "Redstone Wire", (255, 0, 0))
REDSTONE_TORCH = _reg("redstone_torch", "Redstone Torch", (255, 0, 0))
REPEATER = _reg("repeater", "Redstone Repeater", (200, 200, 200))
COMPARATOR = _reg("comparator", "Redstone Comparator", (200, 200, 200))
PISTON = _reg("piston", "Piston", (150, 150, 150))
STICKY_PISTON = _reg("sticky_piston", "Sticky Piston", (150, 180, 150))
OBSERVER = _reg("observer", "Observer", (50, 50, 50))
DISPENSER = _reg("dispenser", "Dispenser", (100, 100, 100))
DROPPER = _reg("dropper", "Dropper", (100, 100, 100))
HOPPER = _reg("hopper", "Hopper", (80, 80, 80))
LEVER = _reg("lever", "Lever", (100, 80, 60))
DAYLIGHT_DETECTOR = _reg("daylight_detector", "Daylight Detector", (200, 180, 120))
SCULK_SENSOR = _reg("sculk_sensor", "Sculk Sensor", (10, 100, 150))
CALIBRATED_SCULK_SENSOR = _reg("calibrated_sculk_sensor", "Calibrated Sculk Sensor", (20, 100, 160))
TRIPWIRE_HOOK = _reg("tripwire_hook", "Tripwire Hook", (100, 100, 100))
TRIPWIRE = _reg("tripwire", "Tripwire", (200, 200, 200))

# Rails
RAIL = _reg("rail", "Rail", (200, 200, 200))
POWERED_RAIL = _reg("powered_rail", "Powered Rail", (255, 200, 100))
DETECTOR_RAIL = _reg("detector_rail", "Detector Rail", (200, 100, 100))
ACTIVATOR_RAIL = _reg("activator_rail", "Activator Rail", (100, 200, 100))

# Doors (Base definitions, typically used with upper/lower props)
OAK_DOOR = _reg("oak_door", "Oak Door", OAK_PLANKS.color)
IRON_DOOR = _reg("iron_door", "Iron Door", IRON_BLOCK.color)
SPRUCE_DOOR = _reg("spruce_door", "Spruce Door", SPRUCE_PLANKS.color)
BIRCH_DOOR = _reg("birch_door", "Birch Door", BIRCH_PLANKS.color)
JUNGLE_DOOR = _reg("jungle_door", "Jungle Door", JUNGLE_PLANKS.color)
ACACIA_DOOR = _reg("acacia_door", "Acacia Door", ACACIA_PLANKS.color)
DARK_OAK_DOOR = _reg("dark_oak_door", "Dark Oak Door", DARK_OAK_PLANKS.color)
MANGROVE_DOOR = _reg("mangrove_door", "Mangrove Door", MANGROVE_PLANKS.color)
CHERRY_DOOR = _reg("cherry_door", "Cherry Door", CHERRY_PLANKS.color)
BAMBOO_DOOR = _reg("bamboo_door", "Bamboo Door", BAMBOO_PLANKS.color)
CRIMSON_DOOR = _reg("crimson_door", "Crimson Door", CRIMSON_PLANKS.color)
WARPED_DOOR = _reg("warped_door", "Warped Door", WARPED_PLANKS.color)
COPPER_DOOR = _reg("copper_door", "Copper Door", COPPER_BLOCK.color)
EXPOSED_COPPER_DOOR = _reg("exposed_copper_door", "Exposed Copper Door", EXPOSED_COPPER.color)
WEATHERED_COPPER_DOOR = _reg("weathered_copper_door", "Weathered Copper Door", WEATHERED_COPPER.color)
OXIDIZED_COPPER_DOOR = _reg("oxidized_copper_door", "Oxidized Copper Door", OXIDIZED_COPPER.color)

# Trapdoors
OAK_TRAPDOOR = _reg("oak_trapdoor", "Oak Trapdoor", OAK_PLANKS.color)
IRON_TRAPDOOR = _reg("iron_trapdoor", "Iron Trapdoor", IRON_BLOCK.color)
SPRUCE_TRAPDOOR = _reg("spruce_trapdoor", "Spruce Trapdoor", SPRUCE_PLANKS.color)
BIRCH_TRAPDOOR = _reg("birch_trapdoor", "Birch Trapdoor", BIRCH_PLANKS.color)
JUNGLE_TRAPDOOR = _reg("jungle_trapdoor", "Jungle Trapdoor", JUNGLE_PLANKS.color)
ACACIA_TRAPDOOR = _reg("acacia_trapdoor", "Acacia Trapdoor", ACACIA_PLANKS.color)
DARK_OAK_TRAPDOOR = _reg("dark_oak_trapdoor", "Dark Oak Trapdoor", DARK_OAK_PLANKS.color)
MANGROVE_TRAPDOOR = _reg("mangrove_trapdoor", "Mangrove Trapdoor", MANGROVE_PLANKS.color)
CHERRY_TRAPDOOR = _reg("cherry_trapdoor", "Cherry Trapdoor", CHERRY_PLANKS.color)
BAMBOO_TRAPDOOR = _reg("bamboo_trapdoor", "Bamboo Trapdoor", BAMBOO_PLANKS.color)
CRIMSON_TRAPDOOR = _reg("crimson_trapdoor", "Crimson Trapdoor", CRIMSON_PLANKS.color)
WARPED_TRAPDOOR = _reg("warped_trapdoor", "Warped Trapdoor", WARPED_PLANKS.color)
COPPER_TRAPDOOR = _reg("copper_trapdoor", "Copper Trapdoor", COPPER_BLOCK.color)

# Fences
OAK_FENCE = _reg("oak_fence", "Oak Fence", OAK_PLANKS.color)
SPRUCE_FENCE = _reg("spruce_fence", "Spruce Fence", SPRUCE_PLANKS.color)
BIRCH_FENCE = _reg("birch_fence", "Birch Fence", BIRCH_PLANKS.color)
JUNGLE_FENCE = _reg("jungle_fence", "Jungle Fence", JUNGLE_PLANKS.color)
ACACIA_FENCE = _reg("acacia_fence", "Acacia Fence", ACACIA_PLANKS.color)
DARK_OAK_FENCE = _reg("dark_oak_fence", "Dark Oak Fence", DARK_OAK_PLANKS.color)
MANGROVE_FENCE = _reg("mangrove_fence", "Mangrove Fence", MANGROVE_PLANKS.color)
CHERRY_FENCE = _reg("cherry_fence", "Cherry Fence", CHERRY_PLANKS.color)
BAMBOO_FENCE = _reg("bamboo_fence", "Bamboo Fence", BAMBOO_PLANKS.color)
CRIMSON_FENCE = _reg("crimson_fence", "Crimson Fence", CRIMSON_PLANKS.color)
WARPED_FENCE = _reg("warped_fence", "Warped Fence", WARPED_PLANKS.color)
NETHER_BRICK_FENCE = _reg("nether_brick_fence", "Nether Brick Fence", NETHER_BRICKS.color)

# Fence Gates
OAK_FENCE_GATE = _reg("oak_fence_gate", "Oak Fence Gate", OAK_PLANKS.color)
SPRUCE_FENCE_GATE = _reg("spruce_fence_gate", "Spruce Fence Gate", SPRUCE_PLANKS.color)
# ... add more if needed, can be created dynamically

# Stairs (Base)
OAK_STAIRS = _reg("oak_stairs", "Oak Stairs", OAK_PLANKS.color)
COBBLESTONE_STAIRS = _reg("cobblestone_stairs", "Cobblestone Stairs", COBBLESTONE.color)
STONE_BRICK_STAIRS = _reg("stone_brick_stairs", "Stone Brick Stairs", STONE_BRICKS.color)
SANDSTONE_STAIRS = _reg("sandstone_stairs", "Sandstone Stairs", SANDSTONE.color)
NETHER_BRICK_STAIRS = _reg("nether_brick_stairs", "Nether Brick Stairs", NETHER_BRICKS.color)
QUARTZ_STAIRS = _reg("quartz_stairs", "Quartz Stairs", QUARTZ_BLOCK.color)
PURPUR_STAIRS = _reg("purpur_stairs", "Purpur Stairs", PURPUR_BLOCK.color)
PRISMARINE_STAIRS = _reg("prismarine_stairs", "Prismarine Stairs", PRISMARINE.color)

# Slabs
OAK_SLAB = _reg("oak_slab", "Oak Slab", OAK_PLANKS.color)
COBBLESTONE_SLAB = _reg("cobblestone_slab", "Cobblestone Slab", COBBLESTONE.color)
STONE_BRICK_SLAB = _reg("stone_brick_slab", "Stone Brick Slab", STONE_BRICKS.color)
SANDSTONE_SLAB = _reg("sandstone_slab", "Sandstone Slab", SANDSTONE.color)
QUARTZ_SLAB = _reg("quartz_slab", "Quartz Slab", QUARTZ_BLOCK.color)
NETHER_BRICK_SLAB = _reg("nether_brick_slab", "Nether Brick Slab", NETHER_BRICKS.color)

# Walls
COBBLESTONE_WALL = _reg("cobblestone_wall", "Cobblestone Wall", COBBLESTONE.color)
MOSSY_COBBLESTONE_WALL = _reg("mossy_cobblestone_wall", "Mossy Cobblestone Wall", MOSSY_COBBLESTONE.color)
STONE_BRICK_WALL = _reg("stone_brick_wall", "Stone Brick Wall", STONE_BRICKS.color)
MUD_BRICK_WALL = _reg("mud_brick_wall", "Mud Brick Wall", MUD_BRICKS.color)

# Decorations
LANTERN = _reg("lantern", "Lantern", (255, 200, 100))
SOUL_LANTERN = _reg("soul_lantern", "Soul Lantern", (100, 200, 255))
CHAIN = _reg("chain", "Chain", (50, 50, 50))
IRON_BARS = _reg("iron_bars", "Iron Bars", (150, 150, 150))
LADDER = _reg("ladder", "Ladder", (139, 69, 19))
SCAFFOLDING = _reg("scaffolding", "Scaffolding", (200, 180, 120))
VINE = _reg("vine", "Vine", (30, 150, 30))
GLOW_LICHEN = _reg("glow_lichen", "Glow Lichen", (100, 150, 150))
LILY_PAD = _reg("lily_pad", "Lily Pad", (30, 150, 30))
CACTUS = _reg("cactus", "Cactus", (30, 150, 30))
SUGAR_CANE = _reg("sugar_cane", "Sugar Cane", (100, 200, 100))
BOOKSHELF = _reg("bookshelf", "Bookshelf", (139, 69, 19))
CHISELED_BOOKSHELF = _reg("chiseled_bookshelf", "Chiseled Bookshelf", (139, 69, 19))
DECORATED_POT = _reg("decorated_pot", "Decorated Pot", (150, 100, 50))
TORCH = _reg("torch", "Torch", (255, 200, 100))
SOUL_TORCH = _reg("soul_torch", "Soul Torch", (100, 200, 255))
END_ROD = _reg("end_rod", "End Rod", (200, 200, 200))
CHEST = _reg("chest", "Chest", (139, 69, 19))
ENDER_CHEST = _reg("ender_chest", "Ender Chest", (30, 30, 50))
BARREL = _reg("barrel", "Barrel", (139, 100, 50))
SHULKER_BOX = _reg("shulker_box", "Shulker Box", (150, 100, 150))

# Beds
WHITE_BED = _reg("white_bed", "White Bed", WOOL_WHITE.color)
RED_BED = _reg("red_bed", "Red Bed", WOOL_RED.color)
