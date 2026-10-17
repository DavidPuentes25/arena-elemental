-- Arena Elemental - Esquema SQLite (SRS Rev. 1.2)
-- RF-19, RF-20, RF-21, RF-22, RF-23, RF-25 / RNF-12

PRAGMA foreign_keys = ON;

-- Catálogo de personajes jugables (RF-02)
CREATE TABLE IF NOT EXISTS personaje (
    nombre TEXT PRIMARY KEY
);

-- Catálogo de enemigos con su orden fijo de aparición (RF-23)
CREATE TABLE IF NOT EXISTS enemigo (
    nombre TEXT    PRIMARY KEY,
    orden  INTEGER NOT NULL UNIQUE CHECK (orden BETWEEN 1 AND 3)
);

-- Catálogo de objetos del inventario (RF-08, RF-24)
CREATE TABLE IF NOT EXISTS objeto (
    nombre TEXT PRIMARY KEY
);

-- Partida guardada. Solo existe una activa (RNF-04), por eso id = 1.
CREATE TABLE IF NOT EXISTS partida (
    id                INTEGER PRIMARY KEY CHECK (id = 1),
    nombre_jugador    TEXT NOT NULL CHECK (length(trim(nombre_jugador)) > 0),
    personaje         TEXT NOT NULL REFERENCES personaje(nombre),
    siguiente_enemigo TEXT NOT NULL REFERENCES enemigo(nombre),
    fecha_guardado    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Inventario asociado a la partida (RF-25)
CREATE TABLE IF NOT EXISTS inventario (
    partida_id INTEGER NOT NULL REFERENCES partida(id) ON DELETE CASCADE,
    objeto     TEXT    NOT NULL REFERENCES objeto(nombre),
    cantidad   INTEGER NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    PRIMARY KEY (partida_id, objeto)
);

-- Datos fijos del documento
INSERT OR IGNORE INTO personaje (nombre) VALUES ('Guerrero'), ('Mago'), ('Arquero');

INSERT OR IGNORE INTO enemigo (nombre, orden) VALUES
    ('Goblin', 1), ('Orco', 2), ('Guardián Elemental', 3);

INSERT OR IGNORE INTO objeto (nombre) VALUES ('Poción de Vida'), ('Escudo Protector');
