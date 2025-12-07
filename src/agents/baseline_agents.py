import numpy as np

class BaseAgent:

    def __init__(self, action_space):
        self.action_space = action_space
        self.name = "BaseAgent"

    def choose_action(self, observation):
        raise NotImplementedError("Sub must implement")

    def reset(self):
        pass


class RandomAgent(BaseAgent):
    def __init__(self,action_space,seed=None):
        super().__init__(action_space)
        self.name="RandomAgent"

        if seed is not None:
            np.random.seed(seed)

    def choose_action(self, observation):
        return self.action_space.sample()

class AlwaysHoldAgent(BaseAgent):
    def __init__(self, action_space):
        super().__init__(action_space)
        self.name="AlwaysHoldAgent"

    def choose_action(self, observation):
        return 0 #hold

class BuyAndHoldAgent(BaseAgent):
    def __init__(self, action_space):
        super().__init__(action_space)
        self.name="BuyAndHoldAgent"
        self.has_bought = False
    
    def choose_action(self, observation):
        if not self.has_bought:
            self.has_bought = True
            return 1
        else:
            return 0

    def reset(self):
        self.has_bought=False

class SimpleMovingAverageAgent(BaseAgent):
    def __init__(self, action_space, history_length):
        super().__init__(action_space)
        self.name="SimpleMovingAverageAgent"
        self.history_length= history_length
        self.has_shares = False

    def choose_action(self, observation):
        price_history = observation[:self.history_length]
        shares = observation[self.history_length+1]

        current_price = observation[-1]

        moving_avg = np.mean(price_history)

        self.has_shares = (shares > 0)

        if current_price > moving_avg and not self.has_shares:
            return 1  # BUY
        elif current_price < moving_avg and self.has_shares:
            return 2  # SELL
        else:
            return 0  # HOLD
    
    def reset(self):
        self.has_shares = False