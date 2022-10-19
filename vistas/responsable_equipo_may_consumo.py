from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
from PyQt5 import uic
import sys
import pymysql


#
class ResponsableMayConsumo(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/responsable_may_cosumo.ui", self)
        self.llenar_combo_marca()
        self.btn_buscar.clicked.connect(self.responsable_equipo_may_consumo)

    def responsable_equipo_may_consumo(self):
        try:
            marca = self.comboBox_buscar.currentText()
            if marca == "":
                raise Exception("El campo no puede estar vacio")
            consumo = -1
            responsable = None
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
            if len(lista_equipos_electricos) != 0:
                for i in lista_equipos_electricos:
                    if int(i[5]) > consumo:
                        consumo = int(i[6])
                        responsable = i[5]
                query = "select * from responsable where r_id=%s"
                cursor.execute(query, responsable)
                responsable1 = cursor.fetchone()
                self.txt_ci.setText(responsable1[1])
                self.txt_nombre.setText(responsable1[2])
                self.txt_edad.setText(responsable1[3])
                self.txt_sexo.setText(responsable1[4])
                self.txt_rol.setText(responsable1[5])
                self.txt_ocupacion.setText(responsable1[6])

            else:
                raise Exception("No existe equipo electrico con esa marca")
        except Exception as e:
            self.mostrar_error(e.args[0])

    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def llenar_combo_marca(self):
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            QMessageBox.warning(self, "Error", "No", QMessageBox.OK)
        else:
            row = 0
            cursor.execute("SELECT * FROM marca")
            tuple = cursor.fetchall()
            self.comboBox_buscar.addItem("-Seleccione-")
            for valores in tuple:
                self.comboBox_buscar.addItem(valores[1])
                row = row + 1
            cursor.close()
            con.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = ResponsableMayConsumo()
    GUI.show()
    app.exec()
