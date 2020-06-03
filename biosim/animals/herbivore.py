__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


from .animals import Animal


class Herbivore(Animal):
    def __init__(self, age, weight):
        super().__init__(age, weight)
        pass


if __name__ == "__main__":
    h = Herbivore(3, 10)
    print(h.age)