from src.modelos.guerrero import Guerrero
from src.modelos.goblin import Goblin

from src.objetos.pocion_vida import PocionVida

from src.interfaz.pantalla_combate import PantallaCombate


jugador = Guerrero("Ares")

jugador.agregar_objeto(
    PocionVida()
)

enemigo = Goblin()

pantalla = PantallaCombate(
    jugador,
    enemigo
)

pantalla.ejecutar()