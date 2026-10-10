# Permite generar decisiones aleatorias
import random

# Importa la clase base Enemigo
from src.modelos.enemigo import Enemigo


# JefeFinal representa al enemigo más fuerte
class JefeFinal(Enemigo):

    # Define estadísticas superiores a enemigos normales
    def __init__(self):
        super().__init__(
            nombre="Guardián Elemental",
            vida=180,
            ataque=30,
            defensa=15
        )

    # Polimorfismo: comportamiento especial del jefe
    def realizar_turno(self, objetivo):

        # Genera una decisión aleatoria
        decision = random.random()

        # 40 % de probabilidad de ataque devastador
        if decision < 0.4:

            # Aumenta el ataque en un 70 %
            ataque_especial = int(self.ataque * 1.7)

            # Calcula el daño final
            danio = max(1, ataque_especial - objetivo.defensa)

            # Aplica el daño
            objetivo.recibir_danio(danio)

            return danio, "Golpe devastador"

        # Ataque normal en los demás casos
        danio = self.atacar(objetivo)

        return danio, "Ataque normal"