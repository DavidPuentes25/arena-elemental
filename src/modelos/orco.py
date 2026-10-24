# Permite generar decisiones aleatorias
import random

# Importa la clase base Enemigo
from src.modelos.enemigo import Enemigo


# Orco hereda las características de Enemigo
class Orco(Enemigo):

    # Define las estadísticas propias del Orco
    def __init__(self):
        super().__init__(
            nombre="Orco",
            vida=250,
            ataque=30,
            defensa=12
        )

    # Polimorfismo: el Orco puede realizar dos tipos de ataque
    def realizar_turno(self, objetivo):

        # 30 % de probabilidad de realizar un golpe fuerte
        golpe_fuerte = random.random() < 0.3

        if golpe_fuerte:
            # Aumenta el ataque en un 50 %
            ataque_especial = int(self.ataque * 1.5)

            # Calcula el daño final
            danio = max(1, ataque_especial - objetivo.defensa)

            # Aplica el daño y obtiene el daño real
            danio_real = objetivo.recibir_danio(danio)

            return danio_real, "Golpe fuerte"

        # Si no usa habilidad, realiza ataque normal
        danio = self.atacar(objetivo)

        return danio, "Ataque normal"