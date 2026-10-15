# Coordina el combate entre jugador y enemigo
class Combate:

    # Recibe los participantes del combate
    def __init__(self, jugador, enemigo):
        self._jugador = jugador
        self._enemigo = enemigo

        # El jugador inicia el combate
        self._turno = "jugador"

        # Estado inicial
        self._finalizado = False
        self._ganador = None

    # Permite consultar el turno actual
    @property
    def turno(self):
        return self._turno

    # Indica si el combate terminó
    @property
    def finalizado(self):
        return self._finalizado

    # Permite consultar quién ganó
    @property
    def ganador(self):
        return self._ganador

    # Ejecuta un ataque normal del jugador
    def atacar_jugador(self):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        danio = self._jugador.atacar(
            self._enemigo
        )

        self._actualizar_estado()

        if not self._finalizado:
            self._turno = "enemigo"

        return {
            "accion": "Ataque normal",
            "danio": danio,
            "atacante": self._jugador.nombre,
            "objetivo": self._enemigo.nombre
        }

    # Ejecuta la habilidad especial del jugador
    def usar_habilidad_jugador(self):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        resultado = (
            self._jugador.usar_habilidad_especial(
                self._enemigo
            )
        )

        self._actualizar_estado()

        if not self._finalizado:
            self._turno = "enemigo"

        return {
            "accion": resultado["nombre"],
            "danio": resultado["danio"],
            "atacante": self._jugador.nombre,
            "objetivo": self._enemigo.nombre
        }

    # Permite al jugador defenderse
    def defender_jugador(self):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        self._jugador.defenderse()

        self._turno = "enemigo"

        return {
            "accion": "Defenderse",
            "atacante": self._jugador.nombre
        }

    # Permite utilizar un objeto
    def usar_objeto_jugador(self, indice: int):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        resultado = self._jugador.usar_objeto(
            indice
        )

        # Valida que exista el objeto
        if resultado is None:
            return None

        self._turno = "enemigo"

        return {
            "accion": "Usar objeto",
            "objeto": resultado["objeto"],
            "efecto": resultado["efecto"],
            "cantidad": resultado.get(
                "cantidad",
                0
            ),
            "atacante": self._jugador.nombre
        }

    # Ejecuta automáticamente el turno enemigo
    def turno_enemigo(self):

        if self._finalizado:
            return None

        if self._turno != "enemigo":
            return None

        danio, accion = (
            self._enemigo.realizar_turno(
                self._jugador
            )
        )

        self._actualizar_estado()

        if not self._finalizado:
            self._turno = "jugador"

        return {
            "accion": accion,
            "danio": danio,
            "atacante": self._enemigo.nombre,
            "objetivo": self._jugador.nombre
        }

    # Verifica si alguno fue derrotado
    def _actualizar_estado(self):

        # Victoria del jugador
        if not self._enemigo.esta_vivo:
            self._finalizado = True
            self._ganador = self._jugador.nombre

        # Derrota del jugador
        elif not self._jugador.esta_vivo:
            self._finalizado = True
            self._ganador = self._enemigo.nombre