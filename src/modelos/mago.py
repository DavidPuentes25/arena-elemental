# Importa la clase base Personaje
from src.modelos.personaje import Personaje


# Mago hereda las características de Personaje
class Mago(Personaje):

    # Define las estadísticas propias del Mago
    def __init__(self, nombre: str):
        super().__init__(
            nombre=nombre,
            vida=90,
            ataque=30,
            defensa=8
        )

    # Polimorfismo: habilidad propia del Mago
def usar_habilidad_especial(self, objetivo):

    # Aumenta el poder mágico en un 80 %
    ataque_magico = int(self.ataque * 1.8)

    # Calcula y aplica el daño
    danio = max(1, ataque_magico - objetivo.defensa)
    objetivo.recibir_danio(danio)

    # Devuelve información de la habilidad
    return {
        "nombre": "Ataque mágico",
        "danio": danio
    }