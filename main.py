from environment import Environment
from agents.baseline_agent import BaselineAgent

env = Environment(10, 10)
agent = BaselineAgent(env)

agent.run()
print(agent.calc_score())
