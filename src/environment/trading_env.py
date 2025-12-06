import gymnasium as gym
import numpy as nump
from gymnasium import spaces

class TradingEnv(gym.Env):

    HOLD = 0
    BUY = 1
    SELL = 2

    def __init__(self,price_data,initial_cash=10000,history_length=10):
        super(TradingEnv, self).__init__()
        self.price_data = np.array(price_data)
        self.initial_cash = initial_cash
        self.history_length = history_length
        self.n_steps = len(self.price_data) - self.history_length

        self.cash = initial_cash
        self.shares = 0
        self.current_step = 0
        self.previous_portfolio_value = initial_cash

        self.action_space = spaces.Discrete(3)

        obs_size = history_length + 3
        self.observation_space = spaces.Box(
            low = 0
            high = np.inf
            shape=(obs_size,)
            dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.cash = self.initial_cash
        self.shares = 0 
        self.current_step = 0
        self.previous_portfolio_value = initial_cash

        observation = self._get_observation()
        info = self._get_info()

        return observation,info

    def _get_current_price(self):
        price_idx=self.current_step + self.history_length - 1
        return self.price_data[price_idx]

    def _get_observation(self):
        start_idx = self.current_step
        end_idx = self.current_step + self.history_length
        price_history = self.price_data[start_idx:end_idx]

        current_price = self._get_current_price()

        portfolio_value = self.cash + (self.shares * current_price)

        observation = np.concatenate([
            price_history,
            [self.cash, self.shares, portfolio_value]
        ]).astype(np.float32)

        return observation

    def _get_info(self):
        current_price = self._get_current_price()
        portfolio_value = self.cash + (self.shares * current_price)

        return {
            'step': self.current_step,
            'cash': self.cash,
            'shares': self.shares,
            'current_price': current_price,
            'portfolio_value': portfolio_value,
            'profit': portfolio_value - self.initial_cash   
        }

    def step(self, action):

        current_price = self._get_current_price()

        if action == self.BUY:
            if self.cash >= current_price:
                shares_to_buy = int(self.cash/current_price)
                cost = shares_to_buy * current_price
                self.cash -= cost
                self.shares += shares_to_buy

        elif action == self.SELL:
            if self.shares>0:
                revenue = self.shares * current_price
                self.cash += revenue
                self.shares = 0

        # if action is hold do nothing

        self.current_step += 1 
        
        new_current_price = self._get_current_price
        current_portfolio_value = self.cash + (self.shares * new_current_price)
        reward = current_portfolio_value - self.previous_portfolio_value

        self.previous_portfolio_value = current_portfolio_value

        terminated = self.current_step >= self.n_steps
        truncated = false

        observation = self._get_observation
        info = self._get_info
        
        return observation, reward, terminated, truncated, info

