from .operacion import Operacion


class OperacionCambioLocal(Operacion):
    def __init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion, local_anterior,
                 local_nuevo):
        Operacion.__init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion)
        self.__local_anterior = local_anterior
        self.__local_nuevo = local_nuevo

    @property
    def local_anterior(self):
        return self.__local_anterior

    @local_anterior.setter
    def local_anterior(self, local_anterior):
        self.__local_anterior = local_anterior

    @property
    def local_nuevo(self):
        return self.__local_nuevo

    @local_nuevo.setter
    def local_nuevo(self, local_nuevo):
        self.__local_nuevo = local_nuevo
