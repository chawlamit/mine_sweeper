from environment import Environment
from agents.baseline_agent import BaselineAgent
from agents.mine_aware_agent import MineAwareAgent
from agents.csp_agent import CSPAgent
from agents.probability_agent import ProbabilityAgent
import time

env = Environment(10, 20)

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
# #
agent = MineAwareAgent(env, visualize=False)
st = time.time()
agent.run()
print('time: ', agent.__class__.__name__, time.time() - st)
scores.append(agent.calc_score())
# #
agent = ProbabilityAgent(env,visualize=False, debug=False)
agent.P = 0.7
st = time.time()
agent.run()
print('time: ', agent.__class__.__name__, time.time() - st) 
scores.append(agent.calc_score())

print(scores)
