from src.objetos.objeto import Objeto


class EscudoProtector(Objeto):

    def __init__(self):

        super().__init__(
            nombre="Escudo Protector",
            descripcion=(
                "Reduce un 30% el daño recibido "
                "durante 5 ataques enemigos"
            )
        )

    def usar(self, personaje):

        personaje.activar_escudo(
            5
        )

        return {
            "objeto": self.nombre,
            "efecto": "Protección",
            "reduccion": 30,
            "turnos": 5
        }