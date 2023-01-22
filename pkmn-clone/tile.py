import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, image, groups):
        pg.sprite.Sprite.__init__(self, groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -4)
