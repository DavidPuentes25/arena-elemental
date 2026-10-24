from src.modelos.personaje import Personaje


class Guerrero(Personaje):

    def __init__(self, nombre: str):
        super().__init__(
            nombre=nombre,
            vida=120,
            ataque=25,
            defensa=15
        )

    # Habilidad especial del Guerrero
    def usar_habilidad_especial(self, objetivo):
        ataque_especial = int(self.ataque * 1.5)

        danio = max(
            1,
            ataque_especial - objetivo.defensa
        )

        danio_real = objetivo.recibir_danio(
            danio
        )

        return {
            "nombre": "Golpe fuerte",
            "danio": danio_real
        }