import sys
import pygame as pg

from settings import *
from level import *


class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.SCALED)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        # Holding buttons will repeat a 'push' after 100ms
        pg.key.set_repeat(500, 100)

        # Create level manager instance
        self.level_manager = LevelManager()

    def quit(self):
        pg.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()

            self.screen.fill("black")
            self.level_manager.run()
            debug_info(f"{self.level_manager.player.rect}")
            pg.display.update()
            self.clock.tick(FPS)


def debug_info(info, y=10, x=10):
    font = pg.font.Font(None, 20)
    display_surface = pg.display.get_surface()
    debug_surf = font.render(str(info), True, "White")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pg.draw.rect(display_surface, "Black", debug_rect)  # Background
    display_surface.blit(debug_surf, debug_rect)  # Text


if __name__ == "__main__":
    game = Game()
    game.run()
