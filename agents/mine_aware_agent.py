from agents.probabilistic_agent import ProbabilisticAgent
from collections import OrderedDict
from environment import Environment
from utils import partial_equations
import numpy as np


class MineAwareAgent(ProbabilisticAgent):

    def __init__(self, env: Environment, visualize=False, debug=False):
        super().__init__(env, visualize=visualize, debug=debug)
        self.all_cells = set()
        for i in range(self.env.dim):
            for j in range(self.env.dim):
                self.all_cells.add((i, j))

    def make_eqns(self):
        var_set, eqns, b = super().make_eqns()
        # add an eqn with total no. of mines add total no. of remaining cells
        remaining_cells = self.all_cells.difference(set(self.kb.keys()))
        eqns[(-1, -1)] = remaining_cells
        b.append(self.env.n_mines - self.mines_burst - self.mines_flagged)
        var_set = var_set.union(remaining_cells)
        return var_set, eqns, b
