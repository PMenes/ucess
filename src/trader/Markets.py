import src.utils as u
from src.trader.Orders import SingleOrder

class Markets():
    def __init__(self, sens, name, orders):
        self.logname = orders.logname.replace("orders", "markets")
        self.logger = orders.logger.thisClassLogger(self)
        self.sens = sens
        self.name = name
        self.orders = orders
        self.max_take = 3
        self.lst = []
        self.best = 0
        self.oppo=0

    def best_price(self):
        return self.best

    def update(self, markets):
        self.oppo = self.oppo or self.orders.asset.masks if self.sens>0 else self.orders.asset.mbids
        pprice = 0; p = 0; self.lst = []
        for h in markets:
            np = round(h.price,2)
            if np == pprice:
                p["size"] += h.size
            else:
                pprice = np
                if self.keep(p, markets): break
                p = {"price":np, "size": h.size}

        self.best = self.lst[0]["price"] if len(self.lst) else 0


    def keep(self, p, markets):
        if not p: return
        o = self.orders.order_at_price(p["price"]) # orders we have at this price
        if o:
            if abs(o.h["size"]) > abs(p["size"]):
                self.warning(f'size={p["size"]}, but live order with bigger size !!', o.show())
            p["size"] -= o.h["size"] # substract our size from market size
        if p["size"] > 0: u.push(self.lst, p)
        return len(self.lst) > self.max_take - 1
