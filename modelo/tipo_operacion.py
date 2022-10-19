from enum import Enum


class TipoOperacion(Enum):
    ALTA = "Alta"
    BAJA = "Baja"
    CAMBIO_LOCAL = "Cambio de local"
    CAMBIO_RESPONSABLE = "Cambio de responsable"
    ACTUALIZACION = "Actualización"
