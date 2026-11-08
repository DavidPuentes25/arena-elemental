from pathlib import Path
import pygame


BASE_DIR = Path(__file__).resolve().parents[2]


class PantallaProgreso:

    def __init__(self, estado, partida_guardada=False):
        pygame.init()

        self.estado = estado
        self.ancho = 1000
        self.alto = 650
        self.alto_mapa = 563

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption(
            "Arena Elemental - Progreso"
        )

        self.reloj = pygame.time.Clock()

        self.fuente_boton = pygame.font.SysFont(
            "georgia",
            17,
            bold=True
        )

        # =========================================
        # CONFIGURACIÓN SEGÚN PROGRESO
        # =========================================

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

        # =========================================
        # CARGAR IMAGEN
        # =========================================

        imagen_original = pygame.image.load(
            str(ruta)
        ).convert()

        self.fondo = pygame.transform.smoothscale(
            imagen_original,
            (
                self.ancho,
                self.alto_mapa
            )
        )

        # =========================================
        # FRANJA INFERIOR
        # =========================================

        self.rect_franja = pygame.Rect(
            0,
            self.alto_mapa,
            self.ancho,
            self.alto - self.alto_mapa
        )

        # =========================================
        # BOTONES
        # =========================================

        self.rect_inicio = pygame.Rect(
            55,
            580,
            260,
            50
        )

        self.rect_guardar = pygame.Rect(
            370,
            580,
            260,
            50
        )

        self.rect_continuar = pygame.Rect(
            685,
            580,
            260,
            50
        )

    def dibujar_boton(self, rect, texto):
        mouse = pygame.mouse.get_pos()

        if rect.collidepoint(mouse):
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
            3,
            border_radius=10
        )

        superficie = self.fuente_boton.render(
            texto,
            True,
            (255, 240, 190)
        )

        self.pantalla.blit(
            superficie,
            superficie.get_rect(
                center=rect.center
            )
        )

    def dibujar(self):
        self.pantalla.fill(
            (12, 10, 18)
        )

        self.pantalla.blit(
            self.fondo,
            (0, 0)
        )

        pygame.draw.rect(
            self.pantalla,
            (18, 14, 20),
            self.rect_franja
        )

        pygame.draw.line(
            self.pantalla,
            (190, 135, 55),
            (0, self.alto_mapa),
            (self.ancho, self.alto_mapa),
            2
        )

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

    def ejecutar(self):
        while True:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return "salir"

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:
                        return "menu"

                if (
                    evento.type == pygame.MOUSEBUTTONDOWN
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

            self.dibujar()

            self.reloj.tick(60)