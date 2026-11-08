import pygame


class PantallaNombrePartida:

    def __init__(self):
        pygame.init()

        self.ancho = 1000
        self.alto = 650

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption(
            "Arena Elemental - Guardar partida"
        )

        self.reloj = pygame.time.Clock()

        self.fuente_titulo = (
            pygame.font.SysFont(
                "arial",
                34,
                bold=True
            )
        )

        self.fuente = pygame.font.SysFont(
            "arial",
            22
        )

        self.fuente_boton = (
            pygame.font.SysFont(
                "georgia",
                18,
                bold=True
            )
        )

        self.nombre = ""

        self.rect_campo = pygame.Rect(
            250,
            280,
            500,
            55
        )

        self.rect_guardar = pygame.Rect(
            280,
            390,
            200,
            50
        )

        self.rect_cancelar = pygame.Rect(
            520,
            390,
            200,
            50
        )

    def dibujar_boton(
        self,
        rect,
        texto
    ):
        mouse = pygame.mouse.get_pos()

        if rect.collidepoint(mouse):
            color = (120, 75, 35)
        else:
            color = (75, 50, 35)

        pygame.draw.rect(
            self.pantalla,
            color,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            self.pantalla,
            (230, 185, 90),
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

    def dibujar(self):
        self.pantalla.fill(
            (20, 18, 28)
        )

        titulo = (
            self.fuente_titulo.render(
                "NOMBRE DE LA PARTIDA",
                True,
                (255, 215, 110)
            )
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(500, 170)
            )
        )

        pygame.draw.rect(
            self.pantalla,
            (45, 40, 50),
            self.rect_campo,
            border_radius=10
        )

        pygame.draw.rect(
            self.pantalla,
            (230, 185, 90),
            self.rect_campo,
            2,
            border_radius=10
        )

        texto_nombre = (
            self.fuente.render(
                self.nombre,
                True,
                (255, 255, 255)
            )
        )

        self.pantalla.blit(
            texto_nombre,
            (
                self.rect_campo.x + 15,
                self.rect_campo.y + 14
            )
        )

        self.dibujar_boton(
            self.rect_guardar,
            "GUARDAR"
        )

        self.dibujar_boton(
            self.rect_cancelar,
            "CANCELAR"
        )

        pygame.display.flip()

    def ejecutar(self):
        while True:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return None

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:
                        return None

                    if evento.key == pygame.K_RETURN:

                        nombre = (
                            self.nombre.strip()
                        )

                        if nombre:
                            return nombre

                    elif (
                        evento.key
                        == pygame.K_BACKSPACE
                    ):

                        self.nombre = (
                            self.nombre[:-1]
                        )

                    else:

                        if (
                            evento.unicode.isprintable()
                            and len(self.nombre) < 30
                        ):

                            self.nombre += (
                                evento.unicode
                            )

                if (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):

                    if self.rect_guardar.collidepoint(
                        evento.pos
                    ):

                        nombre = (
                            self.nombre.strip()
                        )

                        if nombre:
                            return nombre

                    if self.rect_cancelar.collidepoint(
                        evento.pos
                    ):
                        return None

            self.dibujar()
            self.reloj.tick(60)