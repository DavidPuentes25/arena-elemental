# Importa la clase base Personaje
from src.modelos.personaje import Personaje


# Guerrero hereda características de Personaje
class Guerrero(Personaje):

    # Define las estadísticas propias del Guerrero
    def __init__(self, nombre: str):
        super().__init__(
            nombre=nombre,
            vida=120,
            ataque=25,
            defensa=15
        )

    # Polimorfismo: habilidad propia del Guerrero
    def usar_habilidad_especial(self, objetivo):

        # Aumenta el ataque en un 50 %
        ataque_especial = int(self.ataque * 1.5)

        # Calcula y aplica el daño
        danio = max(1, ataque_especial - objetivo.defensa)
        objetivo.recibir_danio(danio)

        # Devuelve información de la habilidad
        return {
            "nombre": "Golpe fuerte",
            "danio": danio
        }