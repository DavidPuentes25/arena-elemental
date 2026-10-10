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

    # Polimorfismo: habilidad específica del Guerrero
    def usar_habilidad_especial(self, objetivo):

        # Golpe fuerte aumenta el ataque en un 50 %
        ataque_especial = int(self.ataque * 1.5)

        # Calcula el daño teniendo en cuenta la defensa enemiga
        danio = max(1, ataque_especial - objetivo.defensa)

        # Aplica el daño al objetivo
        objetivo.recibir_danio(danio)

        return danio