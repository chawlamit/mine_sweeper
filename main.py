from environment import Environment
from agents.baseline_agent import BaselineAgent
from agents.final_agent import Agent
from agents.probabilistic_agent import ProbabilisticAgent


env = Environment(10, 40)
env._board = [[0, 0, -1, 0, 0, -1, -1, 0, 0, 0],
[-1, -1, -1, 0, 0, -1, -1, -1, 0, -1],
[0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
[0, -1, 0, -1, -1, 0, 0, -1, 0, -1],
[0, -1, -1, -1, 0, 0, 0, 0, -1, -1],
[0, 0, 0, -1, -1, 0, 0, 0, 0, 0],
[0, 0, -1, 0, 0, -1, -1, -1, 0, 0],
[-1, -1, -1, -1, -1, 0, 0, -1, 0, 0],
[0, 0, -1, -1, 0, 0, 0, -1, -1, 0],
[0, 0, 0, 0, -1, 0, -1, 0, -1, 0]]
env.show()

scores = []

agent = BaselineAgent(env)
agent.run()
scores.append(agent.calc_score())

agent = Agent(env)
agent.run()
scores.append(agent.calc_score())

agent = ProbabilisticAgent(env)
agent.run()
scores.append(agent.calc_score())

print(scores)
