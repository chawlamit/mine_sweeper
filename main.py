from environment import Environment
from agents.baselineAgent import BaselineAgent

if __name__ == '__main__':
    env = Environment(10, 10)
    agent = BaselineAgent(env)

    agent.run()
    print(agent.calc_score())
