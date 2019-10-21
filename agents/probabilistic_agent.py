from .final_agent import Agent
from collections import OrderedDict
import numpy as np
from utils import partial_equations


class ProbabilisticAgent(Agent):

    def probabilistic_pick(self, cells_turned: int, mines_flagged: int):
        """ Use the Remaining mines information while opening a random point to search """
        remaining_cells = self.env.dim ** 2 - cells_turned - mines_flagged
        rand_prob = (self.env.n_mines - mines_flagged) / remaining_cells
        dict_hidden_prob = {}
        # plt.pause(0.

        for (row, col) in self.kb:
            clue = self.kb[(row, col)]
            if clue == self.env.MINE or clue == self.FLAG:
                continue
            n, h, m, s = self.infer(row, col)
            if len(h) == 0:
                continue
            prob_hidden = (clue - len(m)) / len(h)
            for (row_, col_) in h:
                if (row_, col_) in dict_hidden_prob:
                    dict_hidden_prob[(row_, col_)] += prob_hidden
                else:
                    dict_hidden_prob[(row_, col_)] = prob_hidden
        list_sorted_probabilities = sorted(dict_hidden_prob.items(), key=lambda l: l[1])
        # print(list_sorted_probabilities)
        # print("rand_prob", rand_prob)
        if list_sorted_probabilities:
            if list_sorted_probabilities[0][1] < rand_prob:
                print("Probabilistic pick ", list_sorted_probabilities[0][0])
                return list_sorted_probabilities[0][0]

        row, col = self.pick_random()

        while (row, col) in dict_hidden_prob and len(dict_hidden_prob) < remaining_cells:
            row, col = self.pick_random()

        # print("random pick", row, col)
        return row, col

    def run(self):
        clue = row = col = None
        # can also use the same exit condition as the baseline agent
        while self.cells_turned + self.mines_flagged < self.env.dim ** 2:
            # random starting point
            if not self.fringe:
                row, col = self.probabilistic_pick(self.cells_turned, self.mines_flagged)
                self.fringe.append((row, col))

            self.explore_fringe()
            self.make_eqns()
