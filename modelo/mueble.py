from .medio_basico import MedioBasico
from .estado_mueble import EstadoMueble


class Mueble(MedioBasico):

    def __init__(self, numero_inventario,fecha, nombre_objeto, nombre_local, responsable, descripcion, estado,
                 material_fabricacion):
        MedioBasico.__init__(self, numero_inventario, nombre_objeto, nombre_local, responsable)
        self.__descripcion = descripcion
        self.__estado = estado
        self.__material_fabricacion = material_fabricacion

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, value):
        self.__fecha = value

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado):
        self.__estado = estado

    @property
    def material_fabricacion(self):
        return self.__material_fabricacion

    @material_fabricacion.setter
    def material_fabricacion(self, material_fabricacion):
        self.__material_fabricacion = material_fabricacion

    def valor(self):
        res = 50
        if self.material_fabricacion.lower() == 'madera':
            res += 30
        elif self.material_fabricacion.lower() == 'metal':
            res += 20

        if self.estado == EstadoMueble.REGULAR:
            res = 75 * res / 100
        elif self.estado == EstadoMueble.MALO:
            res = 50 * res / 100

        return res
