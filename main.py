import pygame

# ============================================================
# INTERFAZ
# ============================================================

from src.interfaz.pantalla_inicio import PantallaInicio
from src.interfaz.pantalla_combate import PantallaCombate
from src.interfaz.pantalla_resultado import PantallaResultado
from src.interfaz.pantalla_recompensa import PantallaRecompensa
from src.interfaz.pantalla_progreso import PantallaProgreso
from src.interfaz.pantalla_nombre_partida import PantallaNombrePartida
from src.interfaz.pantalla_cargar_partida import PantallaCargarPartida
from src.interfaz.pantalla_seleccion_personaje import (
    PantallaSeleccionPersonaje
)
from src.interfaz.pantalla_victoria_final import (
    PantallaVictoriaFinal
)

# ============================================================
# PERSONAJES
# ============================================================

from src.modelos.guerrero import Guerrero
from src.modelos.mago import Mago
from src.modelos.arquero import Arquero

# ============================================================
# ENEMIGOS
# ============================================================

from src.modelos.goblin import Goblin
from src.modelos.orco import Orco
from src.modelos.jefe_final import JefeFinal

# ============================================================
# OBJETOS
# ============================================================

from src.objetos.pocion_vida import PocionVida
from src.objetos.escudo_protector import EscudoProtector

# ============================================================
# BASE DE DATOS
# ============================================================

from src.persistencia.base_datos import RepositorioPartida


# ============================================================
# CREAR PERSONAJE
# ============================================================

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


# ============================================================
# TIPO DE PERSONAJE
# ============================================================

def obtener_tipo_personaje(jugador):

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


# ============================================================
# PREPARAR JUGADOR PARA NUEVO COMBATE
# ============================================================

def preparar_jugador_para_combate(jugador):

    # Vida completa
    jugador._vida = jugador.vida_maxima

    # Estados generales
    if hasattr(jugador, "_defendiendo"):
        jugador._defendiendo = False

    if hasattr(jugador, "_turnos_escudo"):
        jugador._turnos_escudo = 0

    # Guerrero
    if hasattr(jugador, "_turnos_grito"):
        jugador._turnos_grito = 0

    if hasattr(jugador, "_guardia_ferrea"):
        jugador._guardia_ferrea = False

    # Mago
    if hasattr(jugador, "_congelacion_activa"):
        jugador._congelacion_activa = False

    # Arquero
    if hasattr(jugador, "_evasion_activa"):
        jugador._evasion_activa = False

    # Reiniciar cooldowns
    if hasattr(jugador, "habilidades"):

        for habilidad in jugador.habilidades:

            if hasattr(
                habilidad,
                "cooldown_actual"
            ):
                habilidad.cooldown_actual = 0

            elif hasattr(
                habilidad,
                "_cooldown_actual"
            ):
                habilidad._cooldown_actual = 0


# ============================================================
# INVENTARIO -> DICCIONARIO
# ============================================================

def obtener_inventario_para_guardar(jugador):

    inventario = {}

    for objeto in jugador.inventario:

        if objeto.nombre not in inventario:
            inventario[objeto.nombre] = 0

        inventario[objeto.nombre] += 1

    return inventario


# ============================================================
# DICCIONARIO -> INVENTARIO
# ============================================================

def cargar_inventario(
    jugador,
    inventario
):

    for nombre_objeto, cantidad in inventario.items():

        for _ in range(cantidad):

            if nombre_objeto == "Poción de Vida":

                jugador.agregar_objeto(
                    PocionVida()
                )

            elif nombre_objeto == "Escudo Protector":

                jugador.agregar_objeto(
                    EscudoProtector()
                )


# ============================================================
# COPIA TEMPORAL PARA REPETIR
# ============================================================

def crear_jugador_temporal(jugador):

    tipo = obtener_tipo_personaje(
        jugador
    )

    temporal = crear_personaje(
        tipo,
        jugador.nombre
    )

    temporal.restaurar_progreso(
        nivel=jugador.nivel,
        experiencia=jugador.experiencia
    )

    inventario = (
        obtener_inventario_para_guardar(
            jugador
        )
    )

    cargar_inventario(
        temporal,
        inventario
    )

    preparar_jugador_para_combate(
        temporal
    )

    return temporal


# ============================================================
# EXPERIENCIA
# ============================================================

def entregar_experiencia(
    jugador,
    cantidad
):

    niveles = jugador.ganar_experiencia(
        cantidad
    )

    print(
        f"+{cantidad} XP | "
        f"Nivel {jugador.nivel} | "
        f"XP {jugador.experiencia}/"
        f"{jugador.experiencia_siguiente_nivel}"
    )

    for subida in niveles:

        print(
            f"¡SUBISTE A NIVEL "
            f"{subida['nivel']}!"
        )

        print(
            f"+{subida['vida']} VIDA | "
            f"+{subida['ataque']} ATQ | "
            f"+{subida['defensa']} DEF"
        )


