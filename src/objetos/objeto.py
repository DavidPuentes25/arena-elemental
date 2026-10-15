# Permite crear clases abstractas
from abc import ABC, abstractmethod


# Clase base para todos los objetos
class Objeto(ABC):

    # Inicializa los datos principales
    def __init__(self, nombre: str, descripcion: str):
        self._nombre = nombre
        self._descripcion = descripcion

    # Permite consultar el nombre
    @property
    def nombre(self):
        return self._nombre

    # Permite consultar la descripción
    @property
    def descripcion(self):
        return self._descripcion

    # Cada objeto tendrá un efecto diferente
    @abstractmethod
    def usar(self, personaje):
        pass