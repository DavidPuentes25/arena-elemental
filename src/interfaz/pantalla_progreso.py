from pathlib import Path
import pygame


BASE_DIR = Path(__file__).resolve().parents[2]


class PantallaProgreso:

    def __init__(
        self,
        estado,
        jugador,
        partida_guardada=False
    ):
        pygame.init()

        self.estado = estado
        self.jugador = jugador

        self.ancho = 1000
        self.alto = 700

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption(
            "Arena Elemental - Progreso"
        )

        self.reloj = pygame.time.Clock()

        # =====================================================
        # FUENTES
        # =====================================================

        self.fuente_boton = pygame.font.SysFont(
            "georgia",
            16,
            bold=True
        )

        self.fuente_nivel = pygame.font.SysFont(
            "georgia",
            18,
            bold=True
        )

        self.fuente_xp = pygame.font.SysFont(
            "arial",
            13,
            bold=True
        )

        # =====================================================
        # MAPA SEGÚN PROGRESO
        # =====================================================

        if estado == "inicio":

            ruta = (
                BASE_DIR
                / "assets"
                / "interfaz"
                / "mapa_inicio.png"
            )

            self.texto_guardar = (
                "GUARDAR PROGRESO"
                if partida_guardada
                else "GUARDAR PARTIDA"
            )

            self.texto_continuar = (
                "COMENZAR COMBATE"
            )

        elif estado == "goblin":

            ruta = (
                BASE_DIR
                / "assets"
                / "interfaz"
                / "mapa_goblin.png"
            )

            self.texto_guardar = (
                "GUARDAR PROGRESO"
            )

            self.texto_continuar = (
                "ENFRENTAR ORCO"
            )

        elif estado == "orco":

            ruta = (
                BASE_DIR
                / "assets"
                / "interfaz"
                / "mapa_orco.png"
            )

            self.texto_guardar = (
                "GUARDAR PROGRESO"
            )

            self.texto_continuar = (
                "ENFRENTAR GUARDIÁN"
            )

        else:

            raise ValueError(
                f"Estado desconocido: {estado}"
            )

        # =====================================================
        # FONDO
        # =====================================================

        imagen_original = pygame.image.load(
            str(ruta)
        ).convert()

        self.alto_mapa = 560

        self.fondo = pygame.transform.smoothscale(
            imagen_original,
            (
                self.ancho,
                self.alto_mapa
            )
        )

        # =====================================================
        # FRANJA INFERIOR
        # =====================================================

        self.rect_franja = pygame.Rect(
            0,
            self.alto_mapa,
            self.ancho,
            self.alto - self.alto_mapa
        )

        # =====================================================
        # PANEL NIVEL
        # =====================================================

        self.rect_nivel = pygame.Rect(
            30,
            570,
            290,
            50
        )

        # =====================================================
        # BOTONES PRINCIPALES
        # =====================================================

        self.rect_inicio = pygame.Rect(
            35,
            635,
            270,
            45
        )

        self.rect_guardar = pygame.Rect(
            365,
            635,
            270,
            45
        )

        self.rect_continuar = pygame.Rect(
            695,
            635,
            270,
            45
        )

        # =====================================================
        # REPETIR COMBATES
        # =====================================================

        self.rect_repetir_goblin = None
        self.rect_repetir_orco = None

        if estado == "goblin":

            self.rect_repetir_goblin = pygame.Rect(
                365,
                575,
                270,
                40
            )

        elif estado == "orco":

            self.rect_repetir_goblin = pygame.Rect(
                365,
                575,
                200,
                40
            )

            self.rect_repetir_orco = pygame.Rect(
                580,
                575,
                200,
                40
            )

    # =========================================================
    # BOTÓN
    # =========================================================

    def dibujar_boton(
        self,
        rect,
        texto,
        secundario=False
    ):
        mouse = pygame.mouse.get_pos()

        hover = rect.collidepoint(
            mouse
        )

        if secundario:

            if hover:
                color = (75, 65, 85)
                borde = (205, 175, 245)

            else:
                color = (42, 36, 50)
                borde = (140, 115, 170)

        else:

            if hover:
                color = (125, 70, 25)
                borde = (255, 220, 100)

            else:
                color = (55, 35, 30)
                borde = (215, 165, 70)

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

        superficie = self.fuente_boton.render(
            texto,
            True,
            (255, 245, 220)
        )

        self.pantalla.blit(
            superficie,
            superficie.get_rect(
                center=rect.center
            )
        )

    # =========================================================
    # NIVEL Y EXPERIENCIA
    # =========================================================

    def dibujar_nivel(self):

        nivel = getattr(
            self.jugador,
            "nivel",
            1
        )

        experiencia = getattr(
            self.jugador,
            "experiencia",
            0
        )

        experiencia_necesaria = getattr(
            self.jugador,
            "experiencia_siguiente_nivel",
            100
        )

        if experiencia_necesaria > 0:

            porcentaje = (
                experiencia
                / experiencia_necesaria
            )

        else:

            porcentaje = 0

        porcentaje = max(
            0,
            min(
                1,
                porcentaje
            )
        )

        # Panel
        pygame.draw.rect(
            self.pantalla,
            (30, 25, 38),
            self.rect_nivel,
            border_radius=10
        )

        pygame.draw.rect(
            self.pantalla,
            (180, 145, 225),
            self.rect_nivel,
            2,
            border_radius=10
        )

        # Nombre y nivel
        texto_nivel = self.fuente_nivel.render(
            (
                f"{self.jugador.nombre}  "
                f"·  NIVEL {nivel}"
            ),
            True,
            (245, 230, 255)
        )

        self.pantalla.blit(
            texto_nivel,
            (
                self.rect_nivel.x + 12,
                self.rect_nivel.y + 6
            )
        )

        # Barra XP
        x = self.rect_nivel.x + 12
        y = self.rect_nivel.y + 31

        ancho = 180
        alto = 9

        pygame.draw.rect(
            self.pantalla,
            (55, 50, 65),
            (
                x,
                y,
                ancho,
                alto
            ),
            border_radius=5
        )

        pygame.draw.rect(
            self.pantalla,
            (140, 95, 220),
            (
                x,
                y,
                int(
                    ancho
                    * porcentaje
                ),
                alto
            ),
            border_radius=5
        )

        pygame.draw.rect(
            self.pantalla,
            (220, 205, 250),
            (
                x,
                y,
                ancho,
                alto
            ),
            1,
            border_radius=5
        )

        # Texto XP
        texto_xp = self.fuente_xp.render(
            (
                f"XP {experiencia}/"
                f"{experiencia_necesaria}"
            ),
            True,
            (235, 225, 255)
        )

        self.pantalla.blit(
            texto_xp,
            (
                x + 190,
                y - 4
            )
        )

    # =========================================================
    # DIBUJAR
    # =========================================================

    def dibujar(self):

        self.pantalla.fill(
            (12, 10, 18)
        )

        # Mapa
        self.pantalla.blit(
            self.fondo,
            (0, 0)
        )

        # Franja
        pygame.draw.rect(
            self.pantalla,
            (18, 14, 22),
            self.rect_franja
        )

        pygame.draw.line(
            self.pantalla,
            (190, 135, 55),
            (
                0,
                self.alto_mapa
            ),
            (
                self.ancho,
                self.alto_mapa
            ),
            2
        )

        # =====================================================
        # NIVEL
        # =====================================================

        self.dibujar_nivel()

        # =====================================================
        # REPETIR
        # =====================================================

        if (
            self.rect_repetir_goblin
            is not None
        ):

            self.dibujar_boton(
                self.rect_repetir_goblin,
                "REPETIR GOBLIN",
                secundario=True
            )

        if (
            self.rect_repetir_orco
            is not None
        ):

            self.dibujar_boton(
                self.rect_repetir_orco,
                "REPETIR ORCO",
                secundario=True
            )

        # =====================================================
        # BOTONES PRINCIPALES
        # =====================================================

        self.dibujar_boton(
            self.rect_inicio,
            "VOLVER AL INICIO"
        )

        self.dibujar_boton(
            self.rect_guardar,
            self.texto_guardar
        )

        self.dibujar_boton(
            self.rect_continuar,
            self.texto_continuar
        )

        pygame.display.flip()

    # =========================================================
    # EJECUTAR
    # =========================================================

    def ejecutar(self):

        while True:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return "salir"

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:
                        return "menu"

                if (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):

                    if self.rect_inicio.collidepoint(
                        evento.pos
                    ):
                        return "menu"

                    if self.rect_guardar.collidepoint(
                        evento.pos
                    ):
                        return "guardar"

                    if self.rect_continuar.collidepoint(
                        evento.pos
                    ):
                        return "continuar"

                    if (
                        self.rect_repetir_goblin
                        is not None
                        and
                        self.rect_repetir_goblin
                        .collidepoint(
                            evento.pos
                        )
                    ):

                        return "repetir_goblin"

                    if (
                        self.rect_repetir_orco
                        is not None
                        and
                        self.rect_repetir_orco
                        .collidepoint(
                            evento.pos
                        )
                    ):

                        return "repetir_orco"

            self.dibujar()

            self.reloj.tick(
                60
            )