from environment import Environment
from .base_agent import BaseAgent


class BaselineAgent(BaseAgent):

    def infer(self, row, col):

        safe = set()
        mines = set()
        neighbors = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.env.is_valid(row + i, col + j):
                    neighbors.add((row + i, col + j))
                if (row + i, col + j) in self.kb:
                    clue = self.kb[(row + i, col + j)]
                    if clue == self.env.MINE or clue == self.FLAG:
                        mines.add((row + i, col + j))
                    else:
                        safe.add((row + i, col + j))
        hidden = neighbors - mines - safe

        return neighbors, hidden, mines, safe

    def deduce(self, row, col):
        pass

    def run(self):
        fringe = []
        while self.cells_turned + self.mines_flagged < self.env.dim * self.env.dim:

            if not fringe:
                row, col = self.pick_random()
                fringe.append((row, col))

            row, col = fringe.pop(0)

            clue = self.query(row, col)
            self.kb[(row, col)] = clue

            if clue == self.env.MINE:
                self.mines_burst += 1
                continue

            neighbors, hidden, mines, safe = self.infer(row, col)

            # deduction: deduce new knowledge from the inferred information
            if clue - len(mines) == len(hidden):
                for el in hidden:
                    self.flag(*el)

            if len(neighbors) - clue - len(safe) == len(hidden):
                for el in hidden:
                    self.kb[el] = self.env.query(el[0], el[1])
                    fringe.append(el)
