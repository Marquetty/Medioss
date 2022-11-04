from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QDialog, QTableWidgetItem, QTableWidget, QMessageBox, QAction
from PyQt5 import uic
import sys
import pymysql
from vistas.ventana import ventana_principal


class Loguin(QDialog):
    rol_usuario = "sdsd"

    def __init__(self, parent=None):
        super(Loguin, self).__init__(parent)
        QDialog.__init__(self)
        uic.loadUi("ui/Loguin.ui", self)
        self.btn_iniciar.clicked.connect(self.abrir_ventana_principal)

    def abrir_ventana_principal(self):
        try:
            usuario=self.le_usuario.text()
            passw=self.le_pass.text()
            self.validar()
            self.buscar_user(usuario,passw)
            self.ventanaPrincipal = ventana_principal(self.rol_usuario)
            self.ventanaPrincipal.show()
            self.close()
        except Exception as e:
            self.mostrar_error(e.args[0])

    def buscar_user(self, usser,passw):
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            estado = con.open
            if estado == False:
                print("error de conexion")
            else:
                sql = "select * from usuario where nombre_usuario=%s"
                cursor.execute(sql, usser)
                user = cursor.fetchall()
                if user.__len__() != 0:
                    rol = user[0][2]
                    self.rol_usuario = rol
                    pas_sql = "select * from usuario where password_usuario=%s"
                    cursor.execute(pas_sql,passw)
                    passs = cursor.fetchall()
                    cursor.close()
                    if passs.__len__() == 0:
                        raise Exception("Contraseña Incorecta")
                    else:
                        print("")

                else:
                    raise Exception("Usuaior no entontrado")


    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def limpiar_campos(self):
        self.le_usuario.setText("")
        self.le_pass.setText("")

    def validar(self):
        msg = "El campo {} no puede estar vacío"
        if len(self.le_usuario.text()) == 0:
            raise Exception(msg.format("Usuario"))
        if len(self.le_pass.text()) == 0:
            raise Exception(msg.format("contraseña"))






if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Loguin()
    GUI.show()
    app.exec()
