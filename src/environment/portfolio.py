class Portfolio:

    def __init__(self, initial_cash=10000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.shares = 0 
        self.share_price = 0

    
    def reset(self):
        self.cash = initial_cash
        self.shares = 0 
        self.share_price = 0

    def get_value(self,current_price):
        self.share_price = current_price
        stock_value = self.shares * self.current_price
        return self.cash + stock_value

    def buy(self,current_price):
        if self.cash<current_price:
            return 0
        
        shares_to_buy = int(self.cash/current_price)
        total_cost = shares_to_buy * current_price
        
        self.cash -= total_cost
        self.shares += shares_to_buy

        return shares_to_buy

    def sell(self,current_price):
        if self.shares == 0:
            return 0
        
        total_value = self.shares * current_price
        
        self.cash += total_value
        shares_sold = self.shares
        self.shares = 0

        return shares_sold

    def get_state_info(self):
        return {
            'cash': self.cash,
            'shares': self.shares,
            'share_price': self.share_price,
            'total_value': self.cash + (self.shares * self.share_price)
        }

