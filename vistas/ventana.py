from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QDialog, QTableWidgetItem, QTableWidget, QMessageBox, QAction
from PyQt5 import uic
import sys
import pymysql

from vistas.lista_responsable import DialogoResponsable
from vistas.lista_equipo_electrico import DialogoEquiposElectricos
from vistas.lista_mueble import DialogoMuebles
from vistas.porciento_medios_basicos import porcientoMediosBasicos
from vistas.responsable_equipo_may_consumo import ResponsableMayConsumo
from vistas.responsable_may_edad import ResponsableMayEdad


class ventana_principal(QMainWindow):

    def __init__(self, text, parent=None):
        QMainWindow.__init__(self)
        super(ventana_principal, self).__init__()
        uic.loadUi("ui/ventana_principal.ui", self)
        self.parent = parent
        self.text = text
        self.administrador()
        self.dialogo_resposanble = DialogoResponsable()
        self.resposanble_may_consumo = ResponsableMayConsumo()
        self.dialogo_equipos_electricos = DialogoEquiposElectricos()
        self.dialogo_muebles = DialogoMuebles()
        self.porciento = porcientoMediosBasicos()
        self.mayoredad = ResponsableMayEdad()
        self.actionresponsable.triggered.connect(self.abrirDialogoResponsable)
        self.action_muebles.triggered.connect(self.abrirDialogoMuebles)
        self.actionEquipos_Electricos.triggered.connect(self.abrirDialogoEquiposElectricos)
        self.actionResonsable_may_consumo.triggered.connect(self.abrirResponsableMayConsumo)
        self.actionLista_de_responsable_de_edad.triggered.connect(self.abrirResponsableMayEdad)
        self.action_local.triggered.connect(self.abrirPorcientoMediosBasicos)

    def abrirDialogoMuebles(self):
        self.dialogo_muebles.exec_()

    def abrirDialogoEquiposElectricos(self):
        self.dialogo_equipos_electricos.exec_()

    def abrirDialogoResponsable(self):
        self.dialogo_resposanble.exec()

    def abrirResponsableMayConsumo(self):
        self.resposanble_may_consumo.exec()

    def abrirPorcientoMediosBasicos(self):
        self.porciento.exec_()

    def abrirResponsableMayEdad(self):
        self.mayoredad.exec()

    def administrador(self):
        if self.text != "Administrador":
            self.actionResonsable_may_consumo.setEnabled(False)
            self.action_local.setEnabled(False)
            self.actionLista_de_responsable_de_edad.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = ventana_principal()
    GUI.show()
    app.exec()
