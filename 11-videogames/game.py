#!/usr/bin/env python3

import pygame as pg

from os import path

from settings import *
from sprites import *
from map import Map


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 1024)
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(GAME_TITLE)
        self.display = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.nests = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.players = pg.sprite.Group()

        root_dir = path.dirname(__file__)
        fonts_dir = path.join(root_dir, "fonts")
        img_dir = path.join(root_dir, "img")
        fx_dir = path.join(root_dir, "sound")

        self.title_font = pg.font.Font(path.join(fonts_dir, "title.ttf"), 128)
        self.subtitle_font = pg.font.Font(path.join(fonts_dir, "subtitle.ttf"), 64)
        self.game_over_font = pg.font.Font(path.join(fonts_dir, "subtitle.ttf"), 128)

        self.background_image = pg.image.load(path.join(img_dir, "background.png"))
        self.main_menu_image = pg.image.load(path.join(img_dir, "main_menu.png"))

        self.tile_image_large = pg.image.load(
            path.join(img_dir, "tile.png")
        ).convert_alpha()
        self.tile_image = pg.transform.scale(self.tile_image_large, (24, 24))
        self.player_image = pg.image.load(
            path.join(img_dir, "player.png")
        ).convert_alpha()
        self.virus_image = pg.image.load(
            path.join(img_dir, "virus.png")
        ).convert_alpha()
        self.nest_image = pg.image.load(path.join(img_dir, "nest.png")).convert_alpha()
        self.tower_image = pg.image.load(
            path.join(img_dir, "tower.png")
        ).convert_alpha()
        self.bullet_image_large = pg.image.load(
            path.join(img_dir, "bullet.png")
        ).convert_alpha()
        self.bullet_image = pg.transform.scale(self.bullet_image_large, (8, 8))
        self.heal_image = pg.image.load(path.join(img_dir, "heal.png")).convert_alpha()
        self.speed_image = pg.image.load(
            path.join(img_dir, "speed.png")
        ).convert_alpha()

        self.heal_fx = pg.mixer.Sound(path.join(fx_dir, "heal.wav"))
        self.speed_fx = pg.mixer.Sound(path.join(fx_dir, "speed.wav"))
        self.explosion_fx = pg.mixer.Sound(path.join(fx_dir, "boom.wav"))
        self.music = pg.mixer.music.load(path.join(fx_dir, "music.mp3"))
        pg.mixer.music.play(-1)

    def populate_map(self):
        for _ in range(3):
            x, y = self.map.get_empty_position()
            self.map.map_data[y][x] = "B"

        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "P"

        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "h"

        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "s"

        x, y = self.map.get_empty_position()
        self.map.map_data[y][x] = "T"

    def start_game(self):

        self.all_sprites.empty()
        self.walls.empty()
        self.mobs.empty()

        self.map = Map()
        self.map.carve_cave_cellular_automata(self, WIDTH, HEIGHT)
        self.populate_map()
        self.map.create_sprites_from_map_data(self)
        # self.map.load_from_file("map.txt")

        self.player = Player(
            self,
            self.map.player_entry_point,
            PLAYER_MAX_SPEED,
            PLAYER_ACCELERATION,
            PLAYER_HEALTH,
            YELLOW,
        )

        self.run()

    def run(self):
        self.playing = True
        self.dt = self.clock.tick(FPS) / 1000
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            if self.player.health <= 0:
                self.playing = False
        self.game_over()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.display.blit(self.background_image, (0, 0))
        self.all_sprites.draw(self.display)

        for mob in self.mobs:
            mob.draw_health()

        self.draw_game_ui()

        pg.display.flip()

    def draw_game_ui(self):
        health = self.player.health / self.player.max_health
        padding = 3
        width = 100
        height = 25
        health_background = pg.Rect(5, 5, width, height)
        bar_width = int(health * (width - padding * 2))
        health_fill = pg.Rect(5 + padding, 5 + padding, bar_width, height - padding * 2)
        pg.draw.rect(self.display, DARKBLUE, health_background)
        pg.draw.rect(self.display, BLUE, health_fill)

    def main_menu(self):
        title_text = self.title_font.render("PewPewPew", True, YELLOW)
        instructions_text = self.subtitle_font.render(
            "Press any key to start!", True, WHITE
        )
        self.display.blit(self.main_menu_image, (0, 0))
        self.display.blit(
            title_text,
            (
                WIDTH // 2 - title_text.get_rect().width // 2,
                HEIGHT // 2 - title_text.get_rect().height // 2,
            ),
        )
        self.display.blit(
            instructions_text,
            (WIDTH // 2 - instructions_text.get_rect().width // 2, HEIGHT - 256),
        )
        pg.display.flip()
        pg.time.delay(1000)
        in_main_menu = True
        while in_main_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    in_main_menu = False
        self.start_game()

    def game_over(self):
        title_text = self.game_over_font.render("GAME OVER", True, YELLOW)

        self.display.blit(self.main_menu_image, (0, 0))
        self.display.blit(
            title_text,
            (
                WIDTH // 2 - title_text.get_rect().width // 2,
                HEIGHT // 2 - title_text.get_rect().height // 2,
            ),
        )
        pg.display.flip()
        pg.time.delay(1000)
        in_game_over = True
        while in_game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    in_game_over = False
        self.main_menu()


def main():
    game = Game()
    game.main_menu()


if __name__ == "__main__":
    main()
