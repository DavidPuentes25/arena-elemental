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
            ataque=30,
            defensa=10
        )

    # Polimorfismo: habilidad propia del Arquero
# Polimorfismo: habilidad propia del Arquero
def usar_habilidad_especial(self, objetivo):

    # 50 % de probabilidad de crítico
    es_critico = random.random() < 0.5

    multiplicador = 2 if es_critico else 1.2
    ataque_especial = int(self.ataque * multiplicador)

    danio = max(1, ataque_especial - objetivo.defensa)

    # Aplica y obtiene el daño real
    danio_real = objetivo.recibir_danio(danio)

    return {
        "nombre": "Disparo crítico" if es_critico else "Disparo preciso",
        "danio": danio_real,
        "critico": es_critico
    }