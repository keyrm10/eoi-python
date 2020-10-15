import random
from pygame import Vector2
from os import path
from sprites import *
from settings import *


class Map:
    def __init__(self):
        self.map_data = []
        self.player_entry_point = Vector2(0, 0)

    def load_from_file(self, filename):
        game_dir = path.dirname(__file__)
        data_dir = path.join(game_dir, "data")

        with open(path.join(data_dir, filename)) as f:
            for line in f:
                self.map_data.append(line)

    def carve_cave_cellular_automata(self, game, width, height):
        width = width // TILESIZE
        height = height // TILESIZE
        self.width = width
        self.height = height

        self.map_data = [
            [
                "1"
                if y == 0 or y == (height - 1) or x == 0 or x == (width - 1)
                else "0"
                for x in range(0, width)
            ]
            for y in range(0, height)
        ]

        starting_walls = (int)(width * height * 0.4)
        for _ in range(0, starting_walls):
            x = random.randint(1, width - 1)
            y = random.randint(1, height - 1)
            self.map_data[y][x] = "1"

        iterations = 10
        neighbour_delta = [
            (x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0
        ]

        for _ in range(iterations):
            tmp_map = self.map_data.copy()
            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    sum = 0
                    for delta in neighbour_delta:
                        dx, dy = delta
                        if self.map_data[y + dy][x + dx] == "1":
                            sum += 1
                    if tmp_map[y][x] == "1":
                        tmp_map[y][x] = "1" if sum >= 3 else "0"
                    else:
                        tmp_map[y][x] = "1" if sum >= 5 else "0"
            self.map_data = tmp_map.copy()

    def get_empty_position(self):
        is_empty = False
        while is_empty == False:
            x = random.randint(1, self.width - 1)
            y = random.randint(1, self.height - 1)
            if self.map_data[y][x] == "0":
                return (x, y)

    def create_sprites_from_map_data(self, game):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                position = Vector2(col, row) * TILESIZE
                if tile == "1":
                    Wall(game, col, row)
                if tile == "P":
                    self.player_entry_point = position
                if tile == "b":
                    Bee(
                        game,
                        position,
                        BEE_MAX_SPEED,
                        BEE_ACCELERATION,
                        BEE_HEALTH,
                        BEE_HIT_DAMAGE,
                        ORANGE,
                    )
                if tile == "B":
                    BeeNest(
                        game,
                        position,
                        BEE_NEST_HEALTH,
                        BEE_NEST_SPAWN_FREQUENCY,
                        BEE_NEST_MAX_POPULATION,
                        DARKORANGE,
                    )
                if tile == "h":
                    HealthPack(game, position)
                if tile == "s":
                    SpeedUp(game, position)
                if tile == "T":
                    Tower(game, position)
