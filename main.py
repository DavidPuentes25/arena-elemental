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
from src.interfaz.pantalla_recompensa import PantallaRecompensa
from src.interfaz.pantalla_progreso import PantallaProgreso
from src.interfaz.pantalla_nombre_partida import PantallaNombrePartida
from src.interfaz.pantalla_cargar_partida import PantallaCargarPartida
from src.interfaz.pantalla_seleccion_personaje import (PantallaSeleccionPersonaje)
# Crea el personaje según el guardado
def crear_personaje(
    tipo,
    nombre
):

    if tipo == "Guerrero":
        return Guerrero(nombre)

    if tipo == "Mago":
        return Mago(nombre)

    if tipo == "Arquero":
        return Arquero(nombre)

    raise ValueError(
        f"Personaje desconocido: {tipo}"
    )
def obtener_tipo_personaje(
    jugador
):
    tipo = jugador.__class__.__name__

    if tipo not in (
        "Guerrero",
        "Mago",
        "Arquero"
    ):
        raise ValueError(
            f"Tipo de personaje no válido: {tipo}"
        )

    return tipo
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
def guardar_partida_desde_mapa(
    repo,
    partida_id,
    nombre_partida,
    jugador,
    siguiente_enemigo,
    progreso
):
    inventario = (
        obtener_inventario_para_guardar(
            jugador
        )
    )

    # Primera vez que se guarda
    if partida_id is None:

        nombre = (
            PantallaNombrePartida()
            .ejecutar()
        )

        # Canceló el guardado
        if nombre is None:
            return (
                partida_id,
                nombre_partida
            )

        try:
            partida_id = repo.crear_partida(
                nombre_partida=nombre,
                nombre_jugador=jugador.nombre,
                personaje=obtener_tipo_personaje(jugador),
                siguiente_enemigo=siguiente_enemigo,
                progreso=progreso,
                inventario=inventario
            )

            nombre_partida = nombre

            print(
                f"Partida guardada: "
                f"{nombre_partida}"
            )

        except ValueError as error:
            print(
                f"No se pudo guardar: "
                f"{error}"
            )

    # Ya existe: actualizar
    else:

        repo.actualizar_partida(
            partida_id=partida_id,
            nombre_jugador=jugador.nombre,
            personaje=obtener_tipo_personaje(jugador),
            siguiente_enemigo=siguiente_enemigo,
            progreso=progreso,
            inventario=inventario
        )

        print(
            f"Progreso actualizado: "
            f"{nombre_partida}"
        )

    return (
        partida_id,
        nombre_partida
    )


def ejecutar_mapa(
    repo,
    estado,
    jugador,
    siguiente_enemigo,
    progreso,
    partida_id=None,
    nombre_partida=None
):
    while True:

        accion = PantallaProgreso(
            estado,
            partida_guardada=(
                partida_id is not None
            )
        ).ejecutar()

        # Volver al menú principal
        if accion == "menu":
            return (
                "menu",
                partida_id,
                nombre_partida
            )

        # Cerrar completamente el juego
        if accion == "salir":
            return (
                "salir",
                partida_id,
                nombre_partida
            )

        # Continuar hacia el combate
        if accion == "continuar":
            return (
                "continuar",
                partida_id,
                nombre_partida
            )

        # Guardar partida o progreso
        if accion == "guardar":

            (
                partida_id,
                nombre_partida
            ) = guardar_partida_desde_mapa(
                repo=repo,
                partida_id=partida_id,
                nombre_partida=nombre_partida,
                jugador=jugador,
                siguiente_enemigo=siguiente_enemigo,
                progreso=progreso
            )
# ============================================================
# COMBATE CONTRA GOBLIN
# ============================================================

