import pygame
from pygame.locals import (
    KEYDOWN,
    QUIT,
    K_RIGHT,
    K_LEFT,
    K_UP,
    K_DOWN,
    K_SPACE
)

from random import choice

from gamestate import GameState


class UserInterface:
    def __init__(self, *, size, cube_size, bg_color, grid_color, food_color, snake_color, font_color, grid=True):
        pygame.init()

        self.window_size = size
        self.width = self.window_size[0]
        self.height = self.window_size[1]

        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Snake')

        self.bg_color = bg_color
        self.grid_color = grid_color
        self.food_color = food_color
        self.snake_color = snake_color
        self.font_color = font_color

        self.cube_size = cube_size

        self.grid = grid
        if self.grid:
            self.grid_surface = pygame.Surface(size)
            self.grid_surface.set_colorkey((0, 0, 0))
            self.set_grid()

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 16)

        self.clock = pygame.time.Clock()

        self.boundary_x = range(self.cube_size, self.width - self.cube_size, self.cube_size)
        self.boundary_y = range(self.cube_size, self.height - self.cube_size, self.cube_size)

        self.game_state = GameState(*self.initial_positions())

        self.running = True
        self.direction_x = 0
        self.direction_y = 0

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    def set_grid(self):
        for i in range(0, self.width, self.cube_size):
            pygame.draw.line(self.grid_surface, self.grid_color, (i, 0), (i, self.height))
            pygame.draw.line(self.grid_surface, self.grid_color, (0, i), (self.width, i))

    def initial_positions(self):
        return (choice(self.boundary_x), choice(self.boundary_y)), (choice(self.boundary_x), choice(self.boundary_y))

    def process_input(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT and self.direction_x != -1:
                    self.direction_y = 0
                    self.direction_x = 1
                elif event.key == K_LEFT and self.direction_x != 1:
                    self.direction_y = 0
                    self.direction_x = -1
                elif event.key == K_UP and self.direction_y != 1:
                    self.direction_x = 0
                    self.direction_y = -1
                elif event.key == K_DOWN and self.direction_y != -1:
                    self.direction_x = 0
                    self.direction_y = 1
                elif event.key == K_SPACE:
                    self.direction_y = 0
                    self.direction_x = 0
                    self.game_state.reset(*self.initial_positions())
            elif event.type == QUIT:
                self.running = False

    def generate_food(self):
        if self.game_state.positions[-1] == self.game_state.food_position:
            food_position = choice(self.boundary_x), choice(self.boundary_y)
            while food_position in self.game_state.positions:
                food_position = choice(self.boundary_x), choice(self.boundary_y)
            return food_position
        return self.game_state.food_position

    def update(self):
        last_cube = self.game_state.positions[-1]
        new_position = (
            last_cube[0] + self.cube_size * self.direction_x,
            last_cube[1] + self.cube_size * self.direction_y
        )
        self.check_collision(new_position)
        self.check_boundaries(new_position)

        if self.game_state.is_over:
            self.direction_y = 0
            self.direction_x = 0

        food_position = self.generate_food()
        self.game_state.update(new_position, food_position)

    def render(self):
        self.window.fill(self.bg_color)

        if self.grid:
            self.window.blit(self.grid_surface, (0, 0))

        food = pygame.Rect(self.game_state.food_position, (self.cube_size, self.cube_size))
        pygame.draw.rect(self.window, self.food_color, food)

        # drawing body
        for position in self.game_state.positions:
            pygame.draw.rect(
                self.window, self.snake_color,
                pygame.Rect((position[0], position[1]), (self.cube_size, self.cube_size))
            )

        if self.game_state.is_over:
            self.window.blit(
                self.font.render(
                    f'Final score: {self.game_state.score}. Press spacebar to restart',
                    True,
                    self.font_color,
                    self.bg_color
                ), (10, 10)
            )
        else:
            self.window.blit(
                self.font.render(
                    f'Score: {self.game_state.score}',
                    True,
                    self.font_color,
                    self.bg_color
                ), (10, 10)
            )
        pygame.display.update()

    def check_boundaries(self, position):
        if position[0] not in self.boundary_x or position[1] not in self.boundary_y:
            self.game_state.is_over = True

    def check_collision(self, position):
        if position in self.game_state.positions[:-1]:
            self.game_state.is_over = True

    def run(self):
        while self.running:
            self.process_input()
            if not self.game_state.is_over:
                self.update()
            self.render()
            self.clock.tick(15)
