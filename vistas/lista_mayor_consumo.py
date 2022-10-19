from PyQt5.QtWidgets import QMessageBox, QApplication, QDialog, QTableWidgetItem, QTableWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pymysql
import sys
from PyQt5 import uic

class listaMayorConusmo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/porciento_medios_basicos.ui",self)
        self.btn_calcular.clicked.connect(self.lista_mayor_conusmo)

    def lista_mayor_conusmo(self):

        try:
            consumo = self.txt_buscar.text()
            if consumo == "":
                raise Exception("El campo no puede estar vacio")
            consumo = -1
            responsable = None
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            estado = con.open
            if estado == False:
                print("error de conexion")
            else:
                sql = "select * from equipos_electricos  where ee_marca>%s"
                cursor.execute(sql, consumo)
                equipos_electricos = cursor.fetchall()
                print(equipos_electricos
                 )

        except Exception as e:
            self.mostrar_error(e.args[0])
    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = listaMayorConusmo()
    GUI.show()
    app.exec()