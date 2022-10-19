from .operacion import Operacion


class OperacionActualizacion(Operacion):
    def __init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion, propiedades_cambiadas):
        Operacion.__init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion)
        self.__propiedades_cambiadas = propiedades_cambiadas

    @property
    def propiedades_cambiadas(self):
        return self.__propiedades_cambiadas

    @propiedades_cambiadas.setter
    def propiedades_cambiadas(self, propiedades_cambiadas):
        self.__propiedades_cambiadas = propiedades_cambiadas
