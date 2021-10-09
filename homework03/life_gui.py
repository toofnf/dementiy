import pygame
import argparse
import pathlib
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):

    def __init__(self,
                 life: GameOfLife,
                 cell_size: int = 10,
                 speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.rows * self.cell_size
        self.height = self.life.cols * self.cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
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

    def draw_grid(self) -> None:
        for i, row in enumerate(self.life.curr_generation):
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

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.life.create_grid(randomize=True)

        pause, running = True, True
        while (
                running and self.life.is_changing
                and not self.life.is_max_generations_exceeded
        ):
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    pause = not pause
                elif event.type == MOUSEBUTTONUP:
                    col, row = event.pos
                    col = col // self.cell_size
                    row = row // self.cell_size
                    self.life.curr_generation[row][col] = (
                        0
                        if self.life.curr_generation[row][col]
                        else 1
                    )
                    self.draw_grid()
                    pygame.display.flip()

            if pause:
                self.draw_lines()
                self.draw_grid()
                pygame.display.flip()
                continue

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_lines()
            self.draw_grid()
            self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


def parse_args():
    parser = argparse.ArgumentParser(description="""Игра жизнь""")

    parser.add_argument("--rows",
                        "-r",
                        type=int,
                        dest="r",
                        required=True,
                        help="Количество строк")
    parser.add_argument("--cols",
                        "-c",
                        type=int,
                        dest="c",
                        required=True,
                        help="Количество столбцов")
    parser.add_argument("--max-iterations",
                        "-it",
                        type=int,
                        dest="it",
                        required=False,
                        default=1000,
                        help="Количество итераций")
    parser.add_argument("--cell-size",
                        "-cs",
                        type=int,
                        dest="cs",
                        required=False,
                        default=10,
                        help="Размер ячейки")

    parser.add_argument("--input-filename",
                        "-in",
                        type=str,
                        dest="in",
                        required=False,
                        help="Путь к файлу с входными данными")

    return parser.parse_args()


if __name__ == '__main__':
    args = vars(parse_args())
    if args.get('in'):
        life = GameOfLife.from_file(pathlib.Path(args['in']))
    else:
        life = GameOfLife((args['r'], args['c']), True, args['it'])
    ui = GUI(life, cell_size=args['cs'])
    ui.run()

