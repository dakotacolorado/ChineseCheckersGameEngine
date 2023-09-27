
class Vector:
    
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j

    def __eq__(self, other: 'Vector') -> bool:
        if not isinstance(other, Vector):
            return False

        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash((self.i, self.j))