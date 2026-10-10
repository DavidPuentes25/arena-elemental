# Permite generar valores aleatorios
import random

# Importa la clase base Personaje
from src.modelos.personaje import Personaje


# Arquero hereda las características de Personaje
class Arquero(Personaje):

    # Define las estadísticas propias del Arquero
    def __init__(self, nombre: str):
        super().__init__(
            nombre=nombre,
            vida=100,
            ataque=22,
            defensa=10
        )

    # Polimorfismo: habilidad específica del Arquero
    def usar_habilidad_especial(self, objetivo):

        # Probabilidad de golpe crítico del 50 %
        es_critico = random.random() < 0.5

        # Si es crítico, duplica el ataque
        multiplicador = 2 if es_critico else 1.2

        # Calcula el ataque especial
        ataque_especial = int(self.ataque * multiplicador)

        # Calcula el daño final
        danio = max(1, ataque_especial - objetivo.defensa)

        # Aplica el daño al objetivo
        objetivo.recibir_danio(danio)

        # Devuelve daño y si fue crítico
        return danio, es_critico