# ============================================================
# GUARDAR PARTIDA
# ============================================================

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

    tipo_personaje = (
        obtener_tipo_personaje(
            jugador
        )
    )

    # ========================================================
    # PRIMER GUARDADO
    # ========================================================

    if partida_id is None:

        nombre = (
            PantallaNombrePartida()
            .ejecutar()
        )

        if nombre is None:

            return (
                partida_id,
                nombre_partida
            )

        try:

            partida_id = repo.crear_partida(
                nombre_partida=nombre,
                nombre_jugador=jugador.nombre,
                personaje=tipo_personaje,
                siguiente_enemigo=siguiente_enemigo,
                progreso=progreso,
                inventario=inventario,
                nivel=jugador.nivel,
                experiencia=jugador.experiencia
            )

            nombre_partida = nombre

            print(
                f"Partida creada: "
                f"{nombre_partida}"
            )

        except ValueError as error:

            print(
                f"No se pudo guardar: "
                f"{error}"
            )

    # ========================================================
    # ACTUALIZAR PARTIDA
    # ========================================================

    else:

        repo.actualizar_partida(
            partida_id=partida_id,
            nombre_jugador=jugador.nombre,
            personaje=tipo_personaje,
            siguiente_enemigo=siguiente_enemigo,
            progreso=progreso,
            inventario=inventario,
            nivel=jugador.nivel,
            experiencia=jugador.experiencia
        )

        print(
            f"Progreso guardado en: "
            f"{nombre_partida}"
        )

    return (
        partida_id,
        nombre_partida
    )


# ============================================================
# REPETIR COMBATE
# ============================================================

def repetir_combate(
    jugador,
    enemigo_nombre
):

    jugador_temporal = (
        crear_jugador_temporal(
            jugador
        )
    )

    # ========================================================
    # CREAR ENEMIGO
    # ========================================================

    if enemigo_nombre == "Goblin":

        enemigo = Goblin()
        experiencia_ganada = 100

    elif enemigo_nombre == "Orco":

        enemigo = Orco()
        experiencia_ganada = 200

    elif enemigo_nombre == "Guardián Elemental":

        enemigo = JefeFinal()
        experiencia_ganada = 300

    else:

        print(
            f"Enemigo desconocido: "
            f"{enemigo_nombre}"
        )

        return "mapa"

    # ========================================================
    # COMBATE
    # ========================================================

    resultado = PantallaCombate(
        jugador_temporal,
        enemigo
    ).ejecutar()

    if resultado == "salir":
        return "salir"

    # ========================================================
    # VICTORIA
    # ========================================================

    if resultado == "victoria":

        accion = PantallaResultado(
            "victoria"
        ).ejecutar()

        if accion == "salir":
            return "salir"

        # ====================================================
        # DAR XP AL JUGADOR REAL
        # ====================================================

        entregar_experiencia(
            jugador,
            experiencia_ganada
        )

        print(
            f"Entrenamiento completado: "
            f"+{experiencia_ganada} XP"
        )

        # No recompensa
        # No cambia progreso
        return "mapa"

    # ========================================================
    # DERROTA
    # ========================================================

    if resultado == "derrota":

        accion = PantallaResultado(
            "derrota"
        ).ejecutar()

        if accion == "salir":
            return "salir"

        # No XP si pierde
        # No elimina partida
        return "mapa"

    return "mapa"


# ============================================================
# MAPA DE PROGRESO
# ============================================================

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
           jugador,
           partida_guardada=(
          partida_id is not None
        )
        ).ejecutar()

        if accion == "menu":

            return (
                "menu",
                partida_id,
                nombre_partida
            )

        if accion == "salir":

            return (
                "salir",
                partida_id,
                nombre_partida
            )

        if accion == "continuar":

            return (
                "continuar",
                partida_id,
                nombre_partida
            )

        # ====================================================
        # GUARDAR
        # ====================================================

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

            continue

        # ====================================================
        # REPETIR GOBLIN
        # ====================================================

        if accion == "repetir_goblin":

            resultado = repetir_combate(
                jugador,
                "Goblin"
            )

            if resultado == "salir":

                return (
                    "salir",
                    partida_id,
                    nombre_partida
                )

            continue

        # ====================================================
        # REPETIR ORCO
        # ====================================================

        if accion == "repetir_orco":

            resultado = repetir_combate(
                jugador,
                "Orco"
            )

            if resultado == "salir":

                return (
                    "salir",
                    partida_id,
                    nombre_partida
                )

            continue


# ============================================================
# GOBLIN
# ============================================================

