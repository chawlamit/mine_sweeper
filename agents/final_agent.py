from collections import OrderedDict
import numpy as np
from environment import Environment
from .baseline_agent import BaselineAgent
from utils import partial_equations, debug
from time import sleep


class Agent(BaselineAgent):

    def make_eqns(self):

        var_set = set()
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
                # debug("var_set", var_set)
        return var_set, eqns, b

    def reduce_eqns(self, var_set, eqns, b):
        a = []
        n_vars = len(var_set)
        debug(n_vars)

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
                        debug(f'Mine Flagged at {var_list[j]}')

    def explore_fringe(self):
        while self.fringe:
            row, col = self.fringe.pop(0)
            debug("quried", row, col)
            clue = self.query(row, col)
            self.kb[(row, col)] = clue
            n, h, m, s = self.infer(row, col)
            # Open all the adjoining cells with 0 values
            if clue == self.env.MINE:
                self.mines_burst += 1
                continue
            elif clue == 0:
                for el in n:
                    if el not in self.kb:
                        self.kb[el] = None
                        self.fringe.append(el)

    def run(self):
        clue = row = col = None
        debug("Entered run")
        # can also use the same exit condition as the baseline agent
        while self.cells_turned + self.mines_flagged < self.env.dim ** 2:
            # random starting point
            if not self.fringe:
                row, col = self.pick_random()
                debug('Random Pick', row, col)
                self.fringe.append((row, col))

            self.explore_fringe()
            # Going beyond local inference with eqn solving
            var_set, eqns, b = self.make_eqns()
            self.reduce_eqns(var_set, eqns, b)

        debug("done")
        debug("cells_turned", self.cells_turned)
        debug("mines_flagged", self.mines_flagged)
