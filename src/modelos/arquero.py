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

    # Polimorfismo: habilidad propia del Arquero
def usar_habilidad_especial(self, objetivo):

    # 50 % de probabilidad de golpe crítico
    es_critico = random.random() < 0.5

    # Define el multiplicador del ataque
    multiplicador = 2 if es_critico else 1.2

    # Calcula y aplica el daño
    ataque_especial = int(self.ataque * multiplicador)
    danio = max(1, ataque_especial - objetivo.defensa)
    objetivo.recibir_danio(danio)

    # Devuelve información de la habilidad
    return {
        "nombre": "Disparo crítico" if es_critico else "Disparo preciso",
        "danio": danio
    }