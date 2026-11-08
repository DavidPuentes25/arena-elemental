import random

from src.modelos.enemigo import Enemigo
from src.objetos.pocion_vida import PocionVida
from src.objetos.escudo_protector import EscudoProtector


class Orco(Enemigo):

    def __init__(self):
        super().__init__(
            nombre="Orco",
            vida=100,
            ataque=16,
            defensa=18
        )

        # ==========================================
        # GOLPE BRUTAL
        # ==========================================

        self._cooldown_brutal = 0
        self._cooldown_brutal_max = 3

        # ==========================================
        # EMBESTIDA
        # ==========================================

        self._cooldown_embestida = 0
        self._cooldown_embestida_max = 4

        # ==========================================
        # FURIA
        # ==========================================

        self._furia_usada = False
        self._turnos_furia = 0

        # Evita defenderse dos veces seguidas
        self._ultimo_movimiento = None

        # ==========================================
        # INVENTARIO
        # ==========================================

        self.agregar_objeto(
            PocionVida()
        )

        self.agregar_objeto(
            EscudoProtector()
        )

    # =====================================================
    # ESTADOS
    # =====================================================

    @property
    def furia_activa(self):
        return self._turnos_furia > 0

    @property
    def turnos_furia(self):
        return self._turnos_furia

    # =====================================================
    # ATAQUE REAL
    # =====================================================

    def ataque_actual(self):

        ataque = self.ataque

        if self._turnos_furia > 0:
            ataque = int(
                ataque * 1.35
            )

        return ataque

    def consumir_furia(self):

        if self._turnos_furia > 0:
            self._turnos_furia -= 1

    # =====================================================
    # COOLDOWNS
    # =====================================================

    def avanzar_cooldowns(self):

        if self._cooldown_brutal > 0:
            self._cooldown_brutal -= 1

        if self._cooldown_embestida > 0:
            self._cooldown_embestida -= 1

    # =====================================================
    # ATAQUE NORMAL
    # =====================================================

    def ataque_normal(
        self,
        jugador
    ):
        ataque = self.ataque_actual()

        danio = max(
            1,
            ataque - jugador.defensa
        )

        danio_real = jugador.recibir_danio(
            danio
        )

        self.consumir_furia()

        self._ultimo_movimiento = "Ataque"

        return {
            "accion": "Ataque",
            "danio": danio_real,
            "atacante": self.nombre,
            "objetivo": jugador.nombre
        }

    # =====================================================
    # GOLPE BRUTAL
    # =====================================================

    def golpe_brutal(
        self,
        jugador
    ):
        ataque = self.ataque_actual()

        danio = max(
            1,
            int(ataque * 1.75)
            - jugador.defensa
        )

        danio_real = jugador.recibir_danio(
            danio
        )

        self._cooldown_brutal = (
            self._cooldown_brutal_max
        )

        self.consumir_furia()

        self._ultimo_movimiento = (
            "Golpe brutal"
        )

        return {
            "accion": "Golpe brutal",
            "danio": danio_real,
            "atacante": self.nombre,
            "objetivo": jugador.nombre
        }

    # =====================================================
    # EMBESTIDA
    # =====================================================

    def embestida(
        self,
        jugador
    ):
        ataque = self.ataque_actual()

        # Solo toma en cuenta el 50%
        # de la defensa del jugador.
        defensa_reducida = int(
            jugador.defensa * 0.50
        )

        danio = max(
            1,
            int(ataque * 1.35)
            - defensa_reducida
        )

        danio_real = jugador.recibir_danio(
            danio
        )

        self._cooldown_embestida = (
            self._cooldown_embestida_max
        )

        self.consumir_furia()

        self._ultimo_movimiento = (
            "Embestida"
        )

        return {
            "accion": "Embestida",
            "danio": danio_real,
            "atacante": self.nombre,
            "objetivo": jugador.nombre
        }

    # =====================================================
    # FURIA
    # =====================================================

    def activar_furia(self):

        self._furia_usada = True

        # Los siguientes 3 ataques
        # tendrán +35% de ataque.
        self._turnos_furia = 3

        self._ultimo_movimiento = "Furia"

        return {
            "accion": "Furia",
            "danio": 0,
            "atacante": self.nombre,
            "objetivo": self.nombre
        }

    # =====================================================
    # DEFENDERSE
    # =====================================================

    def defender(self):

        self.defenderse()

        self._ultimo_movimiento = "Defender"

        return {
            "accion": "Defender",
            "danio": 0,
            "atacante": self.nombre,
            "objetivo": self.nombre
        }

    # =====================================================
    # BUSCAR OBJETO
    # =====================================================

    def buscar_objeto(
        self,
        nombre
    ):
        for indice, objeto in enumerate(
            self.inventario
        ):

            if objeto.nombre == nombre:
                return indice

        return None

    # =====================================================
    # POCIÓN
    # =====================================================

    def usar_pocion(self):

        indice = self.buscar_objeto(
            "Poción de Vida"
        )

        if indice is None:
            return None

        vida_anterior = self.vida

        self.usar_objeto(
            indice
        )

        curacion = (
            self.vida - vida_anterior
        )

        self._ultimo_movimiento = (
            "Usar Poción"
        )

        return {
            "accion": "Usar Poción",
            "danio": 0,
            "curacion": curacion,
            "atacante": self.nombre,
            "objetivo": self.nombre
        }

    # =====================================================
    # ESCUDO
    # =====================================================

    def usar_escudo(self):

        indice = self.buscar_objeto(
            "Escudo Protector"
        )

        if indice is None:
            return None

        self.usar_objeto(
            indice
        )

        self._ultimo_movimiento = (
            "Usar Escudo"
        )

        return {
            "accion": "Usar Escudo",
            "danio": 0,
            "reduccion": 30,
            "turnos": 5,
            "atacante": self.nombre,
            "objetivo": self.nombre
        }

    # =====================================================
    # DAÑO ESTIMADO
    # =====================================================

    def estimar_danio_normal(
        self,
        jugador
    ):
        return max(
            1,
            self.ataque_actual()
            - jugador.defensa
        )

    def estimar_danio_brutal(
        self,
        jugador
    ):
        return max(
            1,
            int(
                self.ataque_actual()
                * 1.75
            )
            - jugador.defensa
        )

    # =====================================================
    # IA DEL ORCO
    # =====================================================

    def realizar_turno(
        self,
        jugador
    ):
        self.avanzar_cooldowns()

        porcentaje_orco = (
            self.vida
            / self.vida_maxima
        )

        porcentaje_jugador = (
            jugador.vida
            / jugador.vida_maxima
        )

        # =================================================
        # 1. SI PUEDE MATAR CON ATAQUE NORMAL,
        #    NO DESPERDICIA HABILIDADES.
        # =================================================

        if (
            jugador.vida
            <= self.estimar_danio_normal(
                jugador
            )
        ):
            return self.ataque_normal(
                jugador
            )

        # =================================================
        # 2. SI PUEDE REMATAR CON GOLPE BRUTAL
        # =================================================

        if (
            self._cooldown_brutal == 0
            and jugador.vida
            <= self.estimar_danio_brutal(
                jugador
            )
        ):
            return self.golpe_brutal(
                jugador
            )

        # =================================================
        # 3. CURARSE SI ESTÁ EN PELIGRO
        # =================================================

        if porcentaje_orco <= 0.25:

            if (
                self.buscar_objeto(
                    "Poción de Vida"
                )
                is not None
            ):
                return self.usar_pocion()

        # =================================================
        # 4. ACTIVAR FURIA
        # =================================================

        if (
            porcentaje_orco <= 0.40
            and not self._furia_usada
        ):
            return self.activar_furia()

        # =================================================
        # 5. USAR ESCUDO
        # =================================================

        if (
            porcentaje_orco <= 0.50
            and not self.escudo_activo
            and self.buscar_objeto(
                "Escudo Protector"
            ) is not None
        ):
            # No siempre lo hace exactamente
            # en el mismo turno.
            if random.random() < 0.70:
                return self.usar_escudo()

        # =================================================
        # 6. SI JUGADOR ESTÁ DÉBIL:
        #    PRESIONAR CON GOLPE BRUTAL
        # =================================================

        if (
            porcentaje_jugador <= 0.35
            and self._cooldown_brutal == 0
        ):
            return self.golpe_brutal(
                jugador
            )

        # =================================================
        # 7. CONTRA PERSONAJES CON BUENA DEFENSA:
        #    EMBESTIDA
        # =================================================

        if (
            jugador.defensa >= 12
            and self._cooldown_embestida == 0
            and random.random() < 0.60
        ):
            return self.embestida(
                jugador
            )

        # =================================================
        # 8. GOLPE BRUTAL OFENSIVO
        # =================================================

        if (
            self._cooldown_brutal == 0
            and random.random() < 0.45
        ):
            return self.golpe_brutal(
                jugador
            )

        # =================================================
        # 9. EMBESTIDA
        # =================================================

        if (
            self._cooldown_embestida == 0
            and random.random() < 0.35
        ):
            return self.embestida(
                jugador
            )

        # =================================================
        # 10. DEFENDERSE DE VEZ EN CUANDO
        # =================================================

        if (
            porcentaje_orco <= 0.55
            and self._ultimo_movimiento
            != "Defender"
            and random.random() < 0.25
        ):
            return self.defender()

        # =================================================
        # 11. ATAQUE NORMAL
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
        return self.golpe_brutal(
            objetivo
        )