from typing import Final
import os

# Game
WIDTH: Final = 480
HEIGHT: Final = 320
FPS: Final = 60
TITLE: Final = "Unnamed Tile-based RPG"

# Directories
GAME_DIRECTORY = os.path.dirname(__file__)
MAPS_DIRECTORY = os.path.join(GAME_DIRECTORY, "maps")
ASSETS_DIRECTORY = os.path.join(GAME_DIRECTORY, "assets")
