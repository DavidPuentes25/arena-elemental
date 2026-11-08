from pathlib import Path
import pygame


BASE_DIR = Path(__file__).resolve().parents[2]


class PantallaSeleccionPersonaje:

    def __init__(self):
        pygame.init()

        self.ancho = 1000
        self.alto = 650

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption(
            "Arena Elemental - Seleccionar personaje"
        )

        self.reloj = pygame.time.Clock()

        self.fuente_titulo = pygame.font.SysFont(
            "georgia",
            34,
            bold=True
        )

        self.fuente_nombre = pygame.font.SysFont(
            "georgia",
            24,
            bold=True
        )

        self.fuente_texto = pygame.font.SysFont(
            "arial",
            16
        )

        self.fuente_boton = pygame.font.SysFont(
            "georgia",
            16,
            bold=True
        )

        # =========================================
        # PERSONAJES
        # =========================================

        self.personajes = [
            {
                "nombre": "Guerrero",
                "carpeta": "guerrero",
                "descripcion": "Fuerza y gran resistencia."
            },
            {
                "nombre": "Mago",
                "carpeta": "mago",
                "descripcion": "Poderosas habilidades mágicas."
            },
            {
                "nombre": "Arquero",
                "carpeta": "arquero",
                "descripcion": "Ataques rápidos y precisos."
            }
        ]

        self.tarjetas = []

        posiciones_x = [
            70,
            365,
            660
        ]

        for personaje, x in zip(
            self.personajes,
            posiciones_x
        ):
            tarjeta = pygame.Rect(
                x,
                150,
                270,
                390
            )

            boton = pygame.Rect(
                x + 35,
                475,
                200,
                45
            )

            imagen = self.cargar_imagen(
                personaje["carpeta"]
            )

            self.tarjetas.append(
                {
                    "personaje": personaje,
                    "rect": tarjeta,
                    "boton": boton,
                    "imagen": imagen
                }
            )

        self.rect_volver = pygame.Rect(
            30,
            585,
            210,
            42
        )

    # =============================================
    # CARGAR IMAGEN
    # =============================================

    def cargar_imagen(self, carpeta):
        ruta = (
            BASE_DIR
            / "assets"
            / "personajes"
            / carpeta
            / "idle.png"
        )

        if not ruta.exists():
            return None

        imagen = pygame.image.load(
            str(ruta)
        ).convert_alpha()

        ancho_maximo = 180
        alto_maximo = 220

        ancho = imagen.get_width()
        alto = imagen.get_height()

        escala = min(
            ancho_maximo / ancho,
            alto_maximo / alto
        )

        nuevo_ancho = int(
            ancho * escala
        )

        nuevo_alto = int(
            alto * escala
        )

        return pygame.transform.smoothscale(
            imagen,
            (
                nuevo_ancho,
                nuevo_alto
            )
        )

    # =============================================
    # BOTÓN
    # =============================================

    def dibujar_boton(
        self,
        rect,
        texto
    ):
        mouse = pygame.mouse.get_pos()

        if rect.collidepoint(mouse):
            color = (125, 75, 30)
            borde = (255, 220, 110)

        else:
            color = (65, 45, 35)
            borde = (205, 155, 70)

        pygame.draw.rect(
            self.pantalla,
            color,
            rect,
            border_radius=9
        )

        pygame.draw.rect(
            self.pantalla,
            borde,
            rect,
            2,
            border_radius=9
        )

        superficie = self.fuente_boton.render(
            texto,
            True,
            (255, 245, 215)
        )

        self.pantalla.blit(
            superficie,
            superficie.get_rect(
                center=rect.center
            )
        )

    # =============================================
    # DIBUJAR
    # =============================================

    def dibujar(self):
        self.pantalla.fill(
            (17, 14, 23)
        )

        titulo = self.fuente_titulo.render(
            "ELIGE TU PERSONAJE",
            True,
            (255, 215, 115)
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(500, 65)
            )
        )

        subtitulo = self.fuente_texto.render(
            "Cada héroe tiene habilidades diferentes.",
            True,
            (215, 215, 215)
        )

        self.pantalla.blit(
            subtitulo,
            subtitulo.get_rect(
                center=(500, 110)
            )
        )

        mouse = pygame.mouse.get_pos()

        for elemento in self.tarjetas:

            personaje = elemento[
                "personaje"
            ]

            rect = elemento[
                "rect"
            ]

            if rect.collidepoint(mouse):
                color = (55, 43, 42)
                borde = (245, 195, 90)

            else:
                color = (34, 29, 38)
                borde = (125, 95, 65)

            pygame.draw.rect(
                self.pantalla,
                color,
                rect,
                border_radius=14
            )

            pygame.draw.rect(
                self.pantalla,
                borde,
                rect,
                3,
                border_radius=14
            )

            # Nombre
            nombre = self.fuente_nombre.render(
                personaje["nombre"],
                True,
                (255, 225, 145)
            )

            self.pantalla.blit(
                nombre,
                nombre.get_rect(
                    center=(
                        rect.centerx,
                        rect.y + 38
                    )
                )
            )

            # Imagen
            imagen = elemento[
                "imagen"
            ]

            if imagen is not None:

                x_imagen = (
                    rect.centerx
                    - imagen.get_width() // 2
                )

                y_imagen = (
                    rect.y + 70
                )

                self.pantalla.blit(
                    imagen,
                    (
                        x_imagen,
                        y_imagen
                    )
                )

            # Descripción
            descripcion = (
                self.fuente_texto.render(
                    personaje[
                        "descripcion"
                    ],
                    True,
                    (220, 220, 220)
                )
            )

            self.pantalla.blit(
                descripcion,
                descripcion.get_rect(
                    center=(
                        rect.centerx,
                        rect.y + 300
                    )
                )
            )

            self.dibujar_boton(
                elemento["boton"],
                "ELEGIR"
            )

        self.dibujar_boton(
            self.rect_volver,
            "VOLVER AL INICIO"
        )

        pygame.display.flip()

    # =============================================
    # EJECUTAR
    # =============================================

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

                    if self.rect_volver.collidepoint(
                        evento.pos
                    ):
                        return "menu"

                    for elemento in self.tarjetas:

                        if elemento[
                            "boton"
                        ].collidepoint(
                            evento.pos
                        ):

                            return elemento[
                                "personaje"
                            ]["nombre"]

            self.dibujar()

            self.reloj.tick(60)