from .operacion import Operacion


class OperacionCambioResponsable(Operacion):
    def __init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion, responsable_anterior,
                 responsable_nuevo):
        Operacion.__init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion)
        self.__responsable_anterior = responsable_anterior
        self.__responsable_nuevo = responsable_nuevo

    @property
    def responsable_anterior(self):
        return self.__responsable_anterior

    @responsable_anterior.setter
    def responsable_anterior(self, responsable_anterior):
        self.__responsable_anterior = responsable_anterior

    @property
    def responsable_nuevo(self):
        return self.__responsable_nuevo

    @responsable_nuevo.setter
    def responsable_nuevo(self, responsable_nuevo):
        self.__responsable_nuevo = responsable_nuevo
