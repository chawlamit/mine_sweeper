from environment import Environment
from agents.baseline_agent import BaselineAgent
from agents.final_agent import Agent
from agents.probabilistic_agent import ProbabilisticAgent
env = Environment(5, 5)
# env._board = [[0, 0, 0, -1, 0],
# [-1, 0, 0, 0, 0],
# [-1, 0, 0, 0, 0],
# [0, 0, -1, 0, 0],
# [0, 0, -1, 0, 0]]
env.show()

# agent = BaselineAgent(env)
# agent.run()
# print(agent.calc_score())

agent = Agent(env)
agent.run()
print(agent.calc_score())

agent = ProbabilisticAgent(env)
agent.run()
print(agent.calc_score())
