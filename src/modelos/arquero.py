import random

from src.modelos.personaje import Personaje
from src.habilidades.habilidad import Habilidad


class Arquero(Personaje):

    def __init__(self, nombre: str):
        super().__init__(
            nombre=nombre,
            vida=140,
            ataque=27,
            defensa=10
        )

        # Se activa al usar Evasión.
        self._evasion_activa = False

        self._habilidades = [
            Habilidad(
                "Disparo crítico",
                "50% x2 daño / 50% x1.2 daño",
                2,
                Arquero.disparo_critico
            ),
            Habilidad(
                "Flecha perforante",
                "Ignora la defensa del enemigo",
                3,
                Arquero.flecha_perforante
            ),
            Habilidad(
                "Evasión",
                "80% de evitar el siguiente ataque",
                4,
                Arquero.evasion
            )
        ]

    # ==========================================
    # HABILIDADES
    # ==========================================

    @property
    def habilidades(self):
        return self._habilidades

    # ==========================================
    # COOLDOWNS
    # ==========================================

    def avanzar_cooldowns(
        self,
        habilidad_usada=None
    ):
        for habilidad in self._habilidades:

            if habilidad is not habilidad_usada:
                habilidad.avanzar_turno()

    # ==========================================
    # DISPARO CRÍTICO
    # ==========================================

    def disparo_critico(
        self,
        objetivo
    ):
        # 50% de probabilidad para cada resultado.
        if random.random() < 0.5:

            multiplicador = 2.0
            tipo = "Crítico"

        else:

            multiplicador = 1.2
            tipo = "Potenciado"

        danio = max(
            1,
            int(self.ataque * multiplicador)
            - objetivo.defensa
        )

        danio_real = objetivo.recibir_danio(
            danio
        )

        return {
            "nombre": "Disparo crítico",
            "danio": danio_real,
            "tipo": tipo
        }

    # ==========================================
    # FLECHA PERFORANTE
    # ==========================================

    def flecha_perforante(
        self,
        objetivo
    ):
        # No se resta la defensa del enemigo.
        danio = self.ataque

        danio_real = objetivo.recibir_danio(
            danio
        )

        return {
            "nombre": "Flecha perforante",
            "danio": danio_real
        }

    # ==========================================
    # EVASIÓN
    # ==========================================

    def evasion(
        self,
        objetivo
    ):
        if self._evasion_activa:
            return None

        self._evasion_activa = True

        return {
            "nombre": "Evasión",
            "danio": 0
        }

    # ==========================================
    # RECIBIR DAÑO
    # ==========================================

    def recibir_danio(
        self,
        cantidad
    ):
        if self._evasion_activa:

            # Solo sirve para el próximo ataque.
            self._evasion_activa = False

            # 80% de probabilidad de esquivarlo.
            if random.random() < 0.80:
                return 0

        return super().recibir_danio(
            cantidad
        )

    # ==========================================
    # MÉTODO ABSTRACTO
    # ==========================================

    def usar_habilidad_especial(
        self,
        objetivo
    ):
        return self.disparo_critico(
            objetivo
        )