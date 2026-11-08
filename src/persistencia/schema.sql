PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS personaje (
    nombre TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS enemigo (
    nombre TEXT PRIMARY KEY,
    orden INTEGER UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS objeto (
    nombre TEXT PRIMARY KEY
);

INSERT OR IGNORE INTO personaje(nombre)
VALUES
    ('Guerrero'),
    ('Mago'),
    ('Arquero');

INSERT OR IGNORE INTO enemigo(nombre, orden)
VALUES
    ('Goblin', 1),
    ('Orco', 2),
    ('Guardián Elemental', 3);

INSERT OR IGNORE INTO objeto(nombre)
VALUES
    ('Poción de Vida'),
    ('Escudo Protector');


CREATE TABLE IF NOT EXISTS partidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre_partida TEXT NOT NULL UNIQUE COLLATE NOCASE,

    nombre_jugador TEXT NOT NULL,

    personaje TEXT NOT NULL,

    siguiente_enemigo TEXT NOT NULL,

    progreso INTEGER NOT NULL DEFAULT 0
        CHECK (progreso BETWEEN 0 AND 3),

    fecha_guardado TEXT NOT NULL,

    FOREIGN KEY (personaje)
        REFERENCES personaje(nombre),

    FOREIGN KEY (siguiente_enemigo)
        REFERENCES enemigo(nombre)
);


CREATE TABLE IF NOT EXISTS inventario_partida (
    partida_id INTEGER NOT NULL,

    objeto TEXT NOT NULL,

    cantidad INTEGER NOT NULL DEFAULT 1
        CHECK (cantidad >= 0),

    PRIMARY KEY (
        partida_id,
        objeto
    ),

    FOREIGN KEY (partida_id)
        REFERENCES partidas(id)
        ON DELETE CASCADE,

    FOREIGN KEY (objeto)
        REFERENCES objeto(nombre)
);