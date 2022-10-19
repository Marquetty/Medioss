from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QDialog, QTableWidgetItem, QTableWidget, QMessageBox, QAction
from PyQt5 import uic
import sys
import pymysql
from vistas.ventana import ventana_principal

class Loguin(QDialog):

    def __init__(self):

        QDialog.__init__(self)
        uic.loadUi("ui/Loguin.ui", self)
        self.ventanaPrincipal=ventana_principal()
        self.btn_iniciar.clicked.connect(self.abrirQmainwindowventana)

    def abrirQmainwindowventana(self):
        self.ventanaPrincipal.show()


    def buscar_user(self, usser):
        try:
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            estado = con.open
            if estado == False:
                print("error de conexion")
            else:
                sql = "select * from usuario where nombre_usuario=%s"
                cursor.execute(sql, usser)
                user = cursor.fetchall()

                cursor.close()

                return user
        except:
            print("mal")

    def Rol(self):
        usuario = self.le_usuario.text()
        valor = Loguin.buscar_user(self, usuario)
        rol=valor[0][2]
        return rol

    def roll(self):
        rolll=Loguin.Rol
        return rolll


    def buscar_password(self, passw):
        try:
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            estado = con.open
            if estado == False:
                print("error de conexion")
            else:
                sql = "select * from usuario where nombre_usuario={}".format(passw)
                cursor.execute(sql)
                passs = cursor.fetchall()
                cursor.close()
                return passs
        except:
            print("mal")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Loguin()
    GUI.show()
    app.exec()
