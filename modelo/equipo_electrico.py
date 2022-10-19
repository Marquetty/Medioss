from modelo.medio_basico import MedioBasico


class EquipoElectrico(MedioBasico):

    def __init__(self, numero_inventario, fecha,nombre_objeto, nombre_local, responsable, consumo_watts, trabaja110, marca,
                 modelo):
        MedioBasico.__init__(self, numero_inventario,fecha, nombre_objeto, nombre_local, responsable)
        self.__consumo_watts = consumo_watts
        self.__trabaja110 = trabaja110
        self.__marca = marca
        self.__modelo = modelo

    @property
    def consumo_watts(self):
        return self.__consumo_watts

    @consumo_watts.setter
    def consumo_watts(self, consumo_watts):
        self.__consumo_watts = consumo_watts

    @property
    def trabaja110(self):
        return self.__trabaja110

    @trabaja110.setter
    def trabaja110(self, trabaja110):
        self.__trabaja110 = trabaja110

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

    def valor(self):
        res = 100
        if self.trabaja110 == "220":
            res += 25
        return res
