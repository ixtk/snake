import pygame

from ui import UserInterface


def main():
    theme = {
        'bg_color': (255, 255, 255),
        'grid_color': (194, 194, 194),
        'food_color': (0, 255, 0),
        'snake_color': (255, 0, 0),
        'font_color': (0, 0, 0)
    }

    UI = UserInterface(
        size=(500, 500),
        cube_size=25,
        **theme,
        grid=True
    )

    UI.run()

    pygame.quit()


if __name__ == '__main__':
    main()
