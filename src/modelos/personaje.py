from abc import ABC, abstractmethod


class Personaje(ABC):

    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int):
        self._nombre = nombre
        self._vida_maxima = vida
        self._vida = vida
        self._ataque = ataque
        self._defensa = defensa

        # Defensa normal
        self._defendiendo = False

        # Escudo protector
        self._turnos_escudo = 0

        # Inventario
        self._inventario = []

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
    def inventario(self):
        return self._inventario

    @property
    def turnos_escudo(self):
        return self._turnos_escudo

    @property
    def escudo_activo(self):
        return self._turnos_escudo > 0

    @property
    def esta_vivo(self):
        return self._vida > 0

    # Recibe daño y aplica las protecciones activas
    def recibir_danio(self, cantidad: int):

        # Escudo: reduce 30% durante 5 ataques
        if self._turnos_escudo > 0:

            cantidad = max(
                1,
                int(cantidad * 0.70)
            )

            self._turnos_escudo -= 1

        # Defender: reduce 50% un solo ataque
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

    # Activa defensa para el próximo ataque
    def defenderse(self):
        self._defendiendo = True

    # Recupera vida sin superar la vida máxima
    def curar(self, cantidad: int):

        self._vida = min(
            self._vida_maxima,
            self._vida + cantidad
        )

    # Calcula daño normal
    def calcular_danio(self, objetivo):

        return max(
            1,
            self._ataque - objetivo.defensa
        )

    # Ataque normal
    def atacar(self, objetivo):

        danio = self.calcular_danio(
            objetivo
        )

        danio_real = objetivo.recibir_danio(
            danio
        )

        return danio_real

    # Agrega objeto al inventario
    def agregar_objeto(self, objeto):

        self._inventario.append(
            objeto
        )

    # Usa un objeto del inventario
    def usar_objeto(self, indice: int):

        if (
            indice < 0
            or indice >= len(self._inventario)
        ):
            return None

        objeto = self._inventario[indice]

        resultado = objeto.usar(
            self
        )

        self._inventario.pop(
            indice
        )

        return resultado

    # Activa el Escudo Protector
    def activar_escudo(self, turnos=5):

        self._turnos_escudo = turnos

    @abstractmethod
    def usar_habilidad_especial(self, objetivo):
        pass