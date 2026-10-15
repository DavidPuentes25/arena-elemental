# Importa la clase base Objeto
from src.objetos.objeto import Objeto


# Escudo que protege del siguiente ataque
class EscudoProtector(Objeto):

    # Define las características del escudo
    def __init__(self):
        super().__init__(
            nombre="Escudo Protector",
            descripcion="Reduce el daño del próximo ataque"
        )

    # Activa la protección
    def usar(self, personaje):

        personaje.activar_escudo()

        return {
            "objeto": self.nombre,
            "efecto": "Protección"
        }