import pygame

from src.interfaz.pantalla_inicio import PantallaInicio
from src.interfaz.pantalla_combate import PantallaCombate

from src.modelos.guerrero import Guerrero
from src.modelos.mago import Mago
from src.modelos.arquero import Arquero

from src.modelos.goblin import Goblin
from src.modelos.orco import Orco
from src.modelos.jefe_final import JefeFinal
from src.objetos.escudo_protector import EscudoProtector
from src.objetos.pocion_vida import PocionVida
from src.objetos.escudo_protector import EscudoProtector
from src.interfaz.pantalla_resultado import PantallaResultado
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

    # Crear jugador
    jugador = Guerrero("Ares")

    # Objetos temporales para probar el inventario
    jugador.agregar_objeto(
        PocionVida()
    )

    jugador.agregar_objeto(
        EscudoProtector()
    )

    # Primer enemigo
    enemigo = Goblin()

    # Iniciar combate
    pantalla = PantallaCombate(
        jugador,
        enemigo
    )

    resultado = pantalla.ejecutar()

    # Victoria
    if resultado == "victoria":

        pantalla_resultado = PantallaResultado(
            "victoria"
        )

        return pantalla_resultado.ejecutar()

    # Derrota
    elif resultado == "derrota":

        pantalla_resultado = PantallaResultado(
            "derrota"
        )

        return pantalla_resultado.ejecutar()

    return "salir"

# Recupera una partida desde SQLite
def continuar_partida(repo):

    datos = repo.cargar()

    if datos is None:
        return "menu"

    jugador = crear_personaje(
        datos["personaje"],
        datos["nombre"]
    )

    cargar_inventario(
        jugador,
        datos["inventario"]
    )

    enemigo = crear_enemigo(
        datos["siguiente_enemigo"]
    )

    pantalla = PantallaCombate(
        jugador,
        enemigo
    )

    resultado = pantalla.ejecutar()

    if resultado == "victoria":
        pantalla_resultado = PantallaResultado(
            "victoria"
        )
        return pantalla_resultado.ejecutar()

    elif resultado == "derrota":
        pantalla_resultado = PantallaResultado(
            "derrota"
        )
        return pantalla_resultado.ejecutar()

    return "salir"


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
                accion = iniciar_nueva_partida()

                if accion == "salir":
                   break

            elif opcion == "cargar":
                accion = continuar_partida(repo)

                if accion == "salir":
                 break

            elif opcion == "salir":
                break

    finally:
        repo.cerrar()
        pygame.quit()


if __name__ == "__main__":
    main()