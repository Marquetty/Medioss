



from modelo.medio_basico import MedioBasico


class EquipoCombustion(MedioBasico):

    def __init__(self, numero_inventario, fecha, nombre_objeto, nombre_local, responsable, matricula, chofer, marca,
                 modelo,tipo_combustible):
        MedioBasico.__init__(self, numero_inventario,fecha, nombre_objeto, nombre_local, responsable)
        self.__matricula = matricula
        self.__trabaja110 = chofer
        self.__marca = marca
        self.__modelo = modelo
        self.__tipo_combustible=tipo_combustible
    @property
    def matricula(self):
        return self.__matricula

    @matricula.setter
    def consumo_watts(self, matricula):
        self.__matricula = matricula

    @property
    def chofer(self):
        return self.__chofer

    @chofer.setter
    def chofer(self, chofer):
        self.__chofer = chofer

    @property
    def marca(self):
        return self.__marca

    @marca.setter
    def marca(self, marca):
        self.__marca = marca

    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, modelo):
        self.__modelo = modelo

    @property
    def tipo_combustible(self):
        return self.__tipo_combustible

    @modelo.setter
    def tipo_combustible(self, tipo_combustible):
        self.__tipo_combustible = tipo_combustible