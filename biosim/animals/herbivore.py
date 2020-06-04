__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


from .animals import Animal


params = {
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.6,
        "weight_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
        "delta_phi_max": None
    }

class Herbivore(Animal):
    
    def __init__(self, age: int, weight: float) -> None:
        super().__init__(age, weight)
        self._params = params


    @classmethod
    def set_params(cls, params: dict) -> None:
        cls._params = params


if __name__ == "__main__":
    h = Herbivore(3, 10)
    print(h)
    h.increase_age()
    print(h)
    h.update_weight(10000)
    print(h)