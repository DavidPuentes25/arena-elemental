import pygame


class PantallaRecompensa:
    def __init__(self):
        pygame.init()

        self.ancho = 1000
        self.alto = 650

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption(
            "Arena Elemental - Recompensa"
        )

        self.reloj = pygame.time.Clock()

        self.fuente_titulo = pygame.font.SysFont(
            "arial",
            36,
            bold=True
        )

        self.fuente = pygame.font.SysFont(
            "arial",
            22,
            bold=True
        )

        self.fuente_pequena = pygame.font.SysFont(
            "arial",
            17
        )

        self.rect_pocion = pygame.Rect(
            180,
            250,
            280,
            180
        )

        self.rect_escudo = pygame.Rect(
            540,
            250,
            280,
            180
        )

    def dibujar_tarjeta(
        self,
        rect,
        titulo,
        descripcion,
        mouse
    ):
        if rect.collidepoint(mouse):
            color = (105, 70, 35)
            borde = (255, 220, 120)
        else:
            color = (55, 40, 30)
            borde = (210, 165, 80)

        pygame.draw.rect(
            self.pantalla,
            color,
            rect,
            border_radius=18
        )

        pygame.draw.rect(
            self.pantalla,
            borde,
            rect,
            3,
            border_radius=18
        )

        texto_titulo = self.fuente.render(
            titulo,
            True,
            (255, 235, 170)
        )

        self.pantalla.blit(
            texto_titulo,
            texto_titulo.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 45
                )
            )
        )

        texto_desc = self.fuente_pequena.render(
            descripcion,
            True,
            (235, 235, 235)
        )

        self.pantalla.blit(
            texto_desc,
            texto_desc.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 105
                )
            )
        )

        texto_elegir = self.fuente_pequena.render(
            "CLICK PARA ELEGIR",
            True,
            (255, 210, 120)
        )

        self.pantalla.blit(
            texto_elegir,
            texto_elegir.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 145
                )
            )
        )

    def dibujar(self):
        self.pantalla.fill(
            (18, 18, 28)
        )

        titulo = self.fuente_titulo.render(
            "¡VICTORIA!",
            True,
            (255, 215, 90)
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(500, 90)
            )
        )

        subtitulo = self.fuente.render(
            "Elige una recompensa",
            True,
            (240, 240, 240)
        )

        self.pantalla.blit(
            subtitulo,
            subtitulo.get_rect(
                center=(500, 155)
            )
        )

        mouse = pygame.mouse.get_pos()

        self.dibujar_tarjeta(
            self.rect_pocion,
            "POCIÓN DE VIDA",
            "Recupera 30 HP",
            mouse
        )

        self.dibujar_tarjeta(
            self.rect_escudo,
            "ESCUDO PROTECTOR",
            "-30% daño durante 5 ataques",
            mouse
        )

        mensaje = self.fuente_pequena.render(
            "La recompensa será guardada en tu inventario.",
            True,
            (180, 180, 180)
        )

        self.pantalla.blit(
            mensaje,
            mensaje.get_rect(
                center=(500, 505)
            )
        )

        pygame.display.flip()

    def ejecutar(self):
        while True:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return "salir"

                if (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):

                    if self.rect_pocion.collidepoint(
                        evento.pos
                    ):
                        return "pocion"

                    if self.rect_escudo.collidepoint(
                        evento.pos
                    ):
                        return "escudo"

            self.dibujar()

            self.reloj.tick(60)