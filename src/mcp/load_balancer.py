import itertools

class RoundRobinBalancer:
    def __init__(self, agents):
        self.pool = itertools.cycle(agents)

    def next(self):
        return next(self.pool)