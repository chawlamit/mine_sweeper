from agents.csp_agent import CSPAgent
from collections import OrderedDict
from environment import Environment
from utils import set_reduction, debug
from functools import reduce
import numpy as np

def mean(*args):
    return reduce(lambda x, y: x + y, args) / len(args)

class MineAwareAgent(CSPAgent):
    """
    A version of agent with information about the total number of mines present in board. It uses this information in 2 ways:
    1. It augments the Constraint satisfaction with one more equation. i.e.
        All the remaining hidden cells will add up to remaining number of mines on board
    2. It uses the following probabilistic pick function to use probabilities to pick the next cell to
        open when in a giffy
    """

    def __init__(self, env: Environment, visualize=False, debug=False):
        super().__init__(env, visualize=visualize, debug=debug)
        # set of all the cells(row, col) on board
        self.all_cells = set()
        for i in range(self.env.dim):
            for j in range(self.env.dim):
                self.all_cells.add((i, j))

    def make_eqns(self):
        var_set, eqns, b = super().make_eqns()
        # add an eqn with total no. of mines remaing, adding up to the total no. of remaining cells
        remaining_cells = self.all_cells.difference(set(self.kb.keys()))
        eqns[(-1, -1)] = remaining_cells
        b.append(self.env.n_mines - self.mines_burst - self.mines_flagged)
        var_set = var_set.union(remaining_cells)
        return var_set, eqns, b

    def probabilistic_pick(self, cells_turned: int, mines_flagged: int, prob_calc=mean):
        """
        Use the Total number of mines remaining on board to calculte probability of a randomly picked cell having a mine,
        compate it with average probabilites calculated from the clue collected so far. Pick a cell with least
        probability of having a mine.
        Internally uses random pick if the probability of random cell away from boundary cells is lesser
        :return: row, col
        """
        remaining_cells = self.env.dim ** 2 - cells_turned - mines_flagged
        rand_prob = (self.env.n_mines - mines_flagged) / remaining_cells
        dict_hidden_prob = {}

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
                    # calculate avg probability
                    dict_hidden_prob[(row_, col_)] = prob_calc(prob_hidden, dict_hidden_prob[(row_, col_)])
                else:
                    dict_hidden_prob[(row_, col_)] = prob_hidden
        list_sorted_probabilities = sorted(dict_hidden_prob.items(), key=lambda l: l[1])
        # debug(list_sorted_probabilities)
        # debug("rand_prob", rand_prob)
        if list_sorted_probabilities:
            if list_sorted_probabilities[0][1] < rand_prob:
                debug("Probabilistic pick ", list_sorted_probabilities[0][0])
                return list_sorted_probabilities[0][0]

        row, col = self.pick_random()

        # pick a cell randomly, away from the boundary of clues
        while (row, col) in dict_hidden_prob and len(dict_hidden_prob) < remaining_cells:
            row, col = self.pick_random()

        # debug("random pick", row, col)
        return row, col

    def run(self, prob_calc=mean):
        clue = row = col = None
        # can also use the same exit condition as the baseline agent
        while self.cells_turned + self.mines_flagged < self.env.dim ** 2:
            # random starting point
            if not self.fringe:
                row, col = self.probabilistic_pick(self.cells_turned, self.mines_flagged, prob_calc)
                self.fringe.append((row, col))

            self.explore_fringe()
            var_set, eqns, b = self.make_eqns()
            set_reduction(eqns, b)
            self.deduce(eqns, b)
