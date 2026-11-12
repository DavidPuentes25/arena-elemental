from abc import ABC, abstractmethod


class Personaje(ABC):

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

        # ==========================================
        # NIVEL Y EXPERIENCIA
        # ==========================================

        self._nivel = 1
        self._experiencia = 0

        # ==========================================
        # ESTADOS DE COMBATE
        # ==========================================

        self._defendiendo = False

        self._turnos_escudo = 0

        # ==========================================
        # INVENTARIO
        # ==========================================

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

    # =====================================================
    # NIVEL Y EXPERIENCIA
    # =====================================================

    @property
    def nivel(self):
        return self._nivel

    @property
    def experiencia(self):
        return self._experiencia

    @property
    def experiencia_siguiente_nivel(self):
        return self._nivel * 100

    def obtener_mejoras_nivel(self):
        """
        Estadísticas que obtiene cada clase
        cuando sube de nivel.
        """

        tipo = self.__class__.__name__

        if tipo == "Guerrero":
            return {
                "vida": 20,
                "ataque": 4,
                "defensa": 3
            }

        if tipo == "Mago":
            return {
                "vida": 15,
                "ataque": 5,
                "defensa": 2
            }

        if tipo == "Arquero":
            return {
                "vida": 15,
                "ataque": 4,
                "defensa": 2
            }

        return {
            "vida": 10,
            "ataque": 3,
            "defensa": 2
        }

    def ganar_experiencia(
        self,
        cantidad
    ):
        if cantidad <= 0:
            return []

        self._experiencia += cantidad

        niveles_subidos = []

        while (
            self._experiencia
            >= self.experiencia_siguiente_nivel
        ):

            experiencia_necesaria = (
                self.experiencia_siguiente_nivel
            )

            self._experiencia -= (
                experiencia_necesaria
            )

            resultado = (
                self.subir_nivel()
            )

            niveles_subidos.append(
                resultado
            )

        return niveles_subidos

    def subir_nivel(self):

        self._nivel += 1

        mejoras = (
            self.obtener_mejoras_nivel()
        )

        self._vida_maxima += (
            mejoras["vida"]
        )

        self._ataque += (
            mejoras["ataque"]
        )

        self._defensa += (
            mejoras["defensa"]
        )

        # Subir de nivel recupera la vida completa.
        self._vida = (
            self._vida_maxima
        )

        return {
            "nivel": self._nivel,
            "vida": mejoras["vida"],
            "ataque": mejoras["ataque"],
            "defensa": mejoras["defensa"]
        }

    def restaurar_progreso(
        self,
        nivel,
        experiencia
    ):
        """
        Reconstruye las estadísticas cuando
        cargamos una partida guardada.
        """

        nivel = max(
            1,
            int(nivel)
        )

        experiencia = max(
            0,
            int(experiencia)
        )

        while self._nivel < nivel:
            self.subir_nivel()

        self._experiencia = (
            experiencia
        )

        self._vida = (
            self._vida_maxima
        )

    # =====================================================
    # COMBATE
    # =====================================================

    def recibir_danio(
        self,
        cantidad
    ):
        if self._turnos_escudo > 0:

            cantidad = max(
                1,
                int(cantidad * 0.70)
            )

            self._turnos_escudo -= 1

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

    def defenderse(self):
        self._defendiendo = True

    def curar(
        self,
        cantidad
    ):
        self._vida = min(
            self._vida_maxima,
            self._vida + cantidad
        )

    def restaurar_vida(self):
        self._vida = self._vida_maxima

    def calcular_danio(
        self,
        objetivo
    ):
        return max(
            1,
            self._ataque - objetivo.defensa
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

    def activar_escudo(
        self,
        turnos=5
    ):
        self._turnos_escudo = (
            turnos
        )

    # =====================================================
    # MÉTODO ABSTRACTO
    # =====================================================

    @abstractmethod
    def usar_habilidad_especial(
        self,
        objetivo
    ):
        pass