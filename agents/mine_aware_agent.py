from agents.probabilistic_agent import ProbabilisticAgent
from collections import OrderedDict
from environment import Environment
from utils import partial_equations
import numpy as np

class MineAwareAgent(ProbabilisticAgent):
    def __init__(self, env: Environment):
        super().__init__(env)
        self.all_cells = set()
        for i in range(self.env.dim):
            for j in range(self.env.dim):
                self.all_cells.add((i, j))

    def make_eqns(self):

        var_set = set()
        a = []
        b = []
        eqns = OrderedDict()

        for row, col in self.kb:
            clue = self.kb[(row, col)]
            if clue == 0 or clue == self.env.MINE or clue == self.FLAG:
                continue
            n, h, m, s = self.infer(row, col)
            if len(h) > 0:
                eqns[(row, col)] = h
                # already found mines need to subtracted from the clue
                b.append(clue - len(m))
                var_set = var_set.union(h)
                # print("var_set", var_set)
        # add an eqn with total no. of mines
        remaining_cells = self.all_cells.difference(set(self.kb.keys()))
        eqns[(-1, -1)] = remaining_cells
        b.append(self.env.n_mines - self.mines_burst - self.mines_flagged)
        var_set.union(remaining_cells)

        n_vars = len(var_set)
        for _, hidden_set in eqns.items():
            eq = [0] * n_vars
            for i, var in enumerate(var_set):
                if var in hidden_set:
                    eq[i] = 1
            a.append(eq)
        a, b = np.array(a), np.array(b)
        partial_equations(a, b)
        var_list = list(var_set)
        for i, key in enumerate(eqns):
            if b[i] == 0:
                for j in np.where(a[i] == 1)[0]:
                    if var_list[j] not in self.kb:
                        self.kb[var_list[j]] = None
                        self.fringe.append(var_list[j])
            elif sum(a[i]) == b[i]:
                for j in np.where(a[i] == 1)[0]:
                    if var_list[j] not in self.kb:
                        self.flag(*var_list[j])
                        print(f'Mine Flagged at {var_list[j]}')

