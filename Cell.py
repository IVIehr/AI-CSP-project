class Cell:
    def __init__(self, x, y, domain=['w', 'b'], value='_'):
        self.x = x
        self.y = y
        self.domain = domain
        self.value = value


    def is_empty(self):
        return self.value == '_'


    def set_val(self, val):
        self.value = val
        self.domain = [val]


    def remove_val(self):
        self.value = '_'
        self.domain = ['w', 'b']
