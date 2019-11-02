from agents.baseline_agent import BaselineAgent
from utils import debug, set_reduction
from collections import OrderedDict


class CSPAgent(BaselineAgent):
    """

    """

    def make_eqns(self):
        """
        Generate a dictionary of variable sets represeting equations for hidden cells
        e.g. A + B + C = 2 is represented as eqns[(row, col)] = set(A,B,C) one of the items in eqns dictionary
            and the total number of mines is stored in mines vector, mines[2]
        :return: equation_variables: set, eqns: dictionary, mines: [int]
        """
        # A Union of all the boundary cells(row, col) which are being represented in the equations
        eq_vars = set()
        # dictionary of equations
        eqns = OrderedDict()
        # vector containing right side of the equation
        mines = []

        # Make the equations
        for row, col in self.kb:
            clue = self.kb[(row, col)]
            if not clue or clue == 0 or clue == self.env.MINE or clue == self.FLAG:
                continue
            n, h, m, s = self.infer(row, col)
            if len(h) > 0:
                eqns[(row, col)] = h
                # already found mines need to subtracted from the clue
                mines.append(clue - len(m))
                eq_vars = eq_vars.union(h)
                # debug("equation_variables", equation_variables)
        return eq_vars, eqns, mines

    def explore_fringe(self):
        """
        Explore and query the state of all the safe cells added onto the fringe
        :return:
        """
        while self.fringe:
            row, col = self.fringe.pop(0)
            debug("queried", row, col)
            # query the environment for the clue
            clue = self.query(row, col)
            # add the clue to the knowledge base
            self.kb[(row, col)] = clue
            # to be used for the 4th problem, where the clue is returned with some probability
            if clue is None:
                continue
            neighbors, hidden, mines, safe = self.infer(row, col)
            # Open all the adjoining cells with 0 values
            if clue == self.env.MINE:
                self.mines_burst += 1
                continue
            elif clue == 0:
                debug("clue {} neighbors {}".format(clue,neighbors))
                for el in neighbors:
                    if el not in self.kb:
                        self.kb[el] = None
                        # add safe cells to the fringe
                        self.fringe.append(el)
    
    def deduce(self, eqns, b):
        """
        Post the set reduction on eqns produced by make_eqns func, e.g. A+B+C=2, B+C=1 > A=1, B+C=1
        mark the cells as safe or flag
        :param eqns:
        :param b: mine_totals
        """
        for i, key in enumerate(eqns):
            if b[i] == 0:
                for cell in eqns[key]:
                    if cell not in self.kb:
                        self.kb[cell] = None
                        self.fringe.append(cell)
            elif len(eqns[key]) == b[i]:
                for cell in eqns[key]:
                    if cell not in self.kb:
                        self.flag(*cell)
                        debug(f'Mine Flagged at {cell}')

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
            eq_vars, eqns, mines_clues = self.make_eqns()
            set_reduction(eqns, mines_clues)
            self.deduce(eqns, mines_clues)

        debug("done")
        debug("cells_turned", self.cells_turned)
        debug("mines_flagged", self.mines_flagged)