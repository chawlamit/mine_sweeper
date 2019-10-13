from .base_agent import BaseAgent
from .baseline_agent import BaselineAgent
from environment import Environment
from collections import OrderedDict
from gauss_elim import gauss_elim
import numpy as np
from utils import partial_equations


class Agent(BaselineAgent):
    @classmethod
    def covert_set_to_dict(cls, se):
        d = {}
        for el in set:
            d[el] = None
        return d

    def __init__(self, env: Environment):
        super().__init__(env)
        self.kb['safe'] = set()
        self.kb['mine'] = set()
        self.kb['clues'] = {}

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
                if (row + i, col + j) in self.kb['clues']:
                    clue = self.kb['clues'][(row + i, col + j)]
                    if clue == -1:
                        mines.add((row + i, col + j))
                    else:
                        safe.add((row + i, col + j))
        hidden = neighbors - mines - safe

        return neighbors, hidden, mines, safe

    def run(self):
        cells_turned = 0
        mines_flagged = 0

        # Phase 1, Let's start by using the baseLine inference to open as many cells as we can
        # finding a 0 starting point for the agent
        clue = row = col = None

        fringe = []
        # while fringe:

        while cells_turned + mines_flagged <= self.env.dim ** 2:
        # for i in range(10):
            # random starting point
            if not fringe:
                row, col = self.pick_random()

                # keep picking cells until you find an unturned cell
                while (row, col) in self.kb['clues']:
                    row, col = self.pick_random()

                fringe.append((row, col))

            while fringe:
                row, col = fringe.pop(0)
                print(row, col)
                clue = self.query(row, col)
                cells_turned += 1
                n, h, m, s = self.infer(row, col)
                self.kb['clues'][(row, col)] = clue
                if clue == 0:
                    for el in n:
                        if el not in self.kb['clues']:
                            self.kb['clues'][el] = None
                            fringe.append(el)
            var_set = set()
            a = []
            b = []
            eqns = OrderedDict()

            for row, col in self.kb['clues']:
                clue = self.kb['clues'][(row, col)]
                if clue == 0:
                    continue
                n, h, m, s = self.infer(row, col)
                # TODO - use baseline thing first, before going to eqns
                if len(h) > 0:
                    eqns[(row, col)] = h
                    # eqns[len(h)].append({'eq': h, 'val': clue})
                    b.append(clue)
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
                if sum(a[i]) == b[i]:
                    if b[i] == 0:
                        for j in np.where(a[i] == 1)[0]:
                            fringe.append(var_list[j])
                    else:
                        for j in np.where(a[i] == 1)[0]:

                            print('var_list', var_list[j])
                            self.kb['clues'][var_list[j]] = self.FLAG
                            mines_flagged += 1


    def calc_score(self):
        correctly_flagged_mines = 0
        incorrectly_flagged_mines = 0
        undiscovered_mines = 0
        for i, j in self.kb['clues']:
            if self.kb['clues'][(i, j)] == self.FLAG:
                if self.env.has_mine(i, j):
                    correctly_flagged_mines += 1
                else:
                    incorrectly_flagged_mines += 1
            elif self.kb['clues'][(i, j)] == self.env.MINE:
                undiscovered_mines += 1
        score = (correctly_flagged_mines - incorrectly_flagged_mines) / self.env.n_mines
        print(correctly_flagged_mines, incorrectly_flagged_mines)
        return score





    #
    # def is_cell_turned(self, eqns, n, i):
    #     to_remove = []
    #     to_add = []
    #
    #     new_eq = set()
    #     for var in eqns[n][i]['eq']:
    #
    #         if var in self.kb['clues']:
    #             clue = self.kb['clues'][var]
    #             if clue == self.FLAG:
    #                 eqns[n][i]['val'] - 1
    #         else:
    #             new_eq.add(var)
    #
    #     if new_eq == eqns[n][i]['eq']:
    #         return None
    #
    #     to_remove.append((n, i))
    #     if new_eq:
    #         to_add.append((new_eq, eqns[n][i]['val']))
    #     return to_remove, to_add
    #
    # def rule1(self, eqns, n, i):
    #     # 1: if A + B + C = 3 =>  A, B, C will be mines
    #     to_remove = []
    #     to_add = []
    #     eq = eqns[n][i]['eq']
    #     val = eqns[n][i]['val']
    #     if len(eq) == val:
    #         for row, col in eq:
    #             self.kb['clues'][row, col] = self.FLAG
    #             to_remove.append((n, i))
    #     return to_remove, to_add
    #
    # def rule2(self, eqns, n, i):
    #     to_add = []
    #     to_remove = []
    #     # 2: A + B + C = 2, B + C = 1 => A = 1
    #     eq = eqns[n][i]['eq']
    #     val = eqns[n][i]['val']
    #     for s in range(1, n):
    #         for j, sub_eq in enumerate(eqns[s]):
    #             if eq.intersection(sub_eq) == sub_eq:
    #                 result = eq.difference(sub_eq)
    #                 if len(result) == 1:
    #                     if val - eqns[s][j] == 1:
    #                         self.kb['clues'][result.pop()] = self.FLAG
    #                     else:
    #                         self.fringe.append(self.kb['clues'][result.pop()])
    #                 else:
    #                     to_add.append((result, val - eqns[n-1][j]))
    #                     to_remove.append((n, i))
    #     return to_remove, to_add

    # def solve_eqns(self, eqns):
    #     mines = 0
    #     to_add = []
    #     to_remove = []
    #     for n in eqns:
    #         if n <= 2:
    #             continue
    #         for i, eq in enumerate(eqns[n]):
    #             tr, ta = self.is_cell_turned(eqns, n, i)
    #             to_remove += tr
    #