def combatir_goblin(
    repo,
    jugador,
    partida_id=None,
    nombre_partida=None
):
    enemigo = Goblin()

    resultado = PantallaCombate(
        jugador,
        enemigo
    ).ejecutar()

    # ==========================================
    # CERRAR JUEGO
    # ==========================================

    if resultado == "salir":
        return "salir"

    # ==========================================
    # DERROTA
    # ==========================================

    if resultado == "derrota":

        if partida_id is not None:
            repo.eliminar(
                partida_id
            )

        accion = PantallaResultado(
            "derrota"
        ).ejecutar()

        if accion == "salir":
            return "salir"

        return "menu"

    # ==========================================
    # VICTORIA
    # ==========================================

    if resultado == "victoria":

        accion = PantallaResultado(
            "victoria"
        ).ejecutar()

        if accion == "salir":
            return "salir"

        if accion == "menu":
            return "menu"

        # ======================================
        # RECOMPENSA
        # ======================================

        recompensa = PantallaRecompensa(
        ).ejecutar()

        if recompensa == "salir":
            return "salir"

        if recompensa == "pocion":

            jugador.agregar_objeto(
                PocionVida()
            )

        elif recompensa == "escudo":

            jugador.agregar_objeto(
                EscudoProtector()
            )

        # ======================================
        # MAPA DESPUÉS DEL GOBLIN
        # ======================================

        (
            accion_mapa,
            partida_id,
            nombre_partida
        ) = ejecutar_mapa(
            repo=repo,
            estado="goblin",
            jugador=jugador,
            siguiente_enemigo="Orco",
            progreso=1,
            partida_id=partida_id,
            nombre_partida=nombre_partida
        )

        # --------------------------------------
        # VOLVER AL MENÚ
        # --------------------------------------

        if accion_mapa == "menu":
            return "menu"

        # --------------------------------------
        # CERRAR JUEGO
        # --------------------------------------

        if accion_mapa == "salir":
            return "salir"

        # --------------------------------------
        # SOLO SI PULSA ENFRENTAR ORCO
        # --------------------------------------

        if accion_mapa == "continuar":

            return combatir_orco(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

    return "menu"

# ============================================================
# COMBATE CONTRA ORCO
# ============================================================

def combatir_orco(
    repo,
    jugador,
    partida_id=None,
    nombre_partida=None
):
    enemigo = Orco()

    resultado = PantallaCombate(
        jugador,
        enemigo
    ).ejecutar()

    # ==========================================
    # CERRAR JUEGO
    # ==========================================

    if resultado == "salir":
        return "salir"

    # ==========================================
    # DERROTA
    # ==========================================

    if resultado == "derrota":

        if partida_id is not None:
            repo.eliminar(
                partida_id
            )

        accion = PantallaResultado(
            "derrota"
        ).ejecutar()

        if accion == "salir":
            return "salir"

        return "menu"

    # ==========================================
    # VICTORIA
    # ==========================================

    if resultado == "victoria":

        # --------------------------------------
        # PANTALLA DE VICTORIA
        # --------------------------------------

        accion = PantallaResultado(
            "victoria"
        ).ejecutar()

        if accion == "salir":
            return "salir"

        if accion == "menu":
            return "menu"

        # --------------------------------------
        # RECOMPENSA
        # --------------------------------------

        recompensa = (
            PantallaRecompensa()
            .ejecutar()
        )

        if recompensa == "salir":
            return "salir"

        if recompensa == "pocion":

            jugador.agregar_objeto(
                PocionVida()
            )

        elif recompensa == "escudo":

            jugador.agregar_objeto(
                EscudoProtector()
            )

        # --------------------------------------
        # MAPA:
        # GOBLIN Y ORCO DERROTADOS
        # --------------------------------------

        (
            accion_mapa,
            partida_id,
            nombre_partida
        ) = ejecutar_mapa(
            repo=repo,
            estado="orco",
            jugador=jugador,
            siguiente_enemigo="Guardián Elemental",
            progreso=2,
            partida_id=partida_id,
            nombre_partida=nombre_partida
        )

        # --------------------------------------
        # VOLVER AL INICIO
        # --------------------------------------

        if accion_mapa == "menu":
            return "menu"

        # --------------------------------------
        # CERRAR
        # --------------------------------------

        if accion_mapa == "salir":
            return "salir"

        # --------------------------------------
        # GUARDIÁN
        # --------------------------------------

        if accion_mapa == "continuar":

            return combatir_guardian(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

    return "menu"
# Crea una partida nueva
def iniciar_nueva_partida(repo):

    # ==========================================
    # SELECCIONAR PERSONAJE
    # ==========================================

    seleccion = (
        PantallaSeleccionPersonaje()
        .ejecutar()
    )

    if seleccion == "salir":
        return "salir"

    if seleccion == "menu":
        return "menu"

    # ==========================================
    # CREAR PERSONAJE
    # ==========================================

    jugador = crear_personaje(
        seleccion,
        "Ares"
    )

    partida_id = None
    nombre_partida = None

    # ==========================================
    # MAPA INICIAL
    # ==========================================

    (
        accion,
        partida_id,
        nombre_partida
    ) = ejecutar_mapa(
        repo=repo,
        estado="inicio",
        jugador=jugador,
        siguiente_enemigo="Goblin",
        progreso=0,
        partida_id=partida_id,
        nombre_partida=nombre_partida
    )

    if accion == "menu":
        return "menu"

    if accion == "salir":
        return "salir"

    if accion == "continuar":

        return combatir_goblin(
            repo=repo,
            jugador=jugador,
            partida_id=partida_id,
            nombre_partida=nombre_partida
        )

    return "menu"
def continuar_partida(repo):

    # ==========================================
    # SELECCIÓN / ELIMINACIÓN
    # ==========================================

    while True:

        partidas = repo.listar_partidas()

        if not partidas:
            print("No hay partidas guardadas.")
            return "menu"

        (
            accion_partida,
            partida_id
        ) = PantallaCargarPartida(
            partidas
        ).ejecutar()

        # Cerrar juego
        if accion_partida == "salir":
            return "salir"

        # Volver al menú
        if accion_partida == "volver":
            return "menu"

        # Eliminar partida
        if accion_partida == "eliminar":

            repo.eliminar(
                partida_id
            )

            print(
                f"Partida {partida_id} eliminada."
            )

            # Vuelve a cargar la lista
            continue

        # Cargar partida
        if accion_partida == "cargar":
            break

    # ==========================================
    # CARGAR DATOS
    # ==========================================

    datos = repo.cargar(
        partida_id
    )

    if datos is None:
        print("No se pudo cargar la partida.")
        return "menu"

    # ==========================================
    # RECONSTRUIR JUGADOR
    # ==========================================

    jugador = crear_personaje(
        datos["personaje"],
        datos["nombre_jugador"]
    )

    cargar_inventario(
        jugador,
        datos["inventario"]
    )

    nombre_partida = datos[
        "nombre_partida"
    ]

    siguiente_enemigo = datos[
        "siguiente_enemigo"
    ]

    progreso = datos[
        "progreso"
    ]

    # ==========================================
    # MAPA
    # ==========================================

    if siguiente_enemigo == "Goblin":
        estado_mapa = "inicio"

    elif siguiente_enemigo == "Orco":
        estado_mapa = "goblin"

    else:
        print(
            "Ese punto del juego todavía "
            "no está implementado."
        )
        return "menu"

    (
        accion,
        partida_id,
        nombre_partida
    ) = ejecutar_mapa(
        repo=repo,
        estado=estado_mapa,
        jugador=jugador,
        siguiente_enemigo=siguiente_enemigo,
        progreso=progreso,
        partida_id=partida_id,
        nombre_partida=nombre_partida
    )

    # ==========================================
    # VOLVER AL INICIO
    # ==========================================

    if accion == "menu":
        return "menu"

    # ==========================================
    # CERRAR
    # ==========================================

    if accion == "salir":
        return "salir"

    # ==========================================
    # COMBATE
    # ==========================================

    if accion == "continuar":

        if siguiente_enemigo == "Goblin":

            return combatir_goblin(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

        if siguiente_enemigo == "Orco":

            return combatir_orco(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

        if siguiente_enemigo == "Guardián Elemental":

           return combatir_guardian(
             repo=repo,
             jugador=jugador,
             partida_id=partida_id,
             nombre_partida=nombre_partida
            )

    return "menu"
def obtener_inventario_para_guardar(jugador):
    inventario = {}

    for objeto in jugador.inventario:

        if objeto.nombre not in inventario:
            inventario[objeto.nombre] = 0

        inventario[objeto.nombre] += 1

    return inventario


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
                accion = iniciar_nueva_partida(repo)

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