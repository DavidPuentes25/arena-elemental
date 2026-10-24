from pathlib import Path
import pygame

from src.juego.combate import Combate


BASE_DIR = Path(__file__).resolve().parents[2]


class Boton:

    def __init__(self, x, y, ancho, alto, texto, fuente):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.fuente = fuente

    def dibujar(self, pantalla, habilitado=True):
        mouse = pygame.mouse.get_pos()

        if not habilitado:
            color = (70, 70, 70)
        elif self.rect.collidepoint(mouse):
            color = (122, 79, 40)
        else:
            color = (89, 55, 32)

        pygame.draw.rect(
            pantalla,
            color,
            self.rect,
            border_radius=10
        )

        pygame.draw.rect(
            pantalla,
            (224, 185, 105),
            self.rect,
            2,
            border_radius=10
        )

        texto = self.fuente.render(
            self.texto,
            True,
            (255, 255, 255)
        )

        pantalla.blit(
            texto,
            texto.get_rect(center=self.rect.center)
        )

    def fue_presionado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


class PantallaCombate:

    def __init__(self, jugador, enemigo):
        pygame.init()

        self.jugador = jugador
        self.enemigo = enemigo
        self.combate = Combate(jugador, enemigo)

        self.ancho = 1000
        self.alto = 650

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption("Arena Elemental")

        self.reloj = pygame.time.Clock()

        self.fuente_titulo = pygame.font.SysFont(
            "arial",
            30,
            bold=True
        )

        self.fuente = pygame.font.SysFont(
            "arial",
            20,
            bold=True
        )

        self.fuente_pequena = pygame.font.SysFont(
            "arial",
            16
        )

        self.fuente_boton = pygame.font.SysFont(
            "georgia",
            20,
            bold=True
        )

        self.fuente_estado = pygame.font.SysFont(
            "arial",
            15,
            bold=True
        )

        self.pose_jugador = "idle"
        self.pose_enemigo = "idle"

        self.bloqueado = False
        self.accion_pendiente = None
        self.tiempo_animacion = 0

        self.menu_objetos_abierto = False
        self.opciones_objetos = []

        self.rect_volver_objetos = pygame.Rect(
            400,
            445,
            200,
            45
        )

        self.mensajes = [
            f"Comienza el combate contra {enemigo.nombre}."
        ]

        self.cargar_recursos()

        self.boton_atacar = Boton(
            140, 515, 160, 50,
            "ATACAR",
            self.fuente
        )

        self.boton_habilidad = Boton(
            325, 515, 160, 50,
            "HABILIDAD",
            self.fuente
        )

        self.boton_defender = Boton(
            510, 515, 160, 50,
            "DEFENDER",
            self.fuente
        )

        self.boton_objeto = Boton(
            695, 515, 160, 50,
            "OBJETO",
            self.fuente
        )

    # ---------------------------------------------------------
    # RECURSOS
    # ---------------------------------------------------------

    def cargar_imagen(self, ruta, alto=None):
        imagen = pygame.image.load(
            str(ruta)
        ).convert_alpha()

        if alto is None:
            return imagen

        proporcion = alto / imagen.get_height()
        ancho = int(imagen.get_width() * proporcion)

        return pygame.transform.smoothscale(
            imagen,
            (ancho, alto)
        )

    def cargar_recursos(self):
        ruta_fondo = (
            BASE_DIR
            / "assets"
            / "fondos"
            / "arena_combate.png"
        )

        self.fondo = pygame.image.load(
            str(ruta_fondo)
        ).convert()

        self.fondo = pygame.transform.smoothscale(
            self.fondo,
            (self.ancho, self.alto)
        )

        ruta_guerrero = (
            BASE_DIR
            / "assets"
            / "personajes"
            / "guerrero"
        )

        ruta_goblin = (
            BASE_DIR
            / "assets"
            / "enemigos"
            / "goblin"
        )

        self.sprites_jugador = {
            "idle": self.cargar_imagen(
                ruta_guerrero / "idle.png",
                340
            ),
            "ataque": self.cargar_imagen(
                ruta_guerrero / "ataque.png",
                360
            ),
            "habilidad": self.cargar_imagen(
                ruta_guerrero / "habilidad.png",
                370
            ),
            "defensa": self.cargar_imagen(
                ruta_guerrero / "defensa.png",
                350
            ),
            "derrotado": self.cargar_imagen(
                ruta_guerrero / "derrotado.png",
                300
            )
        }

        self.sprites_enemigo = {
            "idle": self.cargar_imagen(
                ruta_goblin / "idle.png",
                300
            ),
            "ataque": self.cargar_imagen(
                ruta_goblin / "ataque.png",
                325
            ),
            "habilidad": self.cargar_imagen(
                ruta_goblin / "habilidad.png",
                330
            ),
            "defensa": self.cargar_imagen(
                ruta_goblin / "defensa.png",
                300
            ),
            "derrotado": self.cargar_imagen(
                ruta_goblin / "derrotado.png",
                260
            )
        }

    # ---------------------------------------------------------
    # ELEMENTOS VISUALES
    # ---------------------------------------------------------

    def dibujar_barra_vida(
        self,
        x,
        y,
        ancho,
        vida,
        vida_maxima
    ):
        porcentaje = vida / vida_maxima
        porcentaje = max(0, min(1, porcentaje))

        pygame.draw.rect(
            self.pantalla,
            (40, 40, 40),
            (x, y, ancho, 25),
            border_radius=8
        )

        pygame.draw.rect(
            self.pantalla,
            (45, 185, 70),
            (
                x,
                y,
                int(ancho * porcentaje),
                25
            ),
            border_radius=8
        )

        pygame.draw.rect(
            self.pantalla,
            (230, 230, 230),
            (x, y, ancho, 25),
            2,
            border_radius=8
        )

        texto = self.fuente_pequena.render(
            f"{vida} / {vida_maxima}",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            texto,
            texto.get_rect(
                center=(
                    x + ancho // 2,
                    y + 12
                )
            )
        )

    def dibujar_sprite(
        self,
        sprite,
        centro_x,
        base_y
    ):
        rect = sprite.get_rect()

        rect.midbottom = (
            centro_x,
            base_y
        )

        self.pantalla.blit(
            sprite,
            rect
        )

    def dibujar_estado_escudo(self):
        turnos = getattr(
            self.jugador,
            "turnos_escudo",
            0
        )

        if turnos <= 0:
            return

        panel_x = 80
        panel_y = 130
        panel_ancho = 250
        panel_alto = 58

        panel = pygame.Surface(
            (panel_ancho, panel_alto),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            panel,
            (15, 35, 55, 220),
            panel.get_rect(),
            border_radius=12
        )

        pygame.draw.rect(
            panel,
            (100, 205, 255, 255),
            panel.get_rect(),
            2,
            border_radius=12
        )

        self.pantalla.blit(
            panel,
            (panel_x, panel_y)
        )

        puntos_escudo = [
            (95, 142),
            (108, 137),
            (121, 142),
            (119, 158),
            (108, 169),
            (97, 158)
        ]

        pygame.draw.polygon(
            self.pantalla,
            (100, 205, 255),
            puntos_escudo
        )

        pygame.draw.polygon(
            self.pantalla,
            (220, 245, 255),
            puntos_escudo,
            2
        )

        texto_estado = self.fuente_estado.render(
            "ESCUDO  -30% DAÑO",
            True,
            (220, 245, 255)
        )

        self.pantalla.blit(
            texto_estado,
            (130, 138)
        )

        for i in range(5):
            x = 140 + (i * 25)
            y = 166

            if i < turnos:
                color = (100, 205, 255)
            else:
                color = (55, 75, 90)

            pygame.draw.circle(
                self.pantalla,
                color,
                (x, y),
                7
            )

            pygame.draw.circle(
                self.pantalla,
                (200, 235, 250),
                (x, y),
                7,
                1
            )

    # ---------------------------------------------------------
    # MENSAJES
    # ---------------------------------------------------------

    def agregar_mensaje(self, mensaje):
        self.mensajes.append(mensaje)
        self.mensajes = self.mensajes[-3:]

    def registrar_resultado(self, resultado):
        if resultado is None:
            return

        accion = resultado.get("accion")

        if accion == "Defenderse":
            self.agregar_mensaje(
                f"{resultado['atacante']} se defiende."
            )

        elif accion == "Usar objeto":
            if resultado["efecto"] == "Curación":
                self.agregar_mensaje(
                    f"{resultado['atacante']} usa "
                    f"{resultado['objeto']} y recupera "
                    f"{resultado['cantidad']} HP."
                )
            else:
                self.agregar_mensaje(
                    f"{resultado['atacante']} activa "
                    f"{resultado['objeto']}."
                )

        else:
            self.agregar_mensaje(
                f"{resultado['atacante']} usa "
                f"{resultado['accion']} y causa "
                f"{resultado['danio']} de daño."
            )

    # ---------------------------------------------------------
    # ACCIONES DEL JUGADOR
    # ---------------------------------------------------------

    def procesar_accion(self, accion):
        if self.bloqueado:
            return

        if self.combate.finalizado:
            return

        if self.combate.turno != "jugador":
            return

        resultado = None

        if accion == "atacar":
            self.pose_jugador = "ataque"
            resultado = self.combate.atacar_jugador()

        elif accion == "habilidad":
            self.pose_jugador = "habilidad"
            resultado = self.combate.usar_habilidad_jugador()

        elif accion == "defender":
            self.pose_jugador = "defensa"
            resultado = self.combate.defender_jugador()

        self.registrar_resultado(resultado)

        if self.combate.finalizado:
            if self.combate.ganador == self.jugador.nombre:
                self.pose_enemigo = "derrotado"

                self.agregar_mensaje(
                    f"¡{self.jugador.nombre} ganó!"
                )

            return

        self.bloqueado = True
        self.accion_pendiente = "enemigo"

        self.tiempo_animacion = (
            pygame.time.get_ticks() + 600
        )

    # ---------------------------------------------------------
    # TURNO DEL ENEMIGO
    # ---------------------------------------------------------

    def ejecutar_turno_enemigo(self):
        resultado = self.combate.turno_enemigo()

        if resultado is None:
            return

        accion = resultado["accion"].lower()

        if (
            "fuerte" in accion
            or "devastador" in accion
            or "especial" in accion
        ):
            self.pose_enemigo = "habilidad"
        else:
            self.pose_enemigo = "ataque"

        self.registrar_resultado(resultado)

        if self.combate.finalizado:
            if self.combate.ganador != self.jugador.nombre:
                self.pose_jugador = "derrotado"

                self.agregar_mensaje(
                    f"{self.jugador.nombre} ha sido derrotado."
                )

        self.accion_pendiente = "fin_enemigo"

        self.tiempo_animacion = (
            pygame.time.get_ticks() + 600
        )

    # ---------------------------------------------------------
    # ANIMACIONES
    # ---------------------------------------------------------

    def actualizar_animaciones(self):
        if not self.bloqueado:
            return

        ahora = pygame.time.get_ticks()

        if ahora < self.tiempo_animacion:
            return

        if self.accion_pendiente == "enemigo":
            if self.pose_jugador != "defensa":
                self.pose_jugador = "idle"

            self.ejecutar_turno_enemigo()

        elif self.accion_pendiente == "fin_enemigo":
            if not self.combate.finalizado:
                self.pose_jugador = "idle"
                self.pose_enemigo = "idle"

            self.accion_pendiente = None
            self.bloqueado = False

    # ---------------------------------------------------------
    # INVENTARIO
    # ---------------------------------------------------------

    def abrir_menu_objetos(self):
        if not self.jugador.inventario:
            self.agregar_mensaje(
                "No tienes objetos disponibles."
            )
            return

        self.menu_objetos_abierto = True
        self.actualizar_opciones_objetos()

    def cerrar_menu_objetos(self):
        self.menu_objetos_abierto = False
        self.opciones_objetos = []

    def actualizar_opciones_objetos(self):
        objetos = {}

        for indice, objeto in enumerate(
            self.jugador.inventario
        ):
            if objeto.nombre not in objetos:
                objetos[objeto.nombre] = {
                    "cantidad": 0,
                    "indice": indice
                }

            objetos[
                objeto.nombre
            ]["cantidad"] += 1

        self.opciones_objetos = []

        y = 275

        for nombre, datos in objetos.items():
            rect = pygame.Rect(
                325,
                y,
                350,
                55
            )

            self.opciones_objetos.append(
                {
                    "nombre": nombre,
                    "cantidad": datos["cantidad"],
                    "indice": datos["indice"],
                    "rect": rect
                }
            )

            y += 70

    def usar_objeto_seleccionado(
        self,
        indice
    ):
        if self.bloqueado:
            return

        resultado = self.combate.usar_objeto_jugador(
            indice
        )

        if resultado is None:
            return

        self.cerrar_menu_objetos()

        if resultado["efecto"] == "Curación":
            self.agregar_mensaje(
                f"{self.jugador.nombre} usa "
                f"{resultado['objeto']} y recupera "
                f"{resultado['cantidad']} HP."
            )

            self.pose_jugador = "idle"

        else:
            self.agregar_mensaje(
                f"{self.jugador.nombre} activa "
                f"{resultado['objeto']}: "
                "-30% daño durante 5 turnos."
            )

            self.pose_jugador = "defensa"

        self.bloqueado = True
        self.accion_pendiente = "enemigo"

        self.tiempo_animacion = (
            pygame.time.get_ticks() + 600
        )

    def manejar_evento_menu_objetos(
        self,
        evento
    ):
        if evento.type != pygame.MOUSEBUTTONDOWN:
            return

        if evento.button != 1:
            return

        for opcion in self.opciones_objetos:
            if opcion["rect"].collidepoint(
                evento.pos
            ):
                self.usar_objeto_seleccionado(
                    opcion["indice"]
                )
                return

        if self.rect_volver_objetos.collidepoint(
            evento.pos
        ):
            self.cerrar_menu_objetos()

    def dibujar_menu_objetos(self):
        sombra = pygame.Surface(
            (self.ancho, self.alto),
            pygame.SRCALPHA
        )

        sombra.fill(
            (0, 0, 0, 165)
        )

        self.pantalla.blit(
            sombra,
            (0, 0)
        )

        panel_rect = pygame.Rect(
            275,
            170,
            450,
            340
        )

        panel = pygame.Surface(
            (
                panel_rect.width,
                panel_rect.height
            ),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            panel,
            (35, 25, 20, 240),
            panel.get_rect(),
            border_radius=18
        )

        self.pantalla.blit(
            panel,
            panel_rect.topleft
        )

        pygame.draw.rect(
            self.pantalla,
            (220, 165, 70),
            panel_rect,
            3,
            border_radius=18
        )

        titulo = self.fuente_titulo.render(
            "INVENTARIO",
            True,
            (255, 220, 130)
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(500, 215)
            )
        )

        mouse = pygame.mouse.get_pos()

        for opcion in self.opciones_objetos:
            rect = opcion["rect"]

            if rect.collidepoint(mouse):
                color = (130, 75, 25)
                borde = (255, 220, 110)
            else:
                color = (65, 38, 20)
                borde = (210, 160, 70)

            pygame.draw.rect(
                self.pantalla,
                color,
                rect,
                border_radius=10
            )

            pygame.draw.rect(
                self.pantalla,
                borde,
                rect,
                2,
                border_radius=10
            )

            texto = (
                f"{opcion['nombre']} "
                f"x{opcion['cantidad']}"
            )

            superficie_texto = self.fuente_boton.render(
                texto,
                True,
                (255, 245, 220)
            )

            self.pantalla.blit(
                superficie_texto,
                superficie_texto.get_rect(
                    center=rect.center
                )
            )

        if self.rect_volver_objetos.collidepoint(
            mouse
        ):
            color_volver = (90, 65, 45)
        else:
            color_volver = (55, 45, 40)

        pygame.draw.rect(
            self.pantalla,
            color_volver,
            self.rect_volver_objetos,
            border_radius=10
        )

        pygame.draw.rect(
            self.pantalla,
            (170, 150, 120),
            self.rect_volver_objetos,
            2,
            border_radius=10
        )

        texto_volver = self.fuente_boton.render(
            "VOLVER",
            True,
            (240, 235, 225)
        )

        self.pantalla.blit(
            texto_volver,
            texto_volver.get_rect(
                center=self.rect_volver_objetos.center
            )
        )

    # ---------------------------------------------------------
    # DIBUJO GENERAL
    # ---------------------------------------------------------

    def dibujar(self):
        self.pantalla.blit(
            self.fondo,
            (0, 0)
        )

        panel = pygame.Surface(
            (1000, 175),
            pygame.SRCALPHA
        )

        panel.fill(
            (15, 15, 25, 210)
        )

        self.pantalla.blit(
            panel,
            (0, 475)
        )

        titulo = self.fuente_titulo.render(
            "ARENA ELEMENTAL",
            True,
            (255, 235, 170)
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(500, 30)
            )
        )

        nombre_jugador = self.fuente.render(
            self.jugador.nombre,
            True,
            (255, 255, 255)
        )

        nombre_enemigo = self.fuente.render(
            self.enemigo.nombre,
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            nombre_jugador,
            (80, 65)
        )

        self.pantalla.blit(
            nombre_enemigo,
            (730, 65)
        )

        self.dibujar_barra_vida(
            80,
            95,
            250,
            self.jugador.vida,
            self.jugador.vida_maxima
        )

        self.dibujar_barra_vida(
            670,
            95,
            250,
            self.enemigo.vida,
            self.enemigo.vida_maxima
        )

        self.dibujar_estado_escudo()

        sprite_jugador = self.sprites_jugador[
            self.pose_jugador
        ]

        sprite_enemigo = self.sprites_enemigo[
            self.pose_enemigo
        ]

        self.dibujar_sprite(
            sprite_jugador,
            265,
            475
        )

        self.dibujar_sprite(
            sprite_enemigo,
            740,
            475
        )

        habilitado = (
            not self.bloqueado
            and not self.combate.finalizado
            and not self.menu_objetos_abierto
        )

        self.boton_atacar.dibujar(
            self.pantalla,
            habilitado
        )

        self.boton_habilidad.dibujar(
            self.pantalla,
            habilitado
        )

        self.boton_defender.dibujar(
            self.pantalla,
            habilitado
        )

        self.boton_objeto.dibujar(
            self.pantalla,
            habilitado
        )

        y = 580

        for mensaje in self.mensajes:
            texto = self.fuente_pequena.render(
                mensaje,
                True,
                (245, 245, 245)
            )

            self.pantalla.blit(
                texto,
                (60, y)
            )

            y += 20

        if self.menu_objetos_abierto:
            self.dibujar_menu_objetos()

        pygame.display.flip()

    # ---------------------------------------------------------
    # BUCLE PRINCIPAL
    # ---------------------------------------------------------

    def ejecutar(self):
        while True:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return "salir"

                if self.menu_objetos_abierto:
                    self.manejar_evento_menu_objetos(
                        evento
                    )
                    continue

                if not self.bloqueado:

                    if self.boton_atacar.fue_presionado(
                        evento
                    ):
                        self.procesar_accion(
                            "atacar"
                        )

                    elif self.boton_habilidad.fue_presionado(
                        evento
                    ):
                        self.procesar_accion(
                            "habilidad"
                        )

                    elif self.boton_defender.fue_presionado(
                        evento
                    ):
                        self.procesar_accion(
                            "defender"
                        )

                    elif self.boton_objeto.fue_presionado(
                        evento
                    ):
                        self.abrir_menu_objetos()

            self.actualizar_animaciones()

            if self.combate.finalizado:

                if self.jugador.esta_vivo:
                    self.pose_enemigo = "derrotado"
                    resultado = "victoria"
                else:
                    self.pose_jugador = "derrotado"
                    resultado = "derrota"

                self.dibujar()

                pygame.time.delay(1000)

                return resultado

            self.dibujar()

            self.reloj.tick(60)
