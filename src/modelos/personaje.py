# Permite crear clases y métodos abstractos
from abc import ABC, abstractmethod


# Clase base para todos los personajes jugables
class Personaje(ABC):

    # Inicializa las estadísticas principales del personaje
    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int):
        self._nombre = nombre
        self._vida_maxima = vida
        self._vida = vida
        self._ataque = ataque
        self._defensa = defensa
        self._defendiendo = False
        self._escudo_activo = False
        self._inventario = []

    # Permite consultar el nombre
    @property
    def nombre(self):
        return self._nombre

    # Permite consultar la vida actual
    @property
    def vida(self):
        return self._vida

    # Permite consultar la vida máxima
    @property
    def vida_maxima(self):
        return self._vida_maxima

    # Permite consultar el ataque
    @property
    def ataque(self):
        return self._ataque

    # Permite consultar la defensa
    @property
    def defensa(self):
        return self._defensa

    # Permite consultar el inventario
    @property
    def inventario(self):
        return self._inventario

    # Indica si el personaje sigue vivo
    @property
    def esta_vivo(self):
        return self._vida > 0

    # Reduce la vida según el daño recibido
    def recibir_danio(self, cantidad: int):

        # El escudo reduce el siguiente daño
        if self._escudo_activo:
            cantidad = max(1, cantidad // 2)
            self._escudo_activo = False

        # Defenderse reduce el siguiente daño
        elif self._defendiendo:
            cantidad = max(1, cantidad // 2)
            self._defendiendo = False

        self._vida = max(0, self._vida - cantidad)

        return cantidad

    # Activa la defensa para el próximo ataque
    def defenderse(self):
        self._defendiendo = True

    # Recupera vida sin superar la vida máxima
    def curar(self, cantidad: int):
        self._vida = min(
            self._vida_maxima,
            self._vida + cantidad
        )

    # Calcula el daño según ataque y defensa
    def calcular_danio(self, objetivo):
        return max(1, self._ataque - objetivo.defensa)

    # Ejecuta un ataque contra otro personaje
    def atacar(self, objetivo):
        danio = self.calcular_danio(objetivo)

        # Obtiene el daño realmente aplicado
        danio_real = objetivo.recibir_danio(danio)

        return danio_real

    # Agrega un objeto al inventario
    def agregar_objeto(self, objeto):
        self._inventario.append(objeto)

    # Utiliza y consume un objeto
    def usar_objeto(self, indice: int):

        # Valida que el objeto exista
        if indice < 0 or indice >= len(self._inventario):
            return None

        objeto = self._inventario[indice]

        # Ejecuta el efecto
        resultado = objeto.usar(self)

        # Consume el objeto
        self._inventario.pop(indice)

        return resultado

    # Activa el escudo para el próximo ataque
    def activar_escudo(self):
        self._escudo_activo = True

    # Cada personaje tendrá su propia habilidad
    @abstractmethod
    def usar_habilidad_especial(self, objetivo):
        pass