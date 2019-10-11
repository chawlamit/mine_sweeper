from .baseAgent import BaseAgent


class BaselineAgent(BaseAgent):

    def infer(self, row, col):
        safe = set()
        mines = set()
        neighbors = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                # print(row+i,col+j)
                if i == 0 and j == 0:
                    continue
                if self.env.is_valid(row + i, col + j):
                    neighbors.add((row + i, col + j))
                if (row + i, col + j) in self.kb:
                    clue = self.kb[(row + i, col + j)]
                    if clue == -1:
                        mines.add((row + i, col + j))
                    else:
                        safe.add((row + i, col + j))
        hidden = neighbors - mines - safe

        return neighbors, hidden, mines, safe

    def run(self):
        fringe = []
        while len(self.kb) < self.env.dim * self.env.dim:
            # print('Fringe: ', fringe)
            if fringe:
                row, col = fringe.pop(0)
            else:
                row, col = self.pick_random()

            self.kb[(row, col)] = self.env.query(row, col)
            clue = self.kb[(row, col)]

            neighbors, hidden, mines, safe = self.infer(row, col)
            if clue - len(mines) == len(hidden):
                for el in hidden:
                    self.kb[el] = -2

            if len(neighbors) - clue - len(safe) == len(hidden):
                for el in hidden:
                    self.kb[el] = self.env.query(el[0], el[1])
                    fringe.append(el)
            # print(kb)
        print(self.kb)
