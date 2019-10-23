from collections import OrderedDict
import numpy as np
from environment import Environment
from .csp_Agent import CSPAgent
from .final_agent import Agent
from utils import debug,set_reduction
from time import sleep

class ProbabilityAgent(Agent) :


    def query(self,row,col):
        prob = np.random.binomial(1,0.5,1)
        if prob :
            return super().query(row,col)
        else :
            return None


    def make_eqns(self):

        var_set = set()
        b = []
        eqns = OrderedDict()

        for row, col in self.kb:
            clue = self.kb[(row, col)]
            # print("row {},col {}, clue {}".format(row,col,clue))
            if clue == 0 or clue == self.env.MINE or clue == self.FLAG or clue is None:
                continue
            n, h, m, s = self.infer(row, col)
            if len(h) > 0:
                eqns[(row, col)] = h
                # already found mines need to subtracted from the clue
                b.append(clue - len(m))
                var_set = var_set.union(h)
                # debug("var_set", var_set)
        return var_set, eqns, b


    def explore_fringe(self):
        while self.fringe:
            row, col = self.fringe.pop(0)
            debug("quried", row, col)
            clue = self.query(row, col)
            if clue is not None :
                debug("Added")
                self.kb[(row, col)] = clue
                n, h, m, s = self.infer(row, col)
                # Open all the adjoining cells with 0 values
                if clue == self.env.MINE:
                    self.mines_burst += 1
                    continue
                elif clue == 0:
                    for el in n:
                        if el not in self.kb:
                            # self.kb[el] = None
                            self.fringe.append(el)
            else :
                debug("skipped")

    def reduce_eqns(self, var_set, eqns, b):
        set_reduction(eqns, b)

        for i, key in enumerate(eqns):
            if b[i] == 0:
                for cell in eqns[key]:
                    if cell not in self.kb:
                        # self.kb[cell] = None
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
            var_set, eqns, b = self.make_eqns()
            self.reduce_eqns(var_set, eqns, b)

        debug("done")
        debug("cells_turned", self.cells_turned)
        debug("mines_flagged", self.mines_flagged)
