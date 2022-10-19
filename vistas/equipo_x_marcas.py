from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication, QTableWidgetItem
from PyQt5 import uic
import sys
import pymysql


#
class Equipo_x_marcas(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/responsable_may_cosumo.ui", self)
        self.btn_buscar.clicked.connect(self.responsable_equipo_may_consumo)

    def Equipo_x_marcas(self):
        try:
            marca = self.txt_buscar.text()
            if marca == "":
                raise Exception("El campo no puede estar vacio")
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            estado = con.open
            if estado == False:
                print("error de conexion")
            else:
                sql = "select * from equipos_electricos  where ee_marca=%s"
                cursor.execute(sql, marca)
                equipos_electricos = cursor.fetchall()
            lista_equipos_electricos = equipos_electricos
            if len(lista_equipos_electricos)!=0:
                for i in lista_equipos_electricos:
                    self.table.insertRow(row)
                    id = QTableWidgetItem(str(lista_equipos_electricos[0]))
                    num_inv = QTableWidgetItem(str(lista_equipos_electricos[1]))
                    nombre_objeto = QTableWidgetItem(str(lista_equipos_electricos[2]))
                    nombre_local = QTableWidgetItem(str(lista_equipos_electricos[3]))
                    responsable = QTableWidgetItem(str(lista_equipos_electricos[9]))
                    consumo = QTableWidgetItem(str(lista_equipos_electricos[5]))
                    voltaje = QTableWidgetItem(str(lista_equipos_electricos[6]))
                    marca = QTableWidgetItem(str(lista_equipos_electricos[7]))
                    modelo = QTableWidgetItem(str(lista_equipos_electricos[8]))
                    self.table.setItem(row, 0, id)
                    self.table.setItem(row, 1, num_inv)
                    self.table.setItem(row, 2, nombre_objeto)
                    self.table.setItem(row, 3, nombre_local)
                    self.table.setItem(row, 4, responsable)
                    self.table.setItem(row, 5, consumo)
                    self.table.setItem(row, 6, voltaje)
                    self.table.setItem(row, 7, marca)
                    self.table.setItem(row, 8, modelo)
                    row = row + 1

                con.commit()
                cursor.close()
                con.close()
                self.table.resizeColumnsToContents()
            else:
                raise Exception("No existe equipo electrico con esa marca")
        except Exception as e:
            self.mostrar_error(e.args[0])
    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Equipo_x_marcas()
    GUI.show()
    app.exec()
