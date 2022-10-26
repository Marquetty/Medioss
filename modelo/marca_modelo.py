class MarcaModelo:

    def __init__(self, Nombre,):
        self.__Nombre = Nombre

    @property
    def Nombre(self):
        return self.__Nombre

    @Nombre.setter
    def numero_inventario(self, Nombre):
        self.__Nombre = Nombre
