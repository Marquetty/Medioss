from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QDialog, QTableWidgetItem, QTableWidget, QMessageBox, QAction
from PyQt5 import uic
import sys
import pymysql

from vistas.lista_equipo_combustion import DialogoEquiposCombustion
from vistas.lista_responsable import DialogoResponsable
from vistas.lista_equipo_electrico import DialogoEquiposElectricos
from vistas.lista_mueble import DialogoMuebles
from vistas.lista_usuario import DialogoUsuario
from vistas.porciento_medios_basicos import porcientoMediosBasicos
from vistas.responsable_equipo_may_consumo import ResponsableMayConsumo
from vistas.responsable_may_edad import ResponsableMayEdad
import matplotlib.pyplot as plt
import pymysql
import numpy as np
import pandas as pd


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
        self.equipos_combustion = DialogoEquiposCombustion()
        self.usuario=DialogoUsuario()
        self.actionresponsable.triggered.connect(self.abrirDialogoResponsable)
        self.action_muebles.triggered.connect(self.abrirDialogoMuebles)
        self.actionEquipos_Electricos.triggered.connect(self.abrirDialogoEquiposElectricos)
        self.actionEquipos_de_Combustion.triggered.connect(self.abrirEquiposCombustion)
        self.actionResonsable_may_consumo.triggered.connect(self.abrirResponsableMayConsumo)
        self.actionLista_de_responsable_de_edad.triggered.connect(self.abrirResponsableMayEdad)
        self.action_local.triggered.connect(self.abrirPorcientoMediosBasicos)
        self.actionGrafico_de_Mueble_por_material.triggered.connect(self.grafico_material)
        self.actionUsuarios.triggered.connect(self.abrirListaUsario)

    #  self.actionCerrar_cesion.triggered.connect(self.abrirLoguin)

    def abrirLoguin(self):
        self.parent.show()

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

    def abrirEquiposCombustion(self):
        self.equipos_combustion.exec_()

    def abrirListaUsario(self):
        self.usuario.exec_()


    def grafico_material(self):
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            print("no")
        else:
            sql = "SELECT mueble.m_id, mueble.m_numero_inventario, mueble.m_fecha,\
                   mueble.m_nombre_objeto, mueble.m_nombre_local, mueble.m_ci_responsable,\
                   mueble.m_descripcion, mueble.m_estado, mueble.m_matrial, responsable.r_nombre FROM mueble INNER JOIN responsable ON mueble.m_ci_responsable = responsable.r_id"
            cursor.execute(sql)
            row = 0
            datos = cursor.fetchall()
            madera = []
            plastico = []
            metal = []
            otros = []

            for valor in datos:
                if valor[8] == "Madera":
                    madera.append(valor[8])
                elif valor[8] == "Plástico":
                    plastico.append(valor[8])
                elif valor[8] == "Metal":
                    metal.append(valor[8])
                else:
                    otros.append(valor[8])

            if len(madera) != 0 or len(plastico) != 0 or len(metal) != 0:
                made = [len(madera), "Madera"]
                plas = [len(plastico), "Plástico"]
                me = [len(metal), "Metal"]

                lista = [made, plas, me]

                df = pd.DataFrame(lista, columns=["Cantidad", "Tipo"])

                plt.pie(df["Cantidad"], labels=df["Tipo"],
                        shadow=True,
                        explode=[0, 0.1, 0.1, ],
                        autopct='%1.1f%%')
                plt.show()
            else:
                print("NO se puede hacer")

    def administrador(self):
        if self.text != "Administrador":
            self.actionResonsable_may_consumo.setEnabled(False)
            self.action_local.setEnabled(False)
            self.actionLista_de_responsable_de_edad.setEnabled(False)
            self.actionGrafico_de_Mueble_por_material.setEnabled(False)
            self.actionUsuarios.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = ventana_principal()
    GUI.show()
    app.exec()
