class Combo:
    def __init__(self, _start):
        self.start = _start
        self.combo_node = []

    def add_node(self, node):
        self.combo_node.append(node)

    def len(self):
        return len(self.combo_node)
