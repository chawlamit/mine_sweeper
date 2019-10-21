from .final_agent import Agent
from collections import OrderedDict
import numpy as np
from utils import partial_equations

class ProbabilisticAgent(Agent) :
    def run(self) :
        cells_turned = 0
        mines_flagged = 0
        clue = row = col = None
        fringe = []
        # can also use the same exit condition as the baseline agent
        while cells_turned + mines_flagged < self.env.dim ** 2:
            # random starting point
            if not fringe:
                row, col = self.probabilistic_pick(cells_turned,mines_flagged)

                # print('Pro')
                fringe.append((row, col))

            while fringe:
                row, col = fringe.pop(0)
                # print(row, cosl)
                clue = self.query(row, col)
                cells_turned += 1
                n, h, m, s = self.infer(row, col)
                self.kb[(row, col)] = clue
                # Open all the adjoining cells with 0 values
                if clue == self.env.MINE:
                    self.kb[(row, col)] = clue
                    continue
                elif clue == 0:
                    for el in n:
                        if el not in self.kb:
                            self.kb[el] = None
                            fringe.append(el)
                # baseline inference logic
                else:
                    if clue - len(m) == len(h):
                        for el in h:
                            self.kb[el] = self.FLAG
                            mines_flagged += 1
                            print(f'Mine Flagged at {el}')

                    if len(n) - clue - len(s) == len(h):
                        for el in h:
                            self.kb[el] = None
                            fringe.append(el)
            # Going beyond local inference with
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
                    # eqns[len(h)].append({'eq': h, 'val': clue})
                    # already found mines need to subtracted from the clue
                    b.append(clue - len(m))
                    var_set = var_set.union(h)
                    # print("var_set", var_set)

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
                        self.kb[var_list[j]] = None
                        fringe.append(var_list[j])
                elif sum(a[i]) == b[i]:
                    for j in np.where(a[i] == 1)[0]:
                        self.kb[var_list[j]] = self.FLAG
                        mines_flagged += 1
                        print(f'Mine Flagged at {var_list[j]}')