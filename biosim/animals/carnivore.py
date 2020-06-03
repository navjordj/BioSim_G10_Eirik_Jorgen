__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


from .animals import Animal

class Carnivore(Animal):
    def __init__(self, age, weight):
        super().__init__(age, weight)
        


if __name__ == "__main__":
    c = Carnivore(0, 10)
    print(c.weight)