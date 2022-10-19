from modelo.mueble import Mueble


class ServiciosEntidad:
    def __init__(self, entidad):
        self.__entidad = entidad

    # b
    def valor_medio_basico(self, numero_inventario):
        for i in self.__entidad.get_lista_medios_basicos():
            if i.numero_inventario == numero_inventario:
                return i.valor()
        raise Exception("No hay ningún medio con ese número de inventario")

    # c
    def responsable_equipo_may_consumo(self, marca):
        consumo = -1
        responsable = None
        lista_equipos_electricos = self.__entidad.get_lista_equipos_electricos()
        for i in lista_equipos_electricos:
            if i.marca == marca and i.consumo_watts > consumo:
                consumo = i.consumo_watts
                responsable = i.responsable
        if responsable is None:
            raise Exception("No hay ningún equipo con esa marca")
        return responsable

    # d
    def porciento_medios_basicos(self, nombre_local, material_fabricacion):
        total, parte = 0, 0
        for i in self.__entidad.get_lista_muebles():
            if i.nombre_local == nombre_local:
                total += 1
                if isinstance(i, Mueble):
                    if i.material_fabricacion.lower() == material_fabricacion.lower():
                        parte += 1
        if total == 0:
            raise Exception("No existe ese local")
        if parte == 0:
            raise Exception("No hay medios básicos de ese local fabricados con ese material")
        return parte * 100.0 / total

    # e
    def promedio_consumo_equipos(self, nombre_local):
        suma, parte = 0, 0
        for i in self.__entidad.get_lista_equipos_electricos():
            if i.nombre_local == nombre_local:
                parte += 1
                suma += i.consumo_watts
        if parte == 0:
            raise Exception("No existen equipos eléctricos en ese local")
        return suma / parte

    # f
    def medios_basicos_x_local_ord(self, nombre_local):
        medios = []
        for medio in self.__entidad.get_lista_medios_basicos():
            if medio.nombre_local == nombre_local:
                medios.append(medio)
        if len(medios) == 0:
            raise Exception("No existen medios en ese local")
        medios.sort()
        return medios
