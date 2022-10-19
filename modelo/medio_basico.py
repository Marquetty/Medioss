class MedioBasico:

    def __init__(self, numero_inventario, fecha, nombre_objeto, nombre_local, responsable):
        self.__numero_inventario = numero_inventario
        self.__fecha = fecha
        self.__nombre_objeto = nombre_objeto
        self.__nombre_local = nombre_local
        self.__responsable = responsable

    @property
    def numero_inventario(self):
        return self.__numero_inventario

    @numero_inventario.setter
    def numero_inventario(self, numero_inventario):
        self.__numero_inventario = numero_inventario

    @property
    def fecha(self):
        return self.__fecha

    def fecha(self, fecha):
        self.__fecha = fecha

    @property
    def nombre_objeto(self):
        return self.__nombre_objeto

    @nombre_objeto.setter
    def nombre_objeto(self, nombre_objeto):
        self.__nombre_objeto = nombre_objeto

    @property
    def nombre_local(self):
        return self.__nombre_local

    @nombre_local.setter
    def nombre_local(self, nombre_local):
        self.__nombre_local = nombre_local

    @property
    def responsable(self):
        return self.__responsable

    @responsable.setter
    def responsable(self, responsable):
        self.__responsable = responsable

    def __lt__(self, other):
        return self.numero_inventario < other.numero_inventario

    def valor(self):
        pass
