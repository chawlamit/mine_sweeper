from environment import Environment
from .base_agent import BaseAgent

class BaselineAgent(BaseAgent):
    def __init__(self, env: Environment):
        super().__init__(env)

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
        while len(self.kb) < self.env.dim * self.env.dim:
            # print('Fringe: ', fringe)

            if not fringe:
                row, col = self.pick_random()
                fringe.append((row, col))

            row, col = fringe.pop(0)

            clue = self.query(row, col)
            self.kb[(row, col)] = clue

            neighbors, hidden, mines, safe = self.infer(row, col)

            # TODO - move the deduction logic into deduce function to be reused by other agents
            # deduction: deduce new knowledge from the inferred knowledge
            if clue - len(mines) == len(hidden):
                for el in hidden:
                    self.flag(*el)

            if len(neighbors) - clue - len(safe) == len(hidden):
                for el in hidden:
                    self.kb[el] = self.env.query(el[0], el[1])
                    fringe.append(el)

