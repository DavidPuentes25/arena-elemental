# Importa la clase base Enemigo
from src.modelos.enemigo import Enemigo


# Goblin hereda las características de Enemigo
class Goblin(Enemigo):

    # Define las estadísticas propias del Goblin
    def __init__(self):
        super().__init__(
            nombre="Goblin",
            vida=70,
            ataque=20,
            defensa=6
        )

    # Polimorfismo: comportamiento propio del Goblin
    def realizar_turno(self, objetivo):

        # Realiza un ataque normal
        danio = self.atacar(objetivo)

        # Devuelve daño y nombre de la acción
        return danio, "Ataque normal"