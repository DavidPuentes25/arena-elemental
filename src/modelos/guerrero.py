from src.modelos.personaje import Personaje
from src.habilidades.habilidad import Habilidad


class Guerrero(Personaje):

    def __init__(self, nombre: str):
        super().__init__(
            nombre=nombre,
            vida=520,
            ataque=25,
            defensa=15
        )

        self._turnos_grito = 0
        self._guardia_ferrea = False

        self._habilidades = [
            Habilidad(
                "Golpe devastador",
                "Ataque de fuerza x1.7",
                3,
                Guerrero.golpe_devastador
            ),
            Habilidad(
                "Grito de guerra",
                "+30% ataque durante 3 ataques",
                5,
                Guerrero.grito_de_guerra
            ),
            Habilidad(
                "Guardia férrea",
                "-70% del siguiente golpe",
                4,
                Guerrero.guardia_ferrea
            )
        ]

    @property
    def habilidades(self):
        return self._habilidades

    @property
    def turnos_grito(self):
        return self._turnos_grito

    def avanzar_cooldowns(self, habilidad_usada=None):
        for habilidad in self._habilidades:
            if habilidad is not habilidad_usada:
                habilidad.avanzar_turno()

    def calcular_danio(self, objetivo):
        ataque = self.ataque

        if self._turnos_grito > 0:
            ataque = int(ataque * 1.30)

        return max(1, ataque - objetivo.defensa)

    def _consumir_grito(self):
        if self._turnos_grito > 0:
            self._turnos_grito -= 1

    def atacar(self, objetivo):
        danio = self.calcular_danio(objetivo)
        resultado = objetivo.recibir_danio(danio)
        self._consumir_grito()
        return resultado

    def golpe_devastador(self, objetivo):
        ataque = self.ataque

        if self._turnos_grito > 0:
            ataque = int(ataque * 1.30)

        danio = max(
            1,
            int(ataque * 1.7) - objetivo.defensa
        )

        resultado = objetivo.recibir_danio(danio)
        self._consumir_grito()

        return {
            "nombre": "Golpe devastador",
            "danio": resultado
        }

    def grito_de_guerra(self, objetivo):
        if self._turnos_grito > 0:
            return None

        self._turnos_grito = 3

        return {
            "nombre": "Grito de guerra",
            "danio": 0
        }

    def guardia_ferrea(self, objetivo):
        if self._guardia_ferrea:
            return None

        self._guardia_ferrea = True

        return {
            "nombre": "Guardia férrea",
            "danio": 0
        }

    def recibir_danio(self, cantidad):
        if self._guardia_ferrea:
            cantidad = max(1, int(cantidad * 0.30))
            self._guardia_ferrea = False

        return super().recibir_danio(cantidad)

    # Compatibilidad con el sistema anterior
    def usar_habilidad_especial(self, objetivo):
        return self.golpe_devastador(objetivo)