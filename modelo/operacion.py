class Operacion:
    def __init__(self, fecha_realizacion, numero_inventario, tipo_medio_basico, tipo_operacion):
        self.__fecha_realizacion = fecha_realizacion
        self.__numero_inventario = numero_inventario
        self.__tipo_medio_basico = tipo_medio_basico
        self.__tipo_operacion = tipo_operacion

    @property
    def fecha_realizacion(self):
        return self.__fecha_realizacion

    @fecha_realizacion.setter
    def fecha_realizacion(self, fecha_realizacion):
        self.__fecha_realizacion = fecha_realizacion

    @property
    def numero_inventario(self):
        return self.__numero_inventario

    @numero_inventario.setter
    def numero_inventario(self, numero_inventario):
        self.__numero_inventario = numero_inventario

    @property
    def tipo_medio_basico(self):
        return self.__tipo_medio_basico

    @tipo_medio_basico.setter
    def tipo_medio_basico(self, tipo_medio_basico):
        self.__tipo_medio_basico = tipo_medio_basico

    @property
    def tipo_operacion(self):
        return self.__tipo_operacion

    @tipo_operacion.setter
    def tipo_operacion(self, tipo_operacion):
        self.__tipo_operacion = tipo_operacion
