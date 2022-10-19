from .operacion import Operacion


class OperacionAlta(Operacion):
    def __init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion, medio_creado):
        Operacion.__init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion)
        self.__medio_creado = medio_creado

    @property
    def medio_creado(self):
        return self.__medio_creado

    @medio_creado.setter
    def medio_creado(self, medio_creado):
        self.__medio_creado = medio_creado
