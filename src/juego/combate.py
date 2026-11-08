class Combate:

    def __init__(self, jugador, enemigo):
        self._jugador = jugador
        self._enemigo = enemigo

        self._turno = "jugador"
        self._finalizado = False
        self._ganador = None

    # =====================================================
    # PROPIEDADES
    # =====================================================

    @property
    def jugador(self):
        return self._jugador

    @property
    def enemigo(self):
        return self._enemigo

    @property
    def turno(self):
        return self._turno

    @property
    def finalizado(self):
        return self._finalizado

    @property
    def ganador(self):
        return self._ganador

    # =====================================================
    # CONTROL DEL COMBATE
    # =====================================================

    def _actualizar_estado(self):

        if not self._enemigo.esta_vivo:
            self._finalizado = True
            self._ganador = self._jugador.nombre
            return

        if not self._jugador.esta_vivo:
            self._finalizado = True
            self._ganador = self._enemigo.nombre
            return

    def _avanzar_cooldowns(
        self,
        habilidad_usada=None
    ):
        if hasattr(
            self._jugador,
            "avanzar_cooldowns"
        ):
            self._jugador.avanzar_cooldowns(
                habilidad_usada=habilidad_usada
            )

    # =====================================================
    # ATAQUE NORMAL
    # =====================================================

    def atacar_jugador(self):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        danio = self._jugador.atacar(
            self._enemigo
        )

        resultado = {
            "accion": "Atacar",
            "danio": danio,
            "atacante": self._jugador.nombre,
            "objetivo": self._enemigo.nombre
        }

        # Una acción normal también avanza cooldowns.
        self._avanzar_cooldowns()

        self._actualizar_estado()

        if not self._finalizado:
            self._turno = "enemigo"

        return resultado

    # =====================================================
    # HABILIDADES NUEVAS
    # =====================================================

    def usar_habilidad_seleccionada(
        self,
        indice
    ):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        if not hasattr(
            self._jugador,
            "habilidades"
        ):
            return None

        habilidades = (
            self._jugador.habilidades
        )

        if indice < 0:
            return None

        if indice >= len(habilidades):
            return None

        habilidad = habilidades[indice]

        # No permite utilizar una habilidad
        # que todavía esté en cooldown.
        if not habilidad.disponible:
            return None

        resultado_habilidad = habilidad.usar(
            self._jugador,
            self._enemigo
        )

        if resultado_habilidad is None:
            return None

        resultado = {
            "accion": resultado_habilidad.get(
                "nombre",
                habilidad.nombre
            ),
            "danio": resultado_habilidad.get(
                "danio",
                0
            ),
            "atacante": self._jugador.nombre,
            "objetivo": self._enemigo.nombre
        }

        # Avanza los cooldowns de las otras
        # habilidades, pero no reduce inmediatamente
        # la habilidad que acabamos de utilizar.
        self._avanzar_cooldowns(
            habilidad_usada=habilidad
        )

        self._actualizar_estado()

        if not self._finalizado:
            self._turno = "enemigo"

        return resultado

    # =====================================================
    # HABILIDAD ANTIGUA
    # Se mantiene para compatibilidad.
    # =====================================================

    def usar_habilidad_jugador(self):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        resultado_habilidad = (
            self._jugador.usar_habilidad_especial(
                self._enemigo
            )
        )

        if resultado_habilidad is None:
            return None

        resultado = {
            "accion": resultado_habilidad.get(
                "nombre",
                "Habilidad especial"
            ),
            "danio": resultado_habilidad.get(
                "danio",
                0
            ),
            "atacante": self._jugador.nombre,
            "objetivo": self._enemigo.nombre
        }

        self._actualizar_estado()

        if not self._finalizado:
            self._turno = "enemigo"

        return resultado

    # =====================================================
    # DEFENDER
    # =====================================================

    def defender_jugador(self):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        self._jugador.defenderse()

        resultado = {
            "accion": "Defenderse",
            "atacante": self._jugador.nombre
        }

        self._avanzar_cooldowns()

        self._turno = "enemigo"

        return resultado

    # =====================================================
    # OBJETOS
    # =====================================================

    def usar_objeto_jugador(
        self,
        indice
    ):

        if self._finalizado:
            return None

        if self._turno != "jugador":
            return None

        resultado_objeto = (
            self._jugador.usar_objeto(
                indice
            )
        )

        if resultado_objeto is None:
            return None

        resultado = {
            "accion": "Usar objeto",
            "objeto": resultado_objeto.get(
                "objeto",
                "Objeto"
            ),
            "efecto": resultado_objeto.get(
                "efecto",
                ""
            ),
            "cantidad": resultado_objeto.get(
                "cantidad",
                0
            ),
            "atacante": self._jugador.nombre
        }

        self._avanzar_cooldowns()

        self._actualizar_estado()

        if not self._finalizado:
            self._turno = "enemigo"

        return resultado

    # =====================================================
    # TURNO DEL ENEMIGO
    # =====================================================

    def turno_enemigo(self):
        if self._finalizado:
            return None

        if self._turno != "enemigo":
            return None

        resultado_bruto = (
            self._enemigo.realizar_turno(
                self._jugador
            )
        )

        if resultado_bruto is None:
            return None

        # -------------------------------------------------
        # Normalizar el resultado del enemigo
        # -------------------------------------------------

        if isinstance(resultado_bruto, dict):
            resultado = resultado_bruto

        elif isinstance(resultado_bruto, tuple):
            accion = "Atacar"
            danio = 0

            # Busca el nombre de la acción
            for valor in resultado_bruto:
                if isinstance(valor, str):
                    texto = valor.lower()

                    if (
                        "ata" in texto
                        or "golpe" in texto
                        or "especial" in texto
                        or "fuerte" in texto
                    ):
                        accion = valor
                        break

            # Busca el daño
            for valor in resultado_bruto:
                if isinstance(valor, (int, float)):
                    danio = int(valor)
                    break

            resultado = {
                "accion": accion,
                "danio": danio,
                "atacante": self._enemigo.nombre,
                "objetivo": self._jugador.nombre
            }

        elif isinstance(
            resultado_bruto,
            (int, float)
        ):
            resultado = {
                "accion": "Atacar",
                "danio": int(resultado_bruto),
                "atacante": self._enemigo.nombre,
                "objetivo": self._jugador.nombre
            }

        else:
            resultado = {
                "accion": "Atacar",
                "danio": 0,
                "atacante": self._enemigo.nombre,
                "objetivo": self._jugador.nombre
            }

        # Garantiza las claves que necesita la interfaz
        resultado.setdefault(
            "accion",
            "Atacar"
        )

        resultado.setdefault(
            "danio",
            0
        )

        resultado.setdefault(
            "atacante",
            self._enemigo.nombre
        )

        resultado.setdefault(
            "objetivo",
            self._jugador.nombre
        )

        # -------------------------------------------------
        # Revisar fin del combate
        # -------------------------------------------------

        self._actualizar_estado()

        if not self._finalizado:
            self._turno = "jugador"

        return resultado