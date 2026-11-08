from abc import ABC, abstractmethod


class Enemigo(ABC):

    def __init__(
        self,
        nombre,
        vida,
        ataque,
        defensa
    ):
        self._nombre = nombre

        self._vida_maxima = vida
        self._vida = vida

        self._ataque = ataque
        self._defensa = defensa

        # Defensa normal
        self._defendiendo = False

        # Escudo Protector
        self._turnos_escudo = 0

        # Inventario del enemigo
        self._inventario = []

    # =====================================================
    # PROPIEDADES
    # =====================================================

    @property
    def nombre(self):
        return self._nombre

    @property
    def vida(self):
        return self._vida

    @property
    def vida_maxima(self):
        return self._vida_maxima

    @property
    def ataque(self):
        return self._ataque

    @property
    def defensa(self):
        return self._defensa

    @property
    def esta_vivo(self):
        return self._vida > 0

    @property
    def inventario(self):
        return self._inventario

    @property
    def turnos_escudo(self):
        return self._turnos_escudo

    @property
    def escudo_activo(self):
        return self._turnos_escudo > 0

    # =====================================================
    # RECIBIR DAÑO
    # =====================================================

    def recibir_danio(
        self,
        cantidad
    ):
        # Escudo Protector:
        # reduce 30% durante varios ataques.
        if self._turnos_escudo > 0:

            cantidad = max(
                1,
                int(cantidad * 0.70)
            )

            self._turnos_escudo -= 1

        # Defensa normal:
        # reduce 50% el próximo golpe.
        if self._defendiendo:

            cantidad = max(
                1,
                cantidad // 2
            )

            self._defendiendo = False

        self._vida = max(
            0,
            self._vida - cantidad
        )

        return cantidad

    # =====================================================
    # DEFENDERSE
    # =====================================================

    def defenderse(self):
        self._defendiendo = True

    # =====================================================
    # CURACIÓN
    # =====================================================

    def curar(
        self,
        cantidad
    ):
        self._vida = min(
            self._vida_maxima,
            self._vida + cantidad
        )

    # =====================================================
    # ATAQUE
    # =====================================================

    def calcular_danio(
        self,
        objetivo
    ):
        return max(
            1,
            self._ataque
            - objetivo.defensa
        )

    def atacar(
        self,
        objetivo
    ):
        danio = self.calcular_danio(
            objetivo
        )

        return objetivo.recibir_danio(
            danio
        )

    # =====================================================
    # INVENTARIO
    # =====================================================

    def agregar_objeto(
        self,
        objeto
    ):
        self._inventario.append(
            objeto
        )

    def usar_objeto(
        self,
        indice
    ):
        if (
            indice < 0
            or indice >= len(
                self._inventario
            )
        ):
            return None

        objeto = self._inventario[
            indice
        ]

        resultado = objeto.usar(
            self
        )

        self._inventario.pop(
            indice
        )

        return resultado

    # =====================================================
    # ESCUDO
    # =====================================================

    def activar_escudo(
        self,
        turnos=5
    ):
        self._turnos_escudo = turnos

    # =====================================================
    # TURNO DEL ENEMIGO
    # =====================================================

    @abstractmethod
    def realizar_turno(
        self,
        jugador
    ):
        pass