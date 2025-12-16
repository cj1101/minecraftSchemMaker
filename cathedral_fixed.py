# 1. Imports
from schematic_api import Schematic
from blocks import *
import math
import random

# 2. Configuration
# Dimensions massives pour l'effet "cathédrale industrielle"
WIDTH, HEIGHT, LENGTH = 60, 40, 80

# Palette Brutaliste
MAIN_WALL = GRAY_CONCRETE
ACCENT_WALL = LIGHT_GRAY_CONCRETE
FLOOR_MAIN = POLISHED_DEEPSLATE
FLOOR_ACCENT = CRACKED_STONE_BRICKS
PILLAR_BLOCK = CHISELED_STONE_BRICKS
INDUSTRIAL_METAL = IRON_BLOCK
VIBE_LIGHT = RED_STAINED_GLASS
DARKNESS = BLACK_CONCRETE

# 3. Initialization
s = Schematic(WIDTH, HEIGHT, LENGTH)

# 4. The "Shell" (Le Bunker)
# Remplir le tout de "terre" ou de pierre pour simuler le souterrain, puis creuser
s.fill(0, 0, 0, WIDTH-1, HEIGHT-1, LENGTH-1, STONE) 
# Creuser la boîte principale (Main Hall)
s.fill(2, 2, 2, WIDTH-3, HEIGHT-5, LENGTH-3, AIR)

# 5. Architecture Brutaliste (Structure)

# Murs texturés (mélange de béton et de pierre)
for y in range(2, HEIGHT-5):
    for z in range(2, LENGTH-2):
        # Murs latéraux
        if random.random() > 0.8:
            s.set_block(2, y, z, ACCENT_WALL)
            s.set_block(WIDTH-3, y, z, ACCENT_WALL)
        else:
            s.set_block(2, y, z, MAIN_WALL)
            s.set_block(WIDTH-3, y, z, MAIN_WALL)

# Sol principal - motif industriel sombre
s.floor_pattern(3, 2, 3, WIDTH-4, LENGTH-4, [POLISHED_DEEPSLATE, COBBLED_DEEPSLATE, BLACKSTONE], pattern='random')

# Colonnes massives (Signature Berghain)
# Des piliers de 18m de haut
pillar_x_coords = [10, 20, 40, 50]
pillar_z_coords = [15, 35, 55]

for px in pillar_x_coords:
    for pz in pillar_z_coords:
        # Base
        s.fill(px-1, 2, pz-1, px+1, 4, pz+1, OBSIDIAN)
        # Fût
        s.column(px, 5, pz, HEIGHT-8, PILLAR_BLOCK, width=2)
        # Chapiteau industriel (support du plafond)
        s.fill(px-2, HEIGHT-8, pz-2, px+2, HEIGHT-6, pz+2, INDUSTRIAL_METAL)

# 6. Le "Panorama Bar" (Mezzanine)
# Un étage supérieur qui surplombe la piste
mezzanine_z_start = 60
mezzanine_height = 15
s.fill(2, mezzanine_height, mezzanine_z_start, WIDTH-3, mezzanine_height+1, LENGTH-3, POLISHED_ANDESITE)
# Garde-corps
s.wall(2, mezzanine_height+2, mezzanine_z_start, WIDTH-3, mezzanine_height+3, mezzanine_z_start, IRON_BLOCK, thickness=1, battlements=False)

# Escalier monumental en béton (accès mezzanine)
s.staircase(5, 2, 45, 'south', length=20, block=SMOOTH_STONE) # Monte vers le sud
# Plateforme intermédiaire
s.fill(4, 12, 65, 8, 12, 68, SMOOTH_STONE)
s.staircase(8, 12, 65, 'east', length=10, block=SMOOTH_STONE) # Tourne vers l'est

# 7. La Cabine DJ (L'Autel)
# Située au fond de la salle principale, surélevée
dj_x, dj_y, dj_z = WIDTH//2, 6, 10
# Base fortifiée
s.fill(dj_x-4, 2, dj_z-2, dj_x+4, dj_y, dj_z+2, DEEPSLATE_TILES)
# Table
s.fill(dj_x-2, dj_y+1, dj_z-1, dj_x+2, dj_y+1, dj_z, BLACK_CONCRETE)
# Enceintes massives (Funktion-One style stacks)
for side in [-6, 6]:
    # Gauche et Droite
    s.fill(dj_x+side-1, 2, dj_z, dj_x+side+1, 8, dj_z+1, WOOL_BLACK)  # FIXED: BLACK_WOOL -> WOOL_BLACK
    s.set_block(dj_x+side, 6, dj_z, OBSIDIAN) # Tweeter

# 8. Éclairage & Ambiance

# Plafond sombre avec des "trous" de lumière
s.fill(2, HEIGHT-6, 2, WIDTH-3, HEIGHT-5, LENGTH-3, DARKNESS)

# Lumières rouges stroboscopiques (éparses)
for i in range(30):
    lx = random.randint(5, WIDTH-5)
    lz = random.randint(5, LENGTH-5)
    ly = HEIGHT-7
    s.set_block(lx, ly, lz, SEA_LANTERN)
    s.set_block(lx, ly-1, lz, RED_STAINED_GLASS) # Filtre rouge

# Éclairage au sol (bandes LED)
s.fill(2, 2, 2, WIDTH-3, 2, 2, SEA_LANTERN)
s.fill(2, 3, 2, WIDTH-3, 3, 2, GLASS) # Protection

# 9. Zones "Darkroom" & Chillout (Sous la mezzanine)
# Créer des petits murs de séparation pour des recoins sombres
for z in range(65, 75, 4):
    s.wall(15, 2, z, 25, 6, z, DARK_PRISMARINE, thickness=1)
    s.furniture(18, 2, z+1, 'chair', NETHER_BRICKS) # Banquettes sombres

# Bar Industriel (Zinc)
bar_x = 45
bar_z_start = 65
s.fill(bar_x, 2, bar_z_start, bar_x+2, 4, bar_z_start+10, IRON_BLOCK)
s.fill(bar_x+1, 5, bar_z_start, bar_x+1, 5, bar_z_start+10, SEA_LANTERN) # Comptoir lumineux
s.fill(bar_x+1, 6, bar_z_start, bar_x+1, 6, bar_z_start+10, TINTED_GLASS)

# 10. Entrée (File d'attente / The Queue)
# Un long couloir étroit et oppressant à l'extérieur (ou début du schem)
s.fill(WIDTH//2 - 2, 2, 0, WIDTH//2 + 2, 8, 5, AIR) # Tunnel d'entrée
s.door(WIDTH//2, 2, 5, 'north', IRON_BLOCK)
