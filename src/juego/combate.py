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

        # Evita acciones después de finalizar
        if self._finalizado:
            return None

        # Valida el turno
        if self._turno != "jugador":
            return None

        # Ejecuta el ataque
        danio = self._jugador.atacar(self._enemigo)

        # Verifica victoria o derrota
        self._actualizar_estado()

        # Cambia el turno
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

        # Evita acciones después de finalizar
        if self._finalizado:
            return None

        # Valida el turno
        if self._turno != "jugador":
            return None

        # Ejecuta la habilidad
        resultado = self._jugador.usar_habilidad_especial(
            self._enemigo
        )

        # Verifica victoria o derrota
        self._actualizar_estado()

        # Cambia el turno
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

        # Evita acciones después de finalizar
        if self._finalizado:
            return None

        # Valida el turno
        if self._turno != "jugador":
            return None

        # Activa la defensa
        self._jugador.defenderse()

        # Cambia al turno enemigo
        self._turno = "enemigo"

        return {
            "accion": "Defenderse",
            "atacante": self._jugador.nombre
        }

    # Ejecuta automáticamente el turno enemigo
    def turno_enemigo(self):

        # Evita acciones después de finalizar
        if self._finalizado:
            return None

        # Valida el turno
        if self._turno != "enemigo":
            return None

        # El enemigo decide su acción
        danio, accion = self._enemigo.realizar_turno(
            self._jugador
        )

        # Verifica victoria o derrota
        self._actualizar_estado()

        # Devuelve el turno al jugador
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