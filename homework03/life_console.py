import curses
import argparse
import time
from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    @staticmethod
    def draw_borders(screen) -> None:
        """ Отобразить рамку """
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток """
        for i in range(1, self.life.rows):
            for j in range(1, self.life.cols):
                screen.addstr(
                    j, i, 'o' if self.life.curr_generation[i][j] else '-'
                )

    def run(self,
            use_key: bool = False,
            timeout: int = 0.1) -> None:
        screen = curses.initscr()

        while life.is_changing and not life.is_max_generations_exceeded:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(timeout)
            self.life.step()
            if use_key:
                screen.getkey()
        curses.endwin()


def parse_args():
    parser = argparse.ArgumentParser(description="""Игра жизнь""")

    parser.add_argument("--width",
                        "-w",
                        type=int,
                        dest="w",
                        required=True,
                        help="Ширина")
    parser.add_argument("--height",
                        "-hei",
                        type=int,
                        dest="hei",
                        required=True,
                        help="Высота")
    parser.add_argument("--max-iterations",
                        "-it",
                        type=int,
                        dest="it",
                        required=False,
                        default=100,
                        help="Количество итераций")

    return parser.parse_args()


if __name__ == '__main__':
    args = vars(parse_args())
    life = GameOfLife((args['w'], args['hei']), max_generations=args['it'])
    ui = Console(life)
    ui.run()
