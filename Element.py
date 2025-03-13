class Element:
    def __init__(self, char_repr):
        self.char_repr = char_repr
    
    def __repr__(self):
        return self.char_repr
    
    def __eq__(self, other):
        return isinstance(other, Element) and self.char_repr == other.char_repr