def combatir_goblin(
    repo,
    jugador,
    partida_id=None,
    nombre_partida=None
):

    preparar_jugador_para_combate(
        jugador
    )

    enemigo = Goblin()

    resultado = PantallaCombate(
        jugador,
        enemigo
    ).ejecutar()

    if resultado == "salir":
        return "salir"

    # ========================================================
    # DERROTA
    # ========================================================

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

    # ========================================================
    # VICTORIA
    # ========================================================

    if resultado == "victoria":

        accion = PantallaResultado(
            "victoria"
        ).ejecutar()

        if accion == "salir":
            return "salir"

        if accion == "menu":
            return "menu"

        # XP
        entregar_experiencia(
            jugador,
            100
        )

        # ====================================================
        # RECOMPENSA
        # ====================================================

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

        # ====================================================
        # MAPA
        # ====================================================

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

        if accion_mapa == "menu":
            return "menu"

        if accion_mapa == "salir":
            return "salir"

        if accion_mapa == "continuar":

            return combatir_orco(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

    return "menu"


# ============================================================
# ORCO
# ============================================================

def combatir_orco(
    repo,
    jugador,
    partida_id=None,
    nombre_partida=None
):

    # ========================================================
    # PREPARAR JUGADOR
    # ========================================================

    preparar_jugador_para_combate(
        jugador
    )

    enemigo = Orco()

    resultado = PantallaCombate(
        jugador,
        enemigo
    ).ejecutar()

    # ========================================================
    # CERRAR JUEGO
    # ========================================================

    if resultado == "salir":
        return "salir"

    # ========================================================
    # DERROTA
    # ========================================================

    if resultado == "derrota":

        accion_resultado = PantallaResultado(
            "derrota"
        ).ejecutar()

        if accion_resultado == "salir":
            return "salir"

        # ----------------------------------------------------
        # NO SE BORRA LA PARTIDA
        # NO SE PIERDE XP
        # NO SE PIERDE NIVEL
        # ----------------------------------------------------

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

        if accion_mapa == "salir":
            return "salir"

        if accion_mapa == "menu":
            return "menu"

        if accion_mapa == "continuar":

            return combatir_orco(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

        return "menu"

    # ========================================================
    # VICTORIA
    # ========================================================

    if resultado == "victoria":

        accion_resultado = PantallaResultado(
            "victoria"
        ).ejecutar()

        if accion_resultado == "salir":
            return "salir"

        if accion_resultado == "menu":
            return "menu"

        # ====================================================
        # EXPERIENCIA
        # ====================================================

        entregar_experiencia(
            jugador,
            200
        )

        # ====================================================
        # RECOMPENSA
        # ====================================================

        recompensa = PantallaRecompensa().ejecutar()

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

        # ====================================================
        # MAPA DESPUÉS DEL ORCO
        # ====================================================

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

        if accion_mapa == "salir":
            return "salir"

        if accion_mapa == "menu":
            return "menu"

        # ====================================================
        # JEFE FINAL
        # ====================================================

        if accion_mapa == "continuar":

            return combatir_jefe_final(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

        return "menu"

    # ========================================================
    # SEGURIDAD
    # ========================================================

    return "menu"

# ============================================================
# JEFE FINAL
# ============================================================

def combatir_jefe_final(
    repo,
    jugador,
    partida_id=None,
    nombre_partida=None
):
    # ========================================================
    # PREPARAR JUGADOR
    # ========================================================

    preparar_jugador_para_combate(
        jugador
    )

    enemigo = JefeFinal()

    # ========================================================
    # COMBATE FINAL
    # ========================================================

    resultado = PantallaCombate(
        jugador,
        enemigo
    ).ejecutar()

    # ========================================================
    # SALIR
    # ========================================================

    if resultado == "salir":
        return "salir"

    # ========================================================
    # DERROTA
    # ========================================================

    if resultado == "derrota":

        accion_resultado = PantallaResultado(
            "derrota"
        ).ejecutar()

        if accion_resultado == "salir":
            return "salir"

        # Volvemos al mapa después del Orco.
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

        if accion_mapa == "salir":
            return "salir"

        if accion_mapa == "menu":
            return "menu"

        if accion_mapa == "continuar":

            return combatir_jefe_final(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

        return "menu"

    # ========================================================
    # VICTORIA FINAL
    # ========================================================

    if resultado == "victoria":

        # ----------------------------------------------------
        # EXPERIENCIA
        # ----------------------------------------------------

        entregar_experiencia(
            jugador,
            300
        )

        # ----------------------------------------------------
        # GUARDAR PROGRESO FINAL
        # ----------------------------------------------------

        if partida_id is not None:

            try:

                repo.actualizar_partida(
                    partida_id=partida_id,
                    nombre_jugador=jugador.nombre,
                    personaje=(
                        obtener_tipo_personaje(
                            jugador
                        )
                    ),
                    siguiente_enemigo="Guardián Elemental",
                    progreso=3,
                    inventario=(
                        obtener_inventario_para_guardar(
                            jugador
                        )
                    ),
                    nivel=jugador.nivel,
                    experiencia=jugador.experiencia
                )

                print(
                    "Progreso final guardado."
                )

            except ValueError as error:

                print(
                    f"No se pudo guardar "
                    f"el progreso final: {error}"
                )

        # ----------------------------------------------------
        # PANTALLA FINAL
        # ----------------------------------------------------

        accion_final = (
            PantallaVictoriaFinal()
            .ejecutar()
        )

        if accion_final == "salir":
            return "salir"

        if accion_final == "menu":
            return "menu"

        if accion_final == "jugar":

            return iniciar_nueva_partida(
                repo
            )

        return "menu"

    return "menu"

# ============================================================
# NUEVA PARTIDA
# ============================================================

def iniciar_nueva_partida(repo):

    seleccion = (
        PantallaSeleccionPersonaje()
        .ejecutar()
    )

    if seleccion == "salir":
        return "salir"

    if seleccion == "menu":
        return "menu"

    jugador = crear_personaje(
        seleccion,
        "Ares"
    )

    partida_id = None
    nombre_partida = None

    # ========================================================
    # MAPA INICIAL
    # ========================================================

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


# ============================================================
# CARGAR PARTIDA
# ============================================================

def continuar_partida(repo):

    while True:

        partidas = (
            repo.listar_partidas()
        )

        if not partidas:

            print(
                "No hay partidas guardadas."
            )

            return "menu"

        (
            accion_partida,
            partida_id
        ) = PantallaCargarPartida(
            partidas
        ).ejecutar()

        if accion_partida == "salir":
            return "salir"

        if accion_partida == "volver":
            return "menu"

        if accion_partida == "eliminar":

            repo.eliminar(
                partida_id
            )

            continue

        if accion_partida == "cargar":
            break

    # ========================================================
    # DATOS
    # ========================================================

    datos = repo.cargar(
        partida_id
    )

    if datos is None:

        print(
            "No se pudo cargar "
            "la partida."
        )

        return "menu"

    # ========================================================
    # PERSONAJE
    # ========================================================

    jugador = crear_personaje(
        datos["personaje"],
        datos["nombre_jugador"]
    )

    jugador.restaurar_progreso(
        nivel=datos["nivel"],
        experiencia=datos["experiencia"]
    )

    cargar_inventario(
        jugador,
        datos["inventario"]
    )

    nombre_partida = (
        datos["nombre_partida"]
    )

    siguiente_enemigo = (
        datos["siguiente_enemigo"]
    )

    progreso = (
        datos["progreso"]
    )

    # ========================================================
    # MAPA CORRESPONDIENTE
    # ========================================================

    if siguiente_enemigo == "Goblin":

        estado_mapa = "inicio"

    elif siguiente_enemigo == "Orco":

        estado_mapa = "goblin"

    elif (
        siguiente_enemigo
        == "Guardián Elemental"
    ):

        estado_mapa = "orco"

    else:

        print(
            "Progreso desconocido: "
            f"{siguiente_enemigo}"
        )

        return "menu"

    # ========================================================
    # MOSTRAR MAPA
    # ========================================================

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

    if accion == "menu":
        return "menu"

    if accion == "salir":
        return "salir"

    # ========================================================
    # CONTINUAR
    # ========================================================

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

        if (
            siguiente_enemigo
            == "Guardián Elemental"
        ):

            return combatir_jefe_final(
                repo=repo,
                jugador=jugador,
                partida_id=partida_id,
                nombre_partida=nombre_partida
            )

    return "menu"


# ============================================================
# MAIN
# ============================================================

def main():

    pygame.init()

    repo = RepositorioPartida()

    try:

        while True:

            hay_partidas = (
                repo.existe_partida()
            )

            opcion = PantallaInicio(
                partida_disponible=hay_partidas
            ).ejecutar()

            # =================================================
            # NUEVA PARTIDA
            # =================================================

            if opcion == "jugar":

                accion = (
                    iniciar_nueva_partida(
                        repo
                    )
                )

            # =================================================
            # CARGAR
            # =================================================

            elif opcion == "cargar":

                accion = (
                    continuar_partida(
                        repo
                    )
                )

            # =================================================
            # SALIR
            # =================================================

            elif opcion == "salir":

                break

            else:

                continue

            if accion == "salir":
                break

    finally:

        repo.cerrar()

        pygame.quit()


# ============================================================
# INICIO
# ============================================================

if __name__ == "__main__":
    main()