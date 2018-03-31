class Goku:
    """
        Implements the AI agent for the gomoku game. It uses the minimax
    algorithm to find the best option for the next move, using alpha-beta
    pruning
    """

    def __init__(self):
        pass

    def search(self, state, max_level=3):
        """
            1 - Makes a depth-first-search till raise the max_level of the tree
            2 - When got to the max_level, computes the heuristic
            3 - Recursively updates the parent nodes alha/beta with the right
            values
            4 - Make the pruning when needed
            5 - After compute 'all' the possibilities, return the next movement
        """
        pass

    def heuristic(self, state):
        postive_factor = (self.doubles_from_ai() +
                          150 * self.triples_from_ai() +
                          95 * self.quartet_from_ai())
        negative_factor = (self.doubles_from_human() +
                           150 * self.triples_from_human() +
                           95 * self.quartet_from_human())
        return postive_factor - 0.5 * negative_factor

    def utility(self, state):
        pass

    def doubles_from_ai(self):
        pass

    def triples_from_ai(self):
        pass

    def quartet_from_ai(self):
        pass

    def doubles_from_human(self):
        pass

    def triples_from_human(self):
        pass

    def quartet_from_human(self):
        pass
