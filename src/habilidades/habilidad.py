class Habilidad:
    def __init__(self, nombre, descripcion, cooldown, efecto):
        self.nombre = nombre
        self.descripcion = descripcion
        self.cooldown_maximo = cooldown
        self.cooldown_actual = 0
        self.efecto = efecto

    @property
    def disponible(self):
        return self.cooldown_actual == 0

    def usar(self, personaje, objetivo):
        if not self.disponible:
            return None

        resultado = self.efecto(personaje, objetivo)
        if resultado is None:
            return None

        self.cooldown_actual = self.cooldown_maximo
        return resultado

    def avanzar_turno(self):
        if self.cooldown_actual > 0:
            self.cooldown_actual -= 1