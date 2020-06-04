__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


from .animals import Animal


params = {
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 40.0,
        "phi_age": 0.3,
        "weight_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.8,
        "F": 50.0,
        "delta_phi_max": 10
    }

class Carnivore(Animal):

    def __init__(self) -> None:
        super().__init__()
        self._params = params
        

    @classmethod
    def set_params(cls, params: dict) -> None:
        cls._params = params


if __name__ == "__main__":
    c = Carnivore(0, 10)
    print(c.weight)