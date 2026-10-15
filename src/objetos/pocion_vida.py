# Importa la clase base Objeto
from src.objetos.objeto import Objeto


# Poción que recupera puntos de vida
class PocionVida(Objeto):

    # Define las características de la poción
    def __init__(self):
        super().__init__(
            nombre="Poción de Vida",
            descripcion="Recupera 30 puntos de vida"
        )

        self._curacion = 30

    # Aplica el efecto de la poción
    def usar(self, personaje):

        # Guarda la vida antes de curar
        vida_anterior = personaje.vida

        # Recupera puntos de vida
        personaje.curar(self._curacion)

        # Calcula la vida realmente recuperada
        recuperado = personaje.vida - vida_anterior

        return {
            "objeto": self.nombre,
            "efecto": "Curación",
            "cantidad": recuperado
        }