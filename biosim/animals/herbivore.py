from .animal import Animal

class Herbivore(Animal):
    params: dict = {
                "w_birth": 8.0,
                "sigma_birth": 1.5,
                "beta": 0.9,
                "eta": 0.05,
                "a_half": 40.0,
                "phi_age": 0.6,
                "w_half": 10.0,
                "phi_weight": 0.1,
                "mu": 0.25,
                "gamma": 0.2,
                "zeta": 3.5,
                "xi": 1.2,
                "omega": 0.4,
                "F": 10.0,
                "DeltaPhiMax": None
            }
    def __init__(self, age=None, weight=None) -> None:
        super().__init__(age, weight)
