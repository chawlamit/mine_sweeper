from environment import Environment
from agents.baseline_agent import BaselineAgent
from agents.final_agent import Agent
from agents.probabilistic_agent import ProbabilisticAgent
from agents.mine_aware_agent import MineAwareAgent
from agents.csp_Agent import CSPAgent

import time

env = Environment(30, 180)
env.show()

scores = []

# agent = BaselineAgent(env)
# agent.run()
# scores.append(agent.calc_score())
#
agent = CSPAgent(env, visualize=False, debug=False)
st = time.time()
agent.run()
print('time: ', agent.__class__.__name__, time.time() - st)
scores.append(agent.calc_score())
#
agent = MineAwareAgent(env, visualize=False)
st = time.time()
agent.run()
print('time: ', agent.__class__.__name__, time.time() - st)
scores.append(agent.calc_score())
#
agent = Agent(env, visualize=False, debug=False)
st = time.time()
agent.run()
print('time: ', agent.__class__.__name__, time.time() - st)
scores.append(agent.calc_score())

print(scores)
