import unittest

from src.modelos.guerrero import Guerrero
from src.modelos.goblin import Goblin
from src.objetos.pocion_vida import PocionVida
from src.objetos.escudo_protector import EscudoProtector
from src.juego.combate import Combate


class TestObjetosCombate(unittest.TestCase):

    def test_inventario(self):
        jugador = Guerrero("Ares")

        jugador.agregar_objeto(PocionVida())
        jugador.agregar_objeto(EscudoProtector())

        self.assertEqual(len(jugador.inventario), 2)

    def test_pocion(self):
        jugador = Guerrero("Ares")

        jugador.recibir_danio(50)
        jugador.agregar_objeto(PocionVida())

        resultado = jugador.usar_objeto(0)

        self.assertEqual(jugador.vida, 100)
        self.assertEqual(resultado["cantidad"], 30)
        self.assertEqual(len(jugador.inventario), 0)

    def test_escudo(self):
        jugador = Guerrero("Ares")

        jugador.agregar_objeto(EscudoProtector())
        jugador.usar_objeto(0)

        danio = jugador.recibir_danio(20)

        self.assertEqual(danio, 10)
        self.assertEqual(jugador.vida, 110)

    def test_defensa(self):
        jugador = Guerrero("Ares")
        enemigo = Goblin()

        combate = Combate(jugador, enemigo)

        combate.defender_jugador()
        resultado = combate.turno_enemigo()

        self.assertEqual(resultado["danio"], 1)
        self.assertEqual(jugador.vida, 119)

    def test_pocion_desde_combate(self):
        jugador = Guerrero("Ares")
        enemigo = Goblin()

        jugador.recibir_danio(50)
        jugador.agregar_objeto(PocionVida())

        combate = Combate(jugador, enemigo)

        resultado = combate.usar_objeto_jugador(0)

        self.assertEqual(jugador.vida, 100)
        self.assertEqual(len(jugador.inventario), 0)
        self.assertEqual(combate.turno, "enemigo")
        self.assertEqual(resultado["objeto"], "Poción de Vida")


if __name__ == "__main__":
    unittest.main()