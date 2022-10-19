class Responsable:

    def __init__(self, ci, nombre, edad, sexo, Departamento, ocupacion):
        self.__ci = ci
        self.__nombre = nombre
        self.__edad = edad
        self.__sexo = sexo
        self.__rol_entidad = Departamento
        self.__ocupacion = ocupacion

    @property
    def ci(self):
        return self.__ci

    @ci.setter
    def ci(self, ci):
        self.__ci = ci

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, edad):
        self.__edad = edad

    @property
    def sexo(self):
        return self.__sexo

    @sexo.setter
    def sexo(self, sexo):
        self.__sexo = sexo

    @property
    def rol_entidad(self):
        return self.__rol_entidad

    @rol_entidad.setter
    def rol_entidad(self, rol_entidad):
        self.__rol_entidad = rol_entidad

    @property
    def ocupacion(self):
        return self.__ocupacion

    @ocupacion.setter
    def ocupacion(self, ocupacion):
        self.__ocupacion = ocupacion
