from pathlib import Path
import pygame


BASE_DIR = Path(__file__).resolve().parents[2]


class PantallaProgreso:

    def __init__(
        self,
        estado,
        partida_guardada=False
    ):
        pygame.init()

        self.estado = estado

        self.ancho = 1000
        self.alto = 700

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption(
            "Arena Elemental - Progreso"
        )

        self.reloj = pygame.time.Clock()

        self.fuente_boton = pygame.font.SysFont(
            "georgia",
            16,
            bold=True
        )

        # =================================================
        # CONFIGURACIÓN DEL MAPA
        # =================================================

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

        # =================================================
        # CARGAR FONDO
        # =================================================

        imagen_original = pygame.image.load(
            str(ruta)
        ).convert()

        # Dejamos espacio inferior para controles.
        self.alto_mapa = 560

        self.fondo = pygame.transform.smoothscale(
            imagen_original,
            (
                self.ancho,
                self.alto_mapa
            )
        )

        # =================================================
        # FRANJA INFERIOR
        # =================================================

        self.rect_franja = pygame.Rect(
            0,
            self.alto_mapa,
            self.ancho,
            self.alto - self.alto_mapa
        )

        # =================================================
        # BOTONES PRINCIPALES
        # =================================================

        self.rect_inicio = pygame.Rect(
            35,
            630,
            270,
            48
        )

        self.rect_guardar = pygame.Rect(
            365,
            630,
            270,
            48
        )

        self.rect_continuar = pygame.Rect(
            695,
            630,
            270,
            48
        )

        # =================================================
        # BOTONES PARA REPETIR COMBATES
        # =================================================

        self.rect_repetir_goblin = None
        self.rect_repetir_orco = None

        # Después del Goblin:
        # se puede repetir Goblin.
        if estado == "goblin":

            self.rect_repetir_goblin = (
                pygame.Rect(
                    365,
                    575,
                    270,
                    42
                )
            )

        # Después del Orco:
        # se puede repetir Goblin u Orco.
        elif estado == "orco":

            self.rect_repetir_goblin = (
                pygame.Rect(
                    200,
                    575,
                    270,
                    42
                )
            )

            self.rect_repetir_orco = (
                pygame.Rect(
                    530,
                    575,
                    270,
                    42
                )
            )

    # =====================================================
    # DIBUJAR BOTÓN
    # =====================================================

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

        superficie = (
            self.fuente_boton.render(
                texto,
                True,
                (255, 245, 220)
            )
        )

        self.pantalla.blit(
            superficie,
            superficie.get_rect(
                center=rect.center
            )
        )

    # =====================================================
    # DIBUJAR
    # =====================================================

    def dibujar(self):

        # Fondo base
        self.pantalla.fill(
            (12, 10, 18)
        )

        # Mapa
        self.pantalla.blit(
            self.fondo,
            (0, 0)
        )

        # Franja inferior
        pygame.draw.rect(
            self.pantalla,
            (18, 14, 22),
            self.rect_franja
        )

        # Separador
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

        # =================================================
        # BOTONES PARA REPETIR
        # =================================================

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

        # =================================================
        # BOTONES PRINCIPALES
        # =================================================

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

    # =====================================================
    # EJECUTAR
    # =====================================================

    def ejecutar(self):

        while True:

            for evento in pygame.event.get():

                # =========================================
                # CERRAR VENTANA
                # =========================================

                if evento.type == pygame.QUIT:
                    return "salir"

                # =========================================
                # TECLADO
                # =========================================

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:
                        return "menu"

                # =========================================
                # CLIC
                # =========================================

                if (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):

                    # -------------------------------------
                    # VOLVER AL INICIO
                    # -------------------------------------

                    if (
                        self.rect_inicio
                        .collidepoint(
                            evento.pos
                        )
                    ):

                        return "menu"

                    # -------------------------------------
                    # GUARDAR
                    # -------------------------------------

                    if (
                        self.rect_guardar
                        .collidepoint(
                            evento.pos
                        )
                    ):

                        return "guardar"

                    # -------------------------------------
                    # CONTINUAR HISTORIA
                    # -------------------------------------

                    if (
                        self.rect_continuar
                        .collidepoint(
                            evento.pos
                        )
                    ):

                        return "continuar"

                    # -------------------------------------
                    # REPETIR GOBLIN
                    # -------------------------------------

                    if (
                        self.rect_repetir_goblin
                        is not None
                        and
                        self.rect_repetir_goblin
                        .collidepoint(
                            evento.pos
                        )
                    ):

                        return (
                            "repetir_goblin"
                        )

                    # -------------------------------------
                    # REPETIR ORCO
                    # -------------------------------------

                    if (
                        self.rect_repetir_orco
                        is not None
                        and
                        self.rect_repetir_orco
                        .collidepoint(
                            evento.pos
                        )
                    ):

                        return (
                            "repetir_orco"
                        )

            self.dibujar()

            self.reloj.tick(
                60
            )