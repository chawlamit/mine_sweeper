import random


class Environment:
    """
    This class contains the specifications of the minesweeper environment
    """
    MINE = -1

    def __init__(self, dim: int, n_mines: int):
        """
        :param dim: This function will generate a dim X dim array(environment) containing mines
        :param n_mines: Number of mines to be placed in this map
        """

        self.dim = dim
        self.n_mines = n_mines
        self._board = [[0] * dim for _ in range(dim)]
        self.hidden = True
        self.flagged = False

        mine_cells = random.sample(range(dim * dim), n_mines)

        for cell in mine_cells:
            self._board[cell // dim][cell % dim] = self.MINE

    def show(self):
        for i in range(self.dim):
            print(self._board[i])
        print()

    def query(self, row: int, col: int):
        if self.has_mine(row, col):
            return self.MINE
        else:
            return self.neighboring_mine_count(row, col)

    def get_valid_neighbors(self, row, col):
        nbs = []
        for i in range(-1 + row, 2 + row):
            for j in range(-1 + col, 2 + col):
                if i == row and j == col:
                    continue
                if self.is_valid(i, j):
                    nbs.append((i, j))
        if nbs:
            return nbs
        return None

    def neighboring_mine_count(self, row, col):
        mine_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_valid(row + i, col + j) and self.has_mine(row + i, col + j):
                    mine_count += 1
        return mine_count

    # helper functions
    def is_valid(self, row, col):
        if 0 <= row < self.dim and 0 <= col < self.dim:
            return True
        else:
            return False

    def has_mine(self, row, col):
        if self._board[row][col] < 0:
            return True
        return False

    def no_of_hidden(self, row, col):
        result = 0
        for p in range(-1, 2):
            for q in range(-1, 2):
                cur_cell = self.query(row + p, col + q)
                if not cur_cell.is_valid and cur_cell.hidden and not cur_cell.flagged:
                    result += 1
        return result

    def no_of_flags(self, row, col):
        result = 0
        for p in range(-1, 2):
            for q in range(-1, 2):
                if p == 0 and q == 0:
                    continue
                cur_cell = self.query(row + p, col + q)
                if not cur_cell.is_valid and cur_cell.isFlag:
                    result += 1
        return result

if __name__ == '__main__':
    env = Environment(10, 10)
    env.show()