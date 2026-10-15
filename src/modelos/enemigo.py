# Permite crear clases y métodos abstractos
from abc import ABC, abstractmethod


# Clase base para todos los enemigos
class Enemigo(ABC):

    # Inicializa las estadísticas principales del enemigo
    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int):
        self._nombre = nombre
        self._vida_maxima = vida
        self._vida = vida
        self._ataque = ataque
        self._defensa = defensa

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

    # Indica si el enemigo sigue vivo
    @property
    def esta_vivo(self):
        return self._vida > 0

    # Reduce la vida sin permitir valores menores a 0
    def recibir_danio(self, cantidad: int):
        self._vida = max(0, self._vida - cantidad)

        return cantidad

    # Calcula el daño según ataque y defensa
    def calcular_danio(self, objetivo):
        return max(1, self._ataque - objetivo.defensa)

    # Ejecuta un ataque normal
    def atacar(self, objetivo):
        danio = self.calcular_danio(objetivo)

        # Obtiene el daño realmente aplicado
        danio_real = objetivo.recibir_danio(danio)

        return danio_real

    # Cada enemigo tendrá su propio comportamiento
    @abstractmethod
    def realizar_turno(self, objetivo):
        pass