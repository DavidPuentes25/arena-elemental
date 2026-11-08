from datetime import datetime
import pygame


class PantallaCargarPartida:

    def __init__(self, partidas):
        pygame.init()

        self.partidas = partidas

        self.ancho = 1000
        self.alto = 650

        self.pantalla = pygame.display.set_mode(
            (self.ancho, self.alto)
        )

        pygame.display.set_caption(
            "Arena Elemental - Cargar partida"
        )

        self.reloj = pygame.time.Clock()

        self.fuente_titulo = pygame.font.SysFont(
            "arial",
            32,
            bold=True
        )

        self.fuente_nombre = pygame.font.SysFont(
            "arial",
            20,
            bold=True
        )

        self.fuente = pygame.font.SysFont(
            "arial",
            15
        )

        self.fuente_boton = pygame.font.SysFont(
            "arial",
            14,
            bold=True
        )

        # =========================================
        # TARJETAS
        # =========================================

        self.tarjetas = []

        y = 105

        for partida in self.partidas[:5]:

            rect_tarjeta = pygame.Rect(
                80,
                y,
                840,
                82
            )

            rect_cargar = pygame.Rect(
                760,
                y + 10,
                135,
                27
            )

            rect_eliminar = pygame.Rect(
                760,
                y + 45,
                135,
                27
            )

            self.tarjetas.append(
                {
                    "partida": partida,
                    "tarjeta": rect_tarjeta,
                    "cargar": rect_cargar,
                    "eliminar": rect_eliminar
                }
            )

            y += 92

        # =========================================
        # VOLVER
        # =========================================

        self.rect_volver = pygame.Rect(
            400,
            585,
            200,
            42
        )

        # =========================================
        # CONFIRMACIÓN DE ELIMINACIÓN
        # =========================================

        self.partida_a_eliminar = None

        self.rect_confirmar_si = pygame.Rect(
            340,
            370,
            140,
            45
        )

        self.rect_confirmar_no = pygame.Rect(
            520,
            370,
            140,
            45
        )

    # =============================================
    # FECHA
    # =============================================

    def formatear_fecha(self, fecha):
        try:
            fecha_obj = datetime.fromisoformat(
                fecha
            )

            return fecha_obj.strftime(
                "%d/%m/%Y - %I:%M %p"
            )

        except ValueError:
            return fecha

    # =============================================
    # BOTÓN
    # =============================================

    def dibujar_boton(
        self,
        rect,
        texto,
        tipo="normal"
    ):
        mouse = pygame.mouse.get_pos()

        hover = rect.collidepoint(mouse)

        if tipo == "eliminar":

            color = (
                (125, 45, 45)
                if hover
                else (85, 35, 35)
            )

            borde = (210, 90, 90)

        else:

            color = (
                (115, 75, 35)
                if hover
                else (70, 50, 38)
            )

            borde = (220, 175, 85)

        pygame.draw.rect(
            self.pantalla,
            color,
            rect,
            border_radius=7
        )

        pygame.draw.rect(
            self.pantalla,
            borde,
            rect,
            2,
            border_radius=7
        )

        superficie = self.fuente_boton.render(
            texto,
            True,
            (255, 245, 225)
        )

        self.pantalla.blit(
            superficie,
            superficie.get_rect(
                center=rect.center
            )
        )

    # =============================================
    # PANTALLA PRINCIPAL
    # =============================================

    def dibujar(self):
        self.pantalla.fill(
            (18, 18, 28)
        )

        titulo = self.fuente_titulo.render(
            "CARGAR PARTIDA",
            True,
            (255, 220, 130)
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(500, 52)
            )
        )

        mouse = pygame.mouse.get_pos()

        # =========================================
        # PARTIDAS
        # =========================================

        for elemento in self.tarjetas:

            partida = elemento["partida"]
            rect = elemento["tarjeta"]

            if rect.collidepoint(mouse):
                color = (55, 45, 45)
            else:
                color = (38, 34, 40)

            pygame.draw.rect(
                self.pantalla,
                color,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                self.pantalla,
                (145, 110, 70),
                rect,
                2,
                border_radius=12
            )

            # Nombre partida
            nombre = self.fuente_nombre.render(
                partida["nombre_partida"],
                True,
                (255, 235, 180)
            )

            self.pantalla.blit(
                nombre,
                (
                    rect.x + 20,
                    rect.y + 10
                )
            )

            # Información
            detalle = (
                f"Personaje: "
                f"{partida['personaje']}   |   "
                f"Próximo: "
                f"{partida['siguiente_enemigo']}"
            )

            texto_detalle = self.fuente.render(
                detalle,
                True,
                (225, 225, 225)
            )

            self.pantalla.blit(
                texto_detalle,
                (
                    rect.x + 20,
                    rect.y + 39
                )
            )

            # Fecha
            fecha = self.formatear_fecha(
                partida["fecha_guardado"]
            )

            texto_fecha = self.fuente.render(
                fecha,
                True,
                (175, 175, 175)
            )

            self.pantalla.blit(
                texto_fecha,
                (
                    rect.x + 430,
                    rect.y + 16
                )
            )

            # Botones
            self.dibujar_boton(
                elemento["cargar"],
                "CARGAR"
            )

            self.dibujar_boton(
                elemento["eliminar"],
                "ELIMINAR",
                tipo="eliminar"
            )

        # =========================================
        # VOLVER
        # =========================================

        self.dibujar_boton(
            self.rect_volver,
            "VOLVER AL INICIO"
        )

        # =========================================
        # CONFIRMACIÓN
        # =========================================

        if self.partida_a_eliminar is not None:
            self.dibujar_confirmacion()

        pygame.display.flip()

    # =============================================
    # CONFIRMACIÓN
    # =============================================

    def dibujar_confirmacion(self):

        # Oscurecer fondo
        capa = pygame.Surface(
            (self.ancho, self.alto),
            pygame.SRCALPHA
        )

        capa.fill(
            (0, 0, 0, 180)
        )

        self.pantalla.blit(
            capa,
            (0, 0)
        )

        panel = pygame.Rect(
            250,
            230,
            500,
            220
        )

        pygame.draw.rect(
            self.pantalla,
            (35, 30, 35),
            panel,
            border_radius=15
        )

        pygame.draw.rect(
            self.pantalla,
            (200, 145, 70),
            panel,
            3,
            border_radius=15
        )

        titulo = self.fuente_nombre.render(
            "¿ELIMINAR PARTIDA?",
            True,
            (255, 210, 120)
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(500, 270)
            )
        )

        nombre = self.partida_a_eliminar[
            "nombre_partida"
        ]

        mensaje = self.fuente.render(
            f'Se eliminará "{nombre}" permanentemente.',
            True,
            (235, 235, 235)
        )

        self.pantalla.blit(
            mensaje,
            mensaje.get_rect(
                center=(500, 320)
            )
        )

        self.dibujar_boton(
            self.rect_confirmar_si,
            "SÍ, ELIMINAR",
            tipo="eliminar"
        )

        self.dibujar_boton(
            self.rect_confirmar_no,
            "CANCELAR"
        )

    # =============================================
    # EJECUTAR
    # =============================================

    def ejecutar(self):

        while True:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    return (
                        "salir",
                        None
                    )

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:

                        if self.partida_a_eliminar:
                            self.partida_a_eliminar = None

                        else:
                            return (
                                "volver",
                                None
                            )

                if (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):

                    # =====================================
                    # CONFIRMACIÓN ABIERTA
                    # =====================================

                    if self.partida_a_eliminar:

                        if (
                            self.rect_confirmar_si
                            .collidepoint(evento.pos)
                        ):

                            return (
                                "eliminar",
                                self.partida_a_eliminar[
                                    "id"
                                ]
                            )

                        if (
                            self.rect_confirmar_no
                            .collidepoint(evento.pos)
                        ):

                            self.partida_a_eliminar = None

                        continue

                    # =====================================
                    # PARTIDAS
                    # =====================================

                    for elemento in self.tarjetas:

                        partida = elemento[
                            "partida"
                        ]

                        if (
                            elemento["cargar"]
                            .collidepoint(evento.pos)
                        ):

                            return (
                                "cargar",
                                partida["id"]
                            )

                        if (
                            elemento["eliminar"]
                            .collidepoint(evento.pos)
                        ):

                            self.partida_a_eliminar = (
                                partida
                            )

                            break

                    # =====================================
                    # VOLVER
                    # =====================================

                    if (
                        self.rect_volver
                        .collidepoint(evento.pos)
                    ):

                        return (
                            "volver",
                            None
                        )

            self.dibujar()

            self.reloj.tick(60)