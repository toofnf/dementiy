import copy
import random
import pygame
from pygame.locals import *
from typing import List, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self,
                 width: int = 640,
                 height: int = 480,
                 cell_size: int = 10,
                 speed: int = 10) -> None:
        """

        :param width: ширина окна
        :param height: высота окна
        :param cell_size: высота и ширина клетки (по умолчанию 10px)
        :param speed: скорость движения клеток
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = None

    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color('black'),
                (x, 0),
                (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color('black'),
                (0, y),
                (self.width, y)
            )

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self,
                    randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1,
        в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой,
            иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        options = [0, 1]
        grid = [
            [
                random.choice(options) if randomize else 0
                for _ in range(self.cell_width)
            ]
            for _ in range(self.cell_height)
        ]

        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        if self.grid is None:
            print('Начальное состояние')
            self.grid = self.create_grid(randomize=True)
        else:
            self.grid = self.get_next_generation()
        for i, row in enumerate(self.grid):
            for j, dead_cell in enumerate(row):
                pygame.draw.rect(
                    surface=self.screen,
                    color=pygame.Color('white') if dead_cell
                    else pygame.Color('green'),
                    rect=(
                        j * self.cell_size,
                        i * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                )

    def get_neighbours(self,
                       cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        top_left = ((row - 1), (col - 1))
        top = ((row - 1), col)
        top_right = ((row - 1), (col + 1))
        left = (row, (col - 1))
        right = (row, (col + 1))
        bottom_left = ((row + 1),
                       (col - 1))
        bottom = ((row + 1), col)
        bottom_right = ((row + 1),
                        (col + 1))

        full_neighbors = [
            self.grid[row][col]
            for row, col in [
                top_left, top, top_right,
                left, right, bottom_left,
                bottom, bottom_right
            ]
            if
            (self.cell_height - 1 >= row >= 0) and
            (self.cell_width - 1 >= col >= 0)
        ]
        return full_neighbors

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        grid = copy.deepcopy(self.grid)

        for row in range(self.cell_height):
            for col in range(self.cell_width):
                neighbours = self.get_neighbours((row, col))
                alive = neighbours.count(1)
                current = self.grid[row][col]
                if current == 1:
                    if alive not in [2, 3]:
                        grid[row][col] = 0
                else:
                    if alive == 3:
                        grid[row][col] = 1

        return grid


if __name__ == '__main__':
    game = GameOfLife(320, 240, 10)
    # grid = game.create_grid(randomize=True)
    game.run()
