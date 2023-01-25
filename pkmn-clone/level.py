import pygame as pg
import os
from pytmx.util_pygame import load_pygame

from settings import *
from player import *
from tile import *


class LevelManager:
    def __init__(self):
        self.display_surface = pg.display.get_surface()

        # Sprite group in order of drawing
        self.sprite_layers = {
            "0": YSortCameraGroup(),
            "1": YSortCameraGroup(),
            "2": YSortCameraGroup(),
            "3": YSortCameraGroup(),
            "4": YSortCameraGroup(),
        }

        # Sprites with collision
        self.obstacle_sprites = pg.sprite.Group()

        # Load data and initialize the first level
        self.load_level_data()
        self.create_level()

    def load_level_data(self):
        level_data_file = os.path.join(MAPS_DIRECTORY, "hometown.tmx")
        self.level_data = load_pygame(level_data_file)

    def create_level(self):
        """
        Reconstructs the level data from level data file to groups of layers
        """
        sprite_layer_names = ["0", "1", "2", "3", "4"]
        obstacles_layer_name = "obstacles"
        water_layer_name = "water"
        consumables_layer_name = "consumables"
        transitions_layer_name = "transition"
        player_layer_name = "player"

        self._process_basic_layers(sprite_layer_names, self.sprite_layers)
        self._process_player_layer(player_layer_name, [self.sprite_layers["2"]])
        self._process_layer(obstacles_layer_name, self.obstacle_sprites)

    def _process_basic_layers(self, layer_names: list, sprite_groups: dict):
        for name in layer_names:
            self._process_layer(name, sprite_groups[name])

    def _process_layer(self, layer_name: str, groups: list):
        layer = self.level_data.get_layer_by_name(layer_name)
        for (x, y, gid) in layer:
            if image := self.level_data.get_tile_image_by_gid(gid):
                pos = (x * self.level_data.tilewidth, y * self.level_data.tilewidth)
                Tile(pos=pos, image=image, groups=groups)

    def _process_player_layer(self, layer_name: str, groups: list):
        layer = self.level_data.get_layer_by_name(layer_name)
        for (x, y, gid) in layer:
            if self.level_data.get_tile_image_by_gid(gid):
                pos = (x * self.level_data.tilewidth, y * self.level_data.tilewidth)
                self.player = Player(pos, groups, self.obstacle_sprites)

    def run(self):
        level_width = self.level_data.width * self.level_data.tilewidth
        level_height = self.level_data.height * self.level_data.tileheight

        for key in self.sprite_layers.keys():
            if key == "2":
                self.sprite_layers[key].custom_draw(
                    self.player, (level_width, level_height)
                )
                self.sprite_layers[key].update()
            else:
                self.sprite_layers[key].custom_draw(
                    self.player, (level_width, level_height)
                )


class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, target, map_size):

        # Offset from player
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

        # # Fix camera to map size
        display_size = self.display_surface.get_size()
        self.offset.x = max(0, self.offset.x)  # left
        self.offset.y = max(0, self.offset.y)  # top
        self.offset.x = min(self.offset.x, (map_size[0] - display_size[0]))  # right
        self.offset.y = min(self.offset.y, (map_size[1] - display_size[1]))  # bottom

        # Draw sprites in y-sorted order
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
