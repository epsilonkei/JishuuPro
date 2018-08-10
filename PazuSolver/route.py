class Route:
    def __init__(self, _start):
        self.start = _start
        self.end = _start
        self.direction = []
        self.ncombos = 0 
        self.dropcoms = 0
        self.sumcoms = 0
        
    def update(self, step, end):
        self.direction.append(step)
        self.end = end

    def update_rou(self, rou, end):
        self.direction.extend(rou)
        self.end = end
    
    def set_ncombos(self, n, d):
        self.ncombos = n
        self.dropcoms = d
        self.sumcoms = n + 0.1*d

    def print_route(self):
        print self.ncombos, self.dropcoms, self.start, self.end
        print self.direction
        
    def copy_route(self, n_route):
        self.start = n_route.start[:] 
        self.end = n_route.end[:]
        self.direction = n_route.direction[:]
        self.combos = n_route.ncombos 
        self.dropcoms = n_route.dropcoms
        self.sumcoms = n_route.sumcoms
