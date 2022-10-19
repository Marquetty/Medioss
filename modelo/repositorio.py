from modelo.mueble import Mueble
from modelo.equipo_electrico import EquipoElectrico
from modelo.operacion import Operacion
from modelo.operacion_alta import OperacionAlta
from modelo.operacion_cambio_local import OperacionCambioLocal
from modelo.operacion_cambio_responsble import  OperacionCambioResponsable
from modelo.operacion_actualizacion import OperacionActualizacion


class Entidad:

    def __init__(self):
        self.__lista_medios_basicos = []
        self.__lista_operaciones = []
        self.__lista_responsables = []


    # Medios basicos
    # Devuelve el indice de un medio basico por su numero de inventario
    def ind_medio_basico_x_numero_inventario(self, numero_inventario):
        for i in range(len(self.__lista_medios_basicos)):
            if self.__lista_medios_basicos[i].numero_inventario == numero_inventario:
                return i

    # Devuelve el medio basico por su numero de inventario
    def medio_basico_x_numero_inventario(self, numero_inventario):
        for medio_basico in self.__lista_medios_basicos:
            if medio_basico.numero_inventario == numero_inventario:
                return medio_basico

    # Devuelve el indice de un medio basico dado el medio
    def ind_medio_basico(self, medio_basico):
        for i in range(len(self.__lista_medios_basicos)):
            if self.__lista_medios_basicos[i] == medio_basico:
                return i

    # Insertar medios basicos en la lista de la entidad
    def insertar_medio_basico(self, medio_basico):
        if self.ind_medio_basico_x_numero_inventario(medio_basico.numero_inventario) is not None:
            raise Exception('El medio básico existe en la entidad')
        self.__lista_medios_basicos.append(medio_basico)

    # Actualizar medios basicos dado el numero de inventario y medio basico
    def actualizar_medio_basico(self, numero_inventario, medio_basico):
        ind_ant = self.ind_medio_basico_x_numero_inventario(numero_inventario)
        if ind_ant is None:
            raise Exception('El medio básico no existe')
        ind_nue = self.ind_medio_basico(medio_basico)
        if ind_nue is not None and ind_nue != ind_ant:
            raise Exception('El medio básico existe en la entidad')
        self.__lista_medios_basicos[ind_ant] = medio_basico

    # Eliminar medio basico por numero de inventario
    def eliminar_medio_basico(self, numero_inventario):
        ind = self.ind_medio_basico_x_numero_inventario(numero_inventario)
        if ind is None:
            raise Exception('El medio básico no existe')
        self.__lista_medios_basicos.remove(self.__lista_medios_basicos[ind])

    # Devuelve la lista de medios basicos
    def get_lista_medios_basicos(self):
        return self.__lista_medios_basicos

    # Devuelve la lista de mueble
    def get_lista_muebles(self):
        lista_muebles = []
        for i in self.__lista_medios_basicos:
            if isinstance(i, Mueble):
                lista_muebles.append(i)
        return lista_muebles

    # Devuelve la lista de equipos electricos
    def get_lista_equipos_electricos(self):
        lista_equipos_electricos = []
        for i in self.__lista_medios_basicos:
            if isinstance(i, EquipoElectrico):
                lista_equipos_electricos.append(i)
        return lista_equipos_electricos

    # Responsables
    # Devuelve el indice de un responsable por su carnet de identidad
    def ind_responsable_x_ci(self, ci):
        for i in range(len(self.__lista_responsables)):
            if self.__lista_responsables[i].ci == ci:
                return i

    # Devuelve el responsable por su carnet de identidad
    def responsable_x_ci(self, ci):
        for responsable in self.__lista_responsables:
            if responsable.ci == ci:
                return responsable

    # Devuelve el indice de un responsable dado el responsable
    def ind_responsable(self, responsable):
        for i in range(len(self.__lista_responsables)):
            if self.__lista_responsables[i] == responsable:
                return i

    # Insertar responsable en la lista de la entidad
    def insertar_responsable(self, responsable):
        if self.ind_responsable_x_ci(responsable.ci) is not None:
            raise Exception('El responsable existe en la entidad')
        self.__lista_responsables.append(responsable)

    # Actualizar responsable dado el carnet de identidad y responsable
    def actualizar_responsable(self, ci, responsable):
        ind_ant = self.ind_responsable_x_ci(ci)
        if ind_ant is None:
            raise Exception('El responsable no existe')
        ind_nue = self.ind_responsable(responsable)
        if ind_nue is not None and ind_nue != ind_ant:
            raise Exception('El responsable existe en la entidad')
        self.__lista_responsables[ind_ant] = responsable

    # Eliminar responsable dado el carnet de identidad
    def eliminar_responsable(self, ci):
        ind = self.ind_responsable_x_ci(ci)
        if ind is None:
            raise Exception('El responsable no existe')
        self.__lista_responsables.remove(self.__lista_responsables[ind])

    # Devuelve la lista de responsables
    def get_lista_responsables(self):
        return self.__lista_responsables

    # Operacion
    # Insertar operacion en la lista de la entidad
    def insertar_operacion(self, operacion):
        self.__lista_operaciones.append(operacion)

    # Devuelve la lista de operaciones de baja
    def get_lista_operaciones_baja(self):
        lista_oper = []
        for i in self.__lista_operaciones:
            if isinstance(i, Operacion):
                lista_oper.append(i)
        return lista_oper

    # Devuelve la lista de operaciones de alta
    def get_lista_operaciones_alta(self):
        lista_oper = []
        for i in self.__lista_operaciones:
            if isinstance(i, OperacionAlta):
                lista_oper.append(i)
        return lista_oper

    # Devuelve la lista de operaciones de cambio de local
    def get_lista_operaciones_cambio_local(self):
        lista_oper = []
        for i in self.__lista_operaciones:
            if isinstance(i, OperacionCambioLocal):
                lista_oper.append(i)
        return lista_oper

    # Devuelve la lista de operaciones de cambio de responsable
    def get_lista_operaciones_cambio_responsable(self):
        lista_oper = []
        for i in self.__lista_operaciones:
            if isinstance(i, OperacionCambioResponsable):
                lista_oper.append(i)
        return lista_oper

    # Devuelve la lista de operaciones de actualizacion
    def get_lista_operaciones_actualizacion(self):
        lista_oper = []
        for i in self.__lista_operaciones:
            if isinstance(i, OperacionActualizacion):
                lista_oper.append(i)
        return lista_oper
