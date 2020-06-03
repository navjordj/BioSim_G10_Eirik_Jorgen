class Animal:

    def __init__(self, weight, pos):
        self.age = 0
        self.pos = pos
        self.weight = weight
        self.fitness = None

    @staticmethod
    def increase_age(self):
        self.age += 1
        return True

    def update_weight(self, change):
        self.weight += change

    def update_fitness(self):
        """
        Update fitness based on given function in document
        """
        pass

    def die(self):
        pass

    def get_child(self, probability):
        """
        Spawn a child. Probability given by probability parameter.
        """
        pass

    def migration(self):
        # Check surroundings
        # if: self.pos = blabla
        pass

    def update_parameters(self, **kwargs):
        """ 
        Update parameters for a given animal
        """
        pass
