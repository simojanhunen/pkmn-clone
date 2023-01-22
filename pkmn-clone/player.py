import pygame as pg
import os

from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacles):
        super().__init__(groups)

        # Sprites the player collides with
        self.obstacles = obstacles

        player_image_path = os.path.join(ASSETS_DIRECTORY, "player.png")
        player_image = pg.image.load(player_image_path).convert_alpha()
        self.image = player_image

        # Position and collision variables
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -8)

        # Movement variables
        self.vel = pg.math.Vector2(0, 0)
        self.speed = 3

    def get_keys(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -1.0
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = 1.0
        else:
            self.vel.x = 0.0

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -1.0
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = 1.0
        else:
            self.vel.y = 0.0

    def collide_with_walls_x(self):
        for sprite in self.obstacles:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.vel.x > 0:  # Moving right
                    self.hitbox.right = sprite.hitbox.left
                if self.vel.x < 0:  # Moving left
                    self.hitbox.left = sprite.hitbox.right

    def collide_with_walls_y(self):
        for sprite in self.obstacles:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.vel.y > 0:  # Moving down
                    self.hitbox.bottom = sprite.hitbox.top
                if self.vel.y < 0:  # Moving up
                    self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.get_keys()

        if self.vel.magnitude() != 0:
            self.vel = self.vel.normalize()

        # X-axis direction movement
        self.hitbox.x += self.vel.x * self.speed
        self.collide_with_walls_x()

        # Y-axis direction movement
        self.hitbox.y += self.vel.y * self.speed
        self.collide_with_walls_y()

        # After boundaries are checked and the hitbox has been realigned, set rect to hitbox
        self.rect.center = self.hitbox.center
