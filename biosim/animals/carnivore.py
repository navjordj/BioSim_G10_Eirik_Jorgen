__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


from animal import Animal

class Carnivore(Animal):
    def __init__(self, weight, pos):
        super().__init__(weight, pos)
        pass
