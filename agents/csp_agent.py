from agents.baseline_agent import BaselineAgent
from utils import debug, set_reduction
from collections import OrderedDict


class CSPAgent(BaselineAgent):
        
    def make_eqns(self):
        var_set = set()
        b = []
        eqns = OrderedDict()

        for row, col in self.kb:
            clue = self.kb[(row, col)]
            if not clue or clue == 0 or clue == self.env.MINE or clue == self.FLAG:
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
            self.kb[(row, col)] = clue
            if clue is None:
                continue
            n, h, m, s = self.infer(row, col)
            # Open all the adjoining cells with 0 values
            if clue == self.env.MINE:
                self.mines_burst += 1
                continue
            elif clue == 0:
                debug("clue {} n {}".format(clue,n))
                for el in n:
                    if el not in self.kb:
                        self.kb[el] = None
                        self.fringe.append(el)
    
    def deduce(self, eqns, b):
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
            var_set, eqns, b = self.make_eqns()
            set_reduction(eqns, b)
            self.deduce(eqns, b)

        debug("done")
        debug("cells_turned", self.cells_turned)
        debug("mines_flagged", self.mines_flagged)