"""Persistencia de Arena Elemental con SQLite (RF-19 a RF-22, RF-25, RNF-12)."""
import sqlite3
from pathlib import Path

RUTA_ESQUEMA = Path(__file__).parent / "schema.sql"  # ruta relativa (RNF-33)
PERSONAJES = ("Guerrero", "Mago", "Arquero")
ENEMIGOS = ("Goblin", "Orco", "Guardián Elemental")
OBJETOS = ("Poción de Vida", "Escudo Protector")


class RepositorioPartida:
    """Guarda, carga y elimina la única partida activa."""

    def __init__(self, ruta_bd="arena_elemental.db"):
        self._conn = sqlite3.connect(ruta_bd)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(RUTA_ESQUEMA.read_text(encoding="utf-8"))

    def existe_partida(self):
        """Determina si 'Continuar partida' debe estar habilitado (RF-01)."""
        return self.cargar() is not None

    def guardar(self, nombre, personaje, siguiente_enemigo, inventario):
        """Reemplaza el guardado actual. 'inventario' es {objeto: cantidad} (RF-20)."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del jugador no puede estar vacío.")
        if personaje not in PERSONAJES:
            raise ValueError(f"Personaje no válido: {personaje}")
        if siguiente_enemigo not in ENEMIGOS[1:]:
            raise ValueError("Solo se guarda progreso con Orco o Guardián Elemental como siguiente.")
        for objeto, cantidad in inventario.items():
            if objeto not in OBJETOS or cantidad < 0:
                raise ValueError(f"Inventario no válido: {objeto}={cantidad}")

        with self._conn:  # transacción: o se guarda todo o nada
            self._conn.execute("DELETE FROM partida WHERE id = 1")
            self._conn.execute(
                "INSERT INTO partida (id, nombre_jugador, personaje, siguiente_enemigo) "
                "VALUES (1, ?, ?, ?)",
                (nombre.strip(), personaje, siguiente_enemigo),
            )
            for objeto in OBJETOS:
                self._conn.execute(
                    "INSERT INTO inventario (partida_id, objeto, cantidad) VALUES (1, ?, ?)",
                    (objeto, inventario.get(objeto, 0)),
                )

    def cargar(self):
        """Devuelve un dict con la partida o None si no existe o es inválida (RF-21, RNF-12)."""
        try:
            fila = self._conn.execute(
                "SELECT nombre_jugador, personaje, siguiente_enemigo FROM partida WHERE id = 1"
            ).fetchone()
            if fila is None:
                return None
            inventario = dict(self._conn.execute(
                "SELECT objeto, cantidad FROM inventario WHERE partida_id = 1"
            ).fetchall())
        except sqlite3.Error:
            return None
        return {
            "nombre": fila[0],
            "personaje": fila[1],
            "siguiente_enemigo": fila[2],
            "inventario": {o: inventario.get(o, 0) for o in OBJETOS},
        }

    def eliminar(self):
        """Borra el progreso tras una derrota (RF-22). El inventario cae en cascada."""
        with self._conn:
            self._conn.execute("DELETE FROM partida WHERE id = 1")

    def cerrar(self):
        self._conn.close()


if __name__ == "__main__":
    repo = RepositorioPartida(":memory:")
    print("¿Hay partida?", repo.existe_partida())
    repo.guardar("Ana", "Mago", "Orco", {"Poción de Vida": 1})
    print(repo.cargar())
    repo.guardar("Ana", "Mago", "Guardián Elemental", {"Poción de Vida": 1, "Escudo Protector": 1})
    print(repo.cargar())
    repo.eliminar()
    print("Tras derrota:", repo.cargar())
    repo.cerrar()
