__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


from .animals import Animal

class Carnivore(Animal):
    def __init__(self, weight, age):
        super().__init__(weight, age)
        


if __name__ == "__main__":
    c = Carnivore(0, 10)
    print(c.weight)