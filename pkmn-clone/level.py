import pygame as pg
import os
from pytmx.util_pygame import load_pygame

from settings import *
from player import *
from tile import *


class LevelManager:
    def __init__(self):
        self.display_surface = pg.display.get_surface()

        # Everything displayed in the game in decreasing priority order
        self.background_sprites = YSortCameraGroup()
        self.background_detailed_sprites = YSortCameraGroup()
        self.middleground_sprites = YSortCameraGroup()
        self.middleground_detailed_sprites = YSortCameraGroup()
        self.foreground_sprites = YSortCameraGroup()
        self.foreground_detailed_sprites = YSortCameraGroup()

        # Sprites with collision
        self.obstacle_sprites = pg.sprite.Group()

        # Load data and initialize the first level
        self.load_level_data()
        self.create_level()

    def load_level_data(self):
        level_data_file = os.path.join(MAPS_DIRECTORY, "demo.tmx")
        self.level_data = load_pygame(level_data_file)

    def create_level(self):

        # Process each layer and add them to corresponding sprite groups
        self._process_layer("background", [self.background_sprites])
        self._process_layer("background_detailed", [self.background_detailed_sprites])
        self._process_layer(
            "middleground",
            [self.middleground_sprites, self.obstacle_sprites],
        )
        self._process_layer(
            "middleground_detailed",
            [self.middleground_detailed_sprites, self.obstacle_sprites],
        )
        self._process_layer("foreground", [self.foreground_sprites])
        self._process_layer("foreground_detailed", [self.foreground_detailed_sprites])

        # Create player and set it to middleground
        # TODO: Figure a better way (tiled object?)
        self.player = Player(
            (2 * self.level_data.tilewidth, 2 * self.level_data.tilewidth),
            [self.middleground_sprites],
            self.obstacle_sprites,
        )

    def _process_layer(self, layer_name, groups):
        layer = self.level_data.get_layer_by_name(layer_name)

        for (x, y, gid) in layer:
            if image := self.level_data.get_tile_image_by_gid(gid):
                pos = (x * self.level_data.tilewidth, y * self.level_data.tilewidth)
                Tile(pos=pos, image=image, groups=groups)

    def run(self):
        level_width = self.level_data.width * self.level_data.tilewidth
        level_height = self.level_data.height * self.level_data.tileheight

        # Background
        self.background_sprites.custom_draw(self.player, (level_width, level_height))
        self.background_detailed_sprites.custom_draw(
            self.player,
            (level_width, level_height),
        )

        # Middleground
        self.middleground_sprites.custom_draw(self.player, (level_width, level_height))
        self.middleground_sprites.update()
        self.middleground_detailed_sprites.custom_draw(
            self.player,
            (level_width, level_height),
        )

        # Foreground
        self.foreground_sprites.custom_draw(self.player, (level_width, level_height))
        self.foreground_detailed_sprites.custom_draw(
            self.player,
            (level_width, level_height),
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
