import copy
import random
import pathlib
from typing import List, Tuple, Optional


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[List[int]]


class GameOfLife:

    def __init__(self,
                 size: Tuple[int, int],
                 randomize: bool = True,
                 max_generations: Optional[int] = float("inf")
                 ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

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
                for _ in range(self.cols)
            ]
            for _ in range(self.rows)
        ]

        return grid

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
            self.curr_generation[row][col]
            for row, col in [
                top_left, top, top_right,
                left, right, bottom_left,
                bottom, bottom_right
            ]
            if
            (self.rows - 1 >= row >= 0) and
            (self.cols - 1 >= col >= 0)
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
        grid = copy.deepcopy(self.curr_generation)

        for row in range(self.rows):
            for col in range(self.cols):
                neighbours = self.get_neighbours((row, col))
                alive = neighbours.count(1)
                current = self.curr_generation[row][col]
                if current == 1:
                    if alive not in [2, 3]:
                        grid[row][col] = 0
                else:
                    if alive == 3:
                        grid[row][col] = 1

        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, 'r') as f:
            arr = []
            for line in f:
                arr.append(
                    [
                        int(x)
                        for x
                        in line.split('\n')[0]
                    ]
                )
        print(f'Loaded from file: {filename}')
        rows = len(arr)
        cols = len(arr[0])
        game_of_life = GameOfLife(size=(rows, cols))
        game_of_life.curr_generation = arr
        return game_of_life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'wt') as f:
            for line in self.curr_generation:
                f.write(''.join([str(x) for x in line]))
                f.write('\n')
        print(f'Saved into file: {filename}')


if __name__ == '__main__':
    print('TEST RANDOM GAME\n')
    random.seed(1234)
    life = GameOfLife((5, 5))

    print('start position:', life.curr_generation)
    life.step()
    print('previous step:', life.prev_generation)
    print('current step:', life.curr_generation)

    print('TEST CONDITIONS\n')

    random.seed(4321)
    life = GameOfLife((5, 5), max_generations=50)

    while life.is_changing and not life.is_max_generations_exceeded:
        life.step()
    print('amount of iterations:', life.generations)

    print('TEST FROM FILES')
    life = GameOfLife.from_file(pathlib.Path('../data/input.txt'))

    for _ in range(4):
        life.step()

    life.save(pathlib.Path('../data/output.txt'))

