import random

from src.modelos.enemigo import Enemigo
from src.objetos.pocion_vida import PocionVida


class Goblin(Enemigo):

    def __init__(self):
        super().__init__(
            nombre="Goblin",
            vida=200,
            ataque=23,
            defensa=9
        )

        # ==========================================
        # HABILIDAD: PUÑALADA TRAICIONERA
        # ==========================================

        self._cooldown_punalada = 0
        self._cooldown_punalada_max = 2

        # ==========================================
        # HABILIDAD: EVASIÓN
        # ==========================================

        self._cooldown_evasion = 0
        self._cooldown_evasion_max = 4

        self._evasion_activa = False

        # ==========================================
        # INVENTARIO
        # ==========================================

        # El Goblin comienza con una sola poción.
        self.agregar_objeto(
            PocionVida()
        )

    # =====================================================
    # COOLDOWNS
    # =====================================================

    def avanzar_cooldowns(self):

        if self._cooldown_punalada > 0:
            self._cooldown_punalada -= 1

        if self._cooldown_evasion > 0:
            self._cooldown_evasion -= 1

    # =====================================================
    # ATAQUE NORMAL
    # =====================================================

    def ataque_normal(
        self,
        jugador
    ):
        danio = max(
            1,
            self.ataque - jugador.defensa
        )

        danio_real = jugador.recibir_danio(
            danio
        )

        return {
            "accion": "Ataque",
            "danio": danio_real,
            "atacante": self.nombre,
            "objetivo": jugador.nombre
        }

    # =====================================================
    # PUÑALADA TRAICIONERA
    # =====================================================

    def punalada_traicionera(
        self,
        jugador
    ):
        danio = max(
            1,
            int(self.ataque * 1.50)
            - jugador.defensa
        )

        danio_real = jugador.recibir_danio(
            danio
        )

        self._cooldown_punalada = (
            self._cooldown_punalada_max
        )

        return {
            "accion": "Puñalada traicionera",
            "danio": danio_real,
            "atacante": self.nombre,
            "objetivo": jugador.nombre
        }

    # =====================================================
    # EVASIÓN
    # =====================================================

    def activar_evasion(self):

        self._evasion_activa = True

        self._cooldown_evasion = (
            self._cooldown_evasion_max
        )

        return {
            "accion": "Evasión",
            "danio": 0,
            "atacante": self.nombre,
            "objetivo": self.nombre
        }

    # =====================================================
    # RECIBIR DAÑO
    # =====================================================

    def recibir_danio(
        self,
        cantidad
    ):
        if self._evasion_activa:

            self._evasion_activa = False

            # 65% de probabilidad de esquivar.
            if random.random() < 0.65:

                return 0

        return super().recibir_danio(
            cantidad
        )

    # =====================================================
    # BUSCAR POCIÓN
    # =====================================================

    def buscar_pocion(self):

        for indice, objeto in enumerate(
            self.inventario
        ):

            if objeto.nombre == "Poción de Vida":
                return indice

        return None

    # =====================================================
    # USAR POCIÓN
    # =====================================================

    def usar_pocion(self):

        indice = self.buscar_pocion()

        if indice is None:
            return None

        vida_antes = self.vida

        self.usar_objeto(
            indice
        )

        curacion = (
            self.vida - vida_antes
        )

        return {
            "accion": "Usar Poción",
            "danio": 0,
            "curacion": curacion,
            "atacante": self.nombre,
            "objetivo": self.nombre
        }

    # =====================================================
    # IA DEL GOBLIN
    # =====================================================

    def realizar_turno(
        self,
        jugador
    ):
        self.avanzar_cooldowns()

        vida_goblin = (
            self.vida
            / self.vida_maxima
        )

        vida_jugador = (
            jugador.vida
            / jugador.vida_maxima
        )

        # =================================================
        # PRIORIDAD 1
        # CURARSE SI ESTÁ A PUNTO DE MORIR
        # =================================================

        if vida_goblin <= 0.30:

            indice_pocion = (
                self.buscar_pocion()
            )

            if indice_pocion is not None:

                return self.usar_pocion()

        # =================================================
        # PRIORIDAD 2
        # REMATAR AL JUGADOR
        # =================================================

        if (
            vida_jugador <= 0.30
            and self._cooldown_punalada == 0
        ):

            return self.punalada_traicionera(
                jugador
            )

        # =================================================
        # PRIORIDAD 3
        # EVASIÓN CUANDO ESTÁ HERIDO
        # =================================================

        if (
            vida_goblin <= 0.50
            and self._cooldown_evasion == 0
            and random.random() < 0.45
        ):

            return self.activar_evasion()

        # =================================================
        # PRIORIDAD 4
        # USAR HABILIDAD OFENSIVA
        # =================================================

        if (
            self._cooldown_punalada == 0
            and random.random() < 0.40
        ):

            return self.punalada_traicionera(
                jugador
            )

        # =================================================
        # ATAQUE NORMAL
        # =================================================

        return self.ataque_normal(
            jugador
        )

    # =====================================================
    # COMPATIBILIDAD
    # =====================================================

    def usar_habilidad_especial(
        self,
        objetivo
    ):
        return self.punalada_traicionera(
            objetivo
        )