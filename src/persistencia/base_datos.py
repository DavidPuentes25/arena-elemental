from pathlib import Path
from datetime import datetime
import sqlite3


BASE_DIR = Path(__file__).resolve().parent


class RepositorioPartida:

    def __init__(self, ruta_bd="arena_elemental.db"):
        self.ruta_bd = ruta_bd

        self.conexion = sqlite3.connect(
            self.ruta_bd
        )

        self.conexion.row_factory = sqlite3.Row

        self.conexion.execute(
            "PRAGMA foreign_keys = ON"
        )

        self._crear_esquema()
        self._migrar_nivel_experiencia()

    # =====================================================
    # ESQUEMA
    # =====================================================

    def _crear_esquema(self):
        ruta_schema = (
            BASE_DIR
            / "schema.sql"
        )

        with open(
            ruta_schema,
            "r",
            encoding="utf-8"
        ) as archivo:
            script = archivo.read()

        self.conexion.executescript(
            script
        )

        self.conexion.commit()

    # =====================================================
    # MIGRACIÓN NIVEL / EXPERIENCIA
    # =====================================================

    def _migrar_nivel_experiencia(self):
        cursor = self.conexion.cursor()

        cursor.execute(
            "PRAGMA table_info(partidas)"
        )

        columnas = {
            fila["name"]
            for fila in cursor.fetchall()
        }

        if "nivel" not in columnas:
            cursor.execute(
                """
                ALTER TABLE partidas
                ADD COLUMN nivel INTEGER
                NOT NULL DEFAULT 1
                """
            )

        if "experiencia" not in columnas:
            cursor.execute(
                """
                ALTER TABLE partidas
                ADD COLUMN experiencia INTEGER
                NOT NULL DEFAULT 0
                """
            )

        self.conexion.commit()

    # =====================================================
    # FECHA
    # =====================================================

    def _fecha_actual(self):
        return (
            datetime.now()
            .astimezone()
            .isoformat(
                timespec="seconds"
            )
        )

    # =====================================================
    # CREAR PARTIDA
    # =====================================================

    def crear_partida(
        self,
        nombre_partida,
        nombre_jugador,
        personaje,
        siguiente_enemigo,
        progreso,
        inventario=None,
        nivel=1,
        experiencia=0
    ):
        nombre_partida = (
            nombre_partida.strip()
        )

        if not nombre_partida:
            raise ValueError(
                "El nombre de la partida "
                "no puede estar vacío."
            )

        if inventario is None:
            inventario = {}

        cursor = self.conexion.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO partidas (
                    nombre_partida,
                    nombre_jugador,
                    personaje,
                    siguiente_enemigo,
                    progreso,
                    nivel,
                    experiencia,
                    fecha_guardado
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    nombre_partida,
                    nombre_jugador,
                    personaje,
                    siguiente_enemigo,
                    progreso,
                    nivel,
                    experiencia,
                    self._fecha_actual()
                )
            )

            partida_id = (
                cursor.lastrowid
            )

            self._guardar_inventario(
                cursor,
                partida_id,
                inventario
            )

            self.conexion.commit()

            return partida_id

        except sqlite3.IntegrityError as error:
            self.conexion.rollback()

            raise ValueError(
                "No se pudo crear la partida. "
                "Puede que ya exista una partida "
                "con ese nombre."
            ) from error

    # =====================================================
    # ACTUALIZAR PARTIDA
    # =====================================================

    def actualizar_partida(
        self,
        partida_id,
        nombre_jugador,
        personaje,
        siguiente_enemigo,
        progreso,
        inventario=None,
        nivel=1,
        experiencia=0
    ):
        if inventario is None:
            inventario = {}

        cursor = self.conexion.cursor()

        cursor.execute(
            """
            UPDATE partidas

            SET
                nombre_jugador = ?,
                personaje = ?,
                siguiente_enemigo = ?,
                progreso = ?,
                nivel = ?,
                experiencia = ?,
                fecha_guardado = ?

            WHERE id = ?
            """,
            (
                nombre_jugador,
                personaje,
                siguiente_enemigo,
                progreso,
                nivel,
                experiencia,
                self._fecha_actual(),
                partida_id
            )
        )

        if cursor.rowcount == 0:
            raise ValueError(
                "La partida no existe."
            )

        self._guardar_inventario(
            cursor,
            partida_id,
            inventario
        )

        self.conexion.commit()

    # =====================================================
    # GUARDAR INVENTARIO
    # =====================================================

    def _guardar_inventario(
        self,
        cursor,
        partida_id,
        inventario
    ):
        cursor.execute(
            """
            DELETE FROM inventario_partida
            WHERE partida_id = ?
            """,
            (partida_id,)
        )

        for objeto, cantidad in (
            inventario.items()
        ):
            if cantidad <= 0:
                continue

            cursor.execute(
                """
                INSERT INTO inventario_partida (
                    partida_id,
                    objeto,
                    cantidad
                )
                VALUES (?, ?, ?)
                """,
                (
                    partida_id,
                    objeto,
                    cantidad
                )
            )

    # =====================================================
    # CARGAR INVENTARIO
    # =====================================================

    def _cargar_inventario(
        self,
        partida_id
    ):
        cursor = self.conexion.cursor()

        cursor.execute(
            """
            SELECT
                objeto,
                cantidad

            FROM inventario_partida

            WHERE partida_id = ?
            """,
            (partida_id,)
        )

        inventario = {}

        for fila in cursor.fetchall():
            inventario[
                fila["objeto"]
            ] = fila["cantidad"]

        return inventario

    # =====================================================
    # CARGAR PARTIDA
    # =====================================================

    def cargar(
        self,
        partida_id
    ):
        cursor = self.conexion.cursor()

        cursor.execute(
            """
            SELECT
                id,
                nombre_partida,
                nombre_jugador,
                personaje,
                siguiente_enemigo,
                progreso,
                nivel,
                experiencia,
                fecha_guardado

            FROM partidas

            WHERE id = ?
            """,
            (partida_id,)
        )

        fila = cursor.fetchone()

        if fila is None:
            return None

        return {
            "id": fila["id"],

            "nombre_partida":
                fila["nombre_partida"],

            "nombre_jugador":
                fila["nombre_jugador"],

            "personaje":
                fila["personaje"],

            "siguiente_enemigo":
                fila["siguiente_enemigo"],

            "progreso":
                fila["progreso"],

            "nivel":
                fila["nivel"],

            "experiencia":
                fila["experiencia"],

            "fecha_guardado":
                fila["fecha_guardado"],

            "inventario":
                self._cargar_inventario(
                    fila["id"]
                )
        }

    # =====================================================
    # LISTAR PARTIDAS
    # =====================================================

    def listar_partidas(self):
        cursor = self.conexion.cursor()

        cursor.execute(
            """
            SELECT
                id,
                nombre_partida,
                nombre_jugador,
                personaje,
                siguiente_enemigo,
                progreso,
                nivel,
                experiencia,
                fecha_guardado

            FROM partidas

            ORDER BY fecha_guardado DESC
            """
        )

        partidas = []

        for fila in cursor.fetchall():
            partidas.append(
                {
                    "id":
                        fila["id"],

                    "nombre_partida":
                        fila["nombre_partida"],

                    "nombre_jugador":
                        fila["nombre_jugador"],

                    "personaje":
                        fila["personaje"],

                    "siguiente_enemigo":
                        fila["siguiente_enemigo"],

                    "progreso":
                        fila["progreso"],

                    "nivel":
                        fila["nivel"],

                    "experiencia":
                        fila["experiencia"],

                    "fecha_guardado":
                        fila["fecha_guardado"]
                }
            )

        return partidas

    # =====================================================
    # EXISTEN PARTIDAS
    # =====================================================

    def existe_partida(self):
        cursor = self.conexion.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM partidas
            """
        )

        fila = cursor.fetchone()

        return fila["total"] > 0

    # =====================================================
    # ELIMINAR PARTIDA
    # =====================================================

    def eliminar(
        self,
        partida_id
    ):
        cursor = self.conexion.cursor()

        cursor.execute(
            """
            DELETE FROM partidas
            WHERE id = ?
            """,
            (partida_id,)
        )

        self.conexion.commit()

    # =====================================================
    # RENOMBRAR PARTIDA
    # =====================================================

    def renombrar(
        self,
        partida_id,
        nuevo_nombre
    ):
        nuevo_nombre = (
            nuevo_nombre.strip()
        )

        if not nuevo_nombre:
            return False

        try:
            self.conexion.execute(
                """
                UPDATE partidas

                SET
                    nombre_partida = ?,
                    fecha_guardado = ?

                WHERE id = ?
                """,
                (
                    nuevo_nombre,
                    self._fecha_actual(),
                    partida_id
                )
            )

            self.conexion.commit()

            return True

        except sqlite3.IntegrityError:
            self.conexion.rollback()

            return False

    # =====================================================
    # CERRAR
    # =====================================================

    def cerrar(self):
        self.conexion.close()