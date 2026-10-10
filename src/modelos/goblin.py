# Importa la clase base Enemigo
from src.modelos.enemigo import Enemigo


# Goblin hereda las características de Enemigo
class Goblin(Enemigo):

    # Define las estadísticas propias del Goblin
    def __init__(self):
        super().__init__(
            nombre="Goblin",
            vida=70,
            ataque=18,
            defensa=6
        )

    # Polimorfismo: comportamiento del Goblin en su turno
    def realizar_turno(self, objetivo):

        # El Goblin realiza un ataque normal
        danio = self.atacar(objetivo)

        return danio