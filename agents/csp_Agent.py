from agents.baseline_agent import BaselineAgent
from agents.final_agent import Agent
from utils import debug, set_reduction


class CSPAgent(Agent):

    def reduce_eqns(self, var_set, eqns, b):
        set_reduction(eqns, b)

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