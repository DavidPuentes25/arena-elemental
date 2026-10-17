from pathlib import Path
import pygame


BASE_DIR = Path(__file__).resolve().parents[2]


class BotonMenu:

    def __init__(
        self,
        x,
        y,
        ancho,
        alto,
        texto,
        fuente,
        habilitado=True
    ):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.fuente = fuente
        self.habilitado = habilitado

    def dibujar(self, pantalla):

        mouse = pygame.mouse.get_pos()

        if not self.habilitado:
            color = (45, 45, 45, 220)
            borde = (105, 105, 105)
            color_texto = (145, 145, 145)

        elif self.rect.collidepoint(mouse):
            color = (130, 75, 25, 235)
            borde = (255, 215, 110)
            color_texto = (255, 255, 255)

        else:
            color = (65, 38, 20, 225)
            borde = (220, 165, 70)
            color_texto = (245, 235, 210)

        superficie = pygame.Surface(
            (self.rect.width, self.rect.height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            superficie,
            color,
            superficie.get_rect(),
            border_radius=12
        )

        pantalla.blit(
            superficie,
            self.rect.topleft
        )

        pygame.draw.rect(
            pantalla,
            borde,
            self.rect,
            3,
            border_radius=12
        )

        texto = self.fuente.render(
            self.texto,
            True,
            color_texto
        )

        pantalla.blit(
            texto,
            texto.get_rect(center=self.rect.center)
        )

    def fue_presionado(self, evento):

        if not self.habilitado:
            return False

        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


class PantallaInicio:

    def __init__(self, partida_disponible=False):

        pygame.init()

        self.ancho = 1000
        self.alto = 650

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption("Arena Elemental")

        self.reloj = pygame.time.Clock()

        self.partida_disponible = partida_disponible

        self.fuente_boton = pygame.font.SysFont(
            "georgia",
            22,
            bold=True
        )

        self.fuente_pequena = pygame.font.SysFont(
            "arial",
            14
        )

        self.cargar_fondo()

        ancho_boton = 300
        alto_boton = 55

        x = (self.ancho - ancho_boton) // 2

        self.boton_jugar = BotonMenu(
            x,
            425,
            ancho_boton,
            alto_boton,
            "NUEVA PARTIDA",
            self.fuente_boton
        )

        self.boton_cargar = BotonMenu(
            x,
            495,
            ancho_boton,
            alto_boton,
            "CARGAR PARTIDA",
            self.fuente_boton,
            habilitado=self.partida_disponible
        )

        self.boton_salir = BotonMenu(
            420,
            575,
            160,
            45,
            "SALIR",
            self.fuente_boton
        )

    def cargar_fondo(self):

        ruta = (
            BASE_DIR
            / "assets"
            / "fondos"
            / "pantalla_inicio.png"
        )

        if not ruta.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen: {ruta}"
            )

        fondo_original = pygame.image.load(
            str(ruta)
        ).convert()

        self.fondo = pygame.transform.smoothscale(
            fondo_original,
            (self.ancho, self.alto)
        )

    def dibujar_panel(self):

        panel_rect = pygame.Rect(
            310,
            405,
            380,
            225
        )

        panel = pygame.Surface(
            (panel_rect.width, panel_rect.height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            panel,
            (10, 8, 8, 125),
            panel.get_rect(),
            border_radius=18
        )

        pygame.draw.rect(
            panel,
            (190, 140, 60, 120),
            panel.get_rect(),
            2,
            border_radius=18
        )

        self.pantalla.blit(
            panel,
            panel_rect.topleft
        )

    def dibujar(self):

        self.pantalla.blit(
            self.fondo,
            (0, 0)
        )

        self.dibujar_panel()

        self.boton_jugar.dibujar(
            self.pantalla
        )

        self.boton_cargar.dibujar(
            self.pantalla
        )

        self.boton_salir.dibujar(
            self.pantalla
        )

        if not self.partida_disponible:

            mensaje = self.fuente_pequena.render(
                "No existe una partida guardada",
                True,
                (210, 205, 195)
            )

            self.pantalla.blit(
                mensaje,
                mensaje.get_rect(
                    center=(500, 558)
                )
            )

        pygame.display.flip()

    def ejecutar(self):

        while True:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return "salir"

                if (
                    evento.type == pygame.KEYDOWN
                    and evento.key == pygame.K_ESCAPE
                ):
                    return "salir"

                if self.boton_jugar.fue_presionado(evento):
                    return "jugar"

                if self.boton_cargar.fue_presionado(evento):
                    return "cargar"

                if self.boton_salir.fue_presionado(evento):
                    return "salir"

            self.dibujar()

            self.reloj.tick(60)