from pathlib import Path
import pygame

from src.juego.combate import Combate


# Ruta principal del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]


# Representa un botón
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


# Controla la interfaz visual del combate
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

        # Estado visual
        self.pose_jugador = "idle"
        self.pose_enemigo = "idle"

        self.bloqueado = False
        self.accion_pendiente = None
        self.tiempo_animacion = 0

        self.mensajes = [
            f"Comienza el combate contra {enemigo.nombre}."
        ]

        # Carga recursos gráficos
        self.cargar_recursos()

        # Botones
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

    # Carga y escala una imagen
    def cargar_imagen(self, ruta, alto=None):
        imagen = pygame.image.load(str(ruta)).convert_alpha()

        if alto is None:
            return imagen

        proporcion = alto / imagen.get_height()
        ancho = int(imagen.get_width() * proporcion)

        return pygame.transform.smoothscale(
            imagen,
            (ancho, alto)
        )

    # Carga fondo y sprites
    def cargar_recursos(self):

        fondo = BASE_DIR / "assets" / "fondos" / "arena_combate.png"

        self.fondo = pygame.image.load(
            str(fondo)
        ).convert()

        self.fondo = pygame.transform.smoothscale(
            self.fondo,
            (self.ancho, self.alto)
        )

        ruta_guerrero = (
            BASE_DIR /
            "assets" /
            "personajes" /
            "guerrero"
        )

        ruta_goblin = (
            BASE_DIR /
            "assets" /
            "enemigos" /
            "goblin"
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

    # Dibuja una barra de vida
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
                center=(x + ancho // 2, y + 12)
            )
        )

    # Agrega mensajes al combate
    def agregar_mensaje(self, mensaje):
        self.mensajes.append(mensaje)
        self.mensajes = self.mensajes[-3:]

    # Convierte resultados en mensajes
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
                    f"{resultado['atacante']} usa "
                    f"{resultado['objeto']}."
                )

        else:
            self.agregar_mensaje(
                f"{resultado['atacante']} usa "
                f"{resultado['accion']} y causa "
                f"{resultado['danio']} de daño."
            )

    # Ejecuta la acción seleccionada
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

        elif accion == "objeto":

            if not self.jugador.inventario:
                self.agregar_mensaje(
                    "No tienes objetos disponibles."
                )
                return

            resultado = self.combate.usar_objeto_jugador(0)

        self.registrar_resultado(resultado)

        # Si derrotó al enemigo
        if self.combate.finalizado:

            if self.combate.ganador == self.jugador.nombre:
                self.pose_enemigo = "derrotado"

                self.agregar_mensaje(
                    f"¡{self.jugador.nombre} ganó!"
                )

            return

        # Espera antes del turno enemigo
        self.bloqueado = True
        self.accion_pendiente = "enemigo"

        self.tiempo_animacion = (
            pygame.time.get_ticks() + 600
        )

    # Ejecuta automáticamente al enemigo
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

    # Controla la duración de las poses
    def actualizar_animaciones(self):

        if not self.bloqueado:
            return

        ahora = pygame.time.get_ticks()

        if ahora < self.tiempo_animacion:
            return

        if self.accion_pendiente == "enemigo":

            # La defensa permanece durante el ataque
            if self.pose_jugador != "defensa":
                self.pose_jugador = "idle"

            self.ejecutar_turno_enemigo()

        elif self.accion_pendiente == "fin_enemigo":

            if not self.combate.finalizado:
                self.pose_jugador = "idle"
                self.pose_enemigo = "idle"

            self.accion_pendiente = None
            self.bloqueado = False

    # Dibuja el personaje desde su base
    def dibujar_sprite(self, sprite, centro_x, base_y):

        rect = sprite.get_rect()

        rect.midbottom = (
            centro_x,
            base_y
        )

        self.pantalla.blit(
            sprite,
            rect
        )

    # Dibuja toda la interfaz
    def dibujar(self):

        self.pantalla.blit(
            self.fondo,
            (0, 0)
        )

        # Sombra inferior
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

        # Título
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

        # Nombres
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

        # Barras
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

        # Sprites
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

        # Botones
        habilitado = (
            not self.bloqueado
            and not self.combate.finalizado
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

        # Mensajes
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

        pygame.display.flip()

    # Bucle principal
    def ejecutar(self):

        ejecutando = True

        while ejecutando:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    ejecutando = False

                if not self.bloqueado:

                    if self.boton_atacar.fue_presionado(evento):
                        self.procesar_accion("atacar")

                    elif self.boton_habilidad.fue_presionado(evento):
                        self.procesar_accion("habilidad")

                    elif self.boton_defender.fue_presionado(evento):
                        self.procesar_accion("defender")

                    elif self.boton_objeto.fue_presionado(evento):
                        self.procesar_accion("objeto")

            self.actualizar_animaciones()

            self.dibujar()

            self.reloj.tick(60)

        pygame.quit()