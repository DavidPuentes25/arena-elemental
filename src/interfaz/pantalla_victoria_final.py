from pathlib import Path
import pygame


BASE_DIR = Path(__file__).resolve().parents[2]


class PantallaVictoriaFinal:

    def __init__(self):
        pygame.init()

        # =====================================================
        # VENTANA
        # =====================================================

        self.ancho = 1000
        self.alto = 700

        self.alto_imagen = 562
        self.alto_panel = (
            self.alto - self.alto_imagen
        )

        self.pantalla = pygame.display.set_mode(
            (
                self.ancho,
                self.alto
            )
        )

        pygame.display.set_caption(
            "Arena Elemental - Victoria Final"
        )

        self.reloj = pygame.time.Clock()

        # =====================================================
        # FUENTES
        # =====================================================

        self.fuente_boton = pygame.font.SysFont(
            "georgia",
            18,
            bold=True
        )

        self.fuente_mensaje = pygame.font.SysFont(
            "georgia",
            16,
            bold=True
        )

        # =====================================================
        # IMAGEN FINAL
        # =====================================================

        ruta = (
            BASE_DIR
            / "assets"
            / "interfaz"
            / "victoria_final.png"
        )

        imagen_original = pygame.image.load(
            str(ruta)
        ).convert()

        # La imagen original es panorámica.
        # La escalamos sin ocupar la zona de botones.
        self.fondo = pygame.transform.smoothscale(
            imagen_original,
            (
                self.ancho,
                self.alto_imagen
            )
        )

        # =====================================================
        # PANEL INFERIOR
        # =====================================================

        self.rect_panel = pygame.Rect(
            0,
            self.alto_imagen,
            self.ancho,
            self.alto_panel
        )

        # =====================================================
        # BOTONES
        # =====================================================

        self.rect_jugar = pygame.Rect(
            175,
            620,
            280,
            52
        )

        self.rect_menu = pygame.Rect(
            545,
            620,
            280,
            52
        )

    # =========================================================
    # DIBUJAR BOTÓN
    # =========================================================

    def dibujar_boton(
        self,
        rect,
        texto
    ):
        mouse = pygame.mouse.get_pos()

        if rect.collidepoint(mouse):

            color = (
                120,
                70,
                25
            )

            borde = (
                255,
                225,
                110
            )

        else:

            color = (
                55,
                35,
                30
            )

            borde = (
                215,
                165,
                70
            )

        pygame.draw.rect(
            self.pantalla,
            color,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            self.pantalla,
            borde,
            rect,
            2,
            border_radius=12
        )

        texto_render = (
            self.fuente_boton.render(
                texto,
                True,
                (
                    255,
                    245,
                    220
                )
            )
        )

        self.pantalla.blit(
            texto_render,
            texto_render.get_rect(
                center=rect.center
            )
        )

    # =========================================================
    # DIBUJAR
    # =========================================================

    def dibujar(self):

        # Fondo general
        self.pantalla.fill(
            (
                12,
                10,
                18
            )
        )

        # =====================================================
        # IMAGEN DE VICTORIA
        # =====================================================

        self.pantalla.blit(
            self.fondo,
            (
                0,
                0
            )
        )

        # =====================================================
        # PANEL INFERIOR
        # =====================================================

        pygame.draw.rect(
            self.pantalla,
            (
                20,
                15,
                22
            ),
            self.rect_panel
        )

        # Línea dorada divisoria
        pygame.draw.line(
            self.pantalla,
            (
                215,
                165,
                70
            ),
            (
                0,
                self.alto_imagen
            ),
            (
                self.ancho,
                self.alto_imagen
            ),
            2
        )

        # =====================================================
        # MENSAJE
        # =====================================================

        mensaje = (
            self.fuente_mensaje.render(
                "¡Has completado Arena Elemental!",
                True,
                (
                    255,
                    220,
                    140
                )
            )
        )

        self.pantalla.blit(
            mensaje,
            mensaje.get_rect(
                center=(
                    self.ancho // 2,
                    592
                )
            )
        )

        # =====================================================
        # BOTONES
        # =====================================================

        self.dibujar_boton(
            self.rect_jugar,
            "JUGAR DE NUEVO"
        )

        self.dibujar_boton(
            self.rect_menu,
            "VOLVER AL MENÚ"
        )

        pygame.display.flip()

    # =========================================================
    # EJECUTAR
    # =========================================================

    def ejecutar(self):

        while True:

            for evento in pygame.event.get():

                # Cerrar ventana
                if evento.type == pygame.QUIT:
                    return "salir"

                # Escape
                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:
                        return "menu"

                # Clic
                if (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):

                    if self.rect_jugar.collidepoint(
                        evento.pos
                    ):
                        return "jugar"

                    if self.rect_menu.collidepoint(
                        evento.pos
                    ):
                        return "menu"

            self.dibujar()

            self.reloj.tick(
                60
            )