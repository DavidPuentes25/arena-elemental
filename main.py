import pygame

from src.interfaz.pantalla_inicio import PantallaInicio
from src.interfaz.pantalla_combate import PantallaCombate

from src.modelos.guerrero import Guerrero
from src.modelos.mago import Mago
from src.modelos.arquero import Arquero

from src.modelos.goblin import Goblin
from src.modelos.orco import Orco
from src.modelos.jefe_final import JefeFinal

from src.objetos.pocion_vida import PocionVida
from src.objetos.escudo_protector import EscudoProtector

from src.persistencia.base_datos import RepositorioPartida


# Crea el personaje según el guardado
def crear_personaje(tipo, nombre):

    if tipo == "Guerrero":
        return Guerrero(nombre)

    if tipo == "Mago":
        return Mago(nombre)

    if tipo == "Arquero":
        return Arquero(nombre)

    raise ValueError(
        f"Personaje desconocido: {tipo}"
    )


# Crea el enemigo correspondiente
def crear_enemigo(nombre):

    if nombre == "Goblin":
        return Goblin()

    if nombre == "Orco":
        return Orco()

    if nombre == "Guardián Elemental":
        return JefeFinal()

    raise ValueError(
        f"Enemigo desconocido: {nombre}"
    )


# Recupera los objetos almacenados
def cargar_inventario(jugador, inventario):

    cantidad_pociones = inventario.get(
        "Poción de Vida",
        0
    )

    cantidad_escudos = inventario.get(
        "Escudo Protector",
        0
    )

    for _ in range(cantidad_pociones):
        jugador.agregar_objeto(
            PocionVida()
        )

    for _ in range(cantidad_escudos):
        jugador.agregar_objeto(
            EscudoProtector()
        )


# Crea una partida nueva
def iniciar_nueva_partida():

    # Temporal hasta crear selección
    jugador = Guerrero("Ares")

    # Objeto inicial
    jugador.agregar_objeto(
        PocionVida()
    )

    enemigo = Goblin()

    pantalla = PantallaCombate(
        jugador,
        enemigo
    )

    pantalla.ejecutar()


# Recupera una partida desde SQLite
def continuar_partida(repo):

    datos = repo.cargar()

    if datos is None:
        return

    # Reconstruye al personaje
    jugador = crear_personaje(
        datos["personaje"],
        datos["nombre"]
    )

    # Recupera inventario
    cargar_inventario(
        jugador,
        datos["inventario"]
    )

    # Recupera el siguiente enemigo
    enemigo = crear_enemigo(
        datos["siguiente_enemigo"]
    )

    pantalla = PantallaCombate(
        jugador,
        enemigo
    )

    pantalla.ejecutar()


def main():

    repo = RepositorioPartida()

    try:

        while True:

            # Comprueba si hay guardado
            hay_partida = repo.existe_partida()

            menu = PantallaInicio(
                partida_disponible=hay_partida
            )

            opcion = menu.ejecutar()

            if opcion == "jugar":
                iniciar_nueva_partida()

            elif opcion == "cargar":
                continuar_partida(repo)

            elif opcion == "salir":
                break

    finally:
        repo.cerrar()
        pygame.quit()


if __name__ == "__main__":
    main()