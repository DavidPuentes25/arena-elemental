from src.modelos.personaje import Personaje
from src.habilidades.habilidad import Habilidad


class Mago(Personaje):

    def __init__(self, nombre: str):
        super().__init__(
            nombre=nombre,
            vida=400,
            ataque=30,
            defensa=8
        )

        # Indica que el siguiente turno enemigo
        # queda bloqueado por Congelación.
        self._congelacion_activa = False

        self._habilidades = [
            Habilidad(
                "Bola de fuego",
                "Ataque mágico x1.8",
                3,
                Mago.bola_de_fuego
            ),
            Habilidad(
                "Congelación",
                "Daña y bloquea el siguiente ataque enemigo",
                5,
                Mago.congelacion
            ),
            Habilidad(
                "Curación arcana",
                "Recupera 25 puntos de vida",
                5,
                Mago.curacion_arcana
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
    # BOLA DE FUEGO
    # ==========================================

    def bola_de_fuego(
        self,
        objetivo
    ):
        danio = max(
            1,
            int(self.ataque * 1.8)
            - objetivo.defensa
        )

        danio_real = objetivo.recibir_danio(
            danio
        )

        return {
            "nombre": "Bola de fuego",
            "danio": danio_real
        }

    # ==========================================
    # CONGELACIÓN
    # ==========================================

    def congelacion(
        self,
        objetivo
    ):
        danio = max(
            1,
            self.ataque
            - objetivo.defensa
        )

        danio_real = objetivo.recibir_danio(
            danio
        )

        # El próximo ataque enemigo
        # no causará daño.
        self._congelacion_activa = True

        return {
            "nombre": "Congelación",
            "danio": danio_real
        }

    # ==========================================
    # CURACIÓN ARCANA
    # ==========================================

    def curacion_arcana(
        self,
        objetivo
    ):
        # No permite desperdiciar la habilidad
        # cuando la vida está completa.
        if self.vida >= self.vida_maxima:
            return None

        vida_antes = self.vida

        self.curar(
            25
        )

        cantidad_curada = (
            self.vida - vida_antes
        )

        return {
            "nombre": "Curación arcana",
            "danio": 0,
            "curacion": cantidad_curada
        }

    # ==========================================
    # RECIBIR DAÑO
    # ==========================================

    def recibir_danio(
        self,
        cantidad
    ):
        # Simula que el enemigo pierde su turno
        # cuando está afectado por Congelación.
        if self._congelacion_activa:

            self._congelacion_activa = False

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
        return self.bola_de_fuego(
            objetivo
        )