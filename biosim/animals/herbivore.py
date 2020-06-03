__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


from animals import Animal


class Herbivore(Animal):
    def __init__(self, weight, pos):
        super().__init__(weight, pos)
        pass


if __name__ == "__main__":
    h = Herbivore(0, 10)
