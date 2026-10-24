from pathlib import Path
import pygame


BASE_DIR = Path(__file__).resolve().parents[2]


class BotonResultado:

    def __init__(self, x, y, ancho, alto, texto, fuente):
        self.rect = pygame.Rect(
            x,
            y,
            ancho,
            alto
        )

        self.texto = texto
        self.fuente = fuente

    def dibujar(self, pantalla):

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            color = (110, 60, 20, 225)
            borde = (255, 220, 120)
        else:
            color = (55, 30, 15, 205)
            borde = (225, 170, 70)

        # Fondo transparente del botón
        superficie = pygame.Surface(
            (self.rect.width, self.rect.height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            superficie,
            color,
            superficie.get_rect(),
            border_radius=14
        )

        pantalla.blit(
            superficie,
            self.rect.topleft
        )

        # Borde
        pygame.draw.rect(
            pantalla,
            borde,
            self.rect,
            3,
            border_radius=14
        )

        # Texto
        texto = self.fuente.render(
            self.texto,
            True,
            (255, 245, 220)
        )

        pantalla.blit(
            texto,
            texto.get_rect(
                center=self.rect.center
            )
        )

    def fue_presionado(self, evento):

        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


class PantallaResultado:

    def __init__(self, resultado):

        pygame.init()

        self.ancho = 1000
        self.alto = 650

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption(
            "Arena Elemental"
        )

        self.reloj = pygame.time.Clock()

        self.resultado = resultado

        self.fuente_boton = pygame.font.SysFont(
            "georgia",
            22,
            bold=True
        )

        self.cargar_imagen()

        # Botón encima de la imagen
        if self.resultado == "victoria":

            self.boton = BotonResultado(
                350,
                565,
                300,
                60,
                "CONTINUAR",
                self.fuente_boton
            )

        else:

            self.boton = BotonResultado(
                350,
                565,
                300,
                60,
                "VOLVER AL MENÚ",
                self.fuente_boton
            )

    def cargar_imagen(self):

        if self.resultado == "victoria":

            ruta = (
                BASE_DIR
                / "assets"
                / "interfaz"
                / "victoria.png"
            )

        else:

            ruta = (
                BASE_DIR
                / "assets"
                / "interfaz"
                / "derrota.png"
            )

        if not ruta.exists():
            raise FileNotFoundError(
                f"No se encontró la imagen: {ruta}"
            )

        imagen_original = pygame.image.load(
            str(ruta)
        ).convert()

        # La imagen ocupa toda la pantalla
        self.imagen = self.escalar_cubriendo_pantalla(
            imagen_original
        )

    def escalar_cubriendo_pantalla(self, imagen):

        ancho_original = imagen.get_width()
        alto_original = imagen.get_height()

        # Escala necesaria para cubrir toda la ventana
        escala = max(
            self.ancho / ancho_original,
            self.alto / alto_original
        )

        nuevo_ancho = int(
            ancho_original * escala
        )

        nuevo_alto = int(
            alto_original * escala
        )

        imagen_escalada = pygame.transform.smoothscale(
            imagen,
            (
                nuevo_ancho,
                nuevo_alto
            )
        )

        # Recorta únicamente lo que sobresale
        superficie_final = pygame.Surface(
            (self.ancho, self.alto)
        )

        x = (
            nuevo_ancho - self.ancho
        ) // 2

        y = (
            nuevo_alto - self.alto
        ) // 2

        superficie_final.blit(
            imagen_escalada,
            (0, 0),
            (
                x,
                y,
                self.ancho,
                self.alto
            )
        )

        return superficie_final

    def dibujar(self):

        # Imagen completa
        self.pantalla.blit(
            self.imagen,
            (0, 0)
        )

        # Botón encima
        self.boton.dibujar(
            self.pantalla
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
                    return "menu"

                if self.boton.fue_presionado(
                    evento
                ):

                    if self.resultado == "victoria":
                        return "continuar"

                    return "menu"

            self.dibujar()

            self.reloj.tick(60)