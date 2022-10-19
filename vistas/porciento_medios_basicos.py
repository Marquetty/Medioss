from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
import pymysql
from PyQt5 import uic
import sys


class porcientoMediosBasicos(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/porciento_medios_basicos.ui",self)
        self.llenarcombonombre()
        self.btn_calcular.clicked.connect(self.porciento_medios_basicos)

    def porciento_medios_basicos(self):
        material_fabricacion = self.comboBox_material.currentText()
        nombre_local = self.comboBox_nombre_local.currentText()
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            print("error de conexion")
        else:
           try:
               total, parte = 0, 0
               sql = "SELECT Count(mueble.m_id) FROM mueble where m_nombre_local=%s"
               cursor.execute(sql, nombre_local)
               total1 = cursor.fetchall()
               total = int(total1[0][0])
               query = "SELECT Count(mueble.m_matrial) FROM mueble WHERE mueble.m_matrial = %s"
               cursor.execute(query, material_fabricacion)
               parte1 = cursor.fetchall()
               parte = int(parte1[0][0])
               if total == 0:
                   raise Exception("No existe ese local")
               if parte == 0:
                   raise Exception("No hay medios básicos de ese local fabricados con ese material")
               porciento = parte * 100.0 / total
               QMessageBox.information(self,"Información",str(porciento),QMessageBox.Ok)

           except Exception as e:
               self.mostrar_error(e.args[0])
    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def llenarcombonombre(self):
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            QMessageBox.warning(self, "Error", "No", QMessageBox.OK)
        else:
            sql = ("SELECT mueble.m_matrial, mueble.m_nombre_local FROM mueble")
            cursor.execute(sql)
            tuple = cursor.fetchall()

            self.comboBox_material.addItem("-Seleccione-")
            self.comboBox_nombre_local.addItem("-Seleccione-")
            for valores in tuple:
                self.comboBox_material.addItem(valores[0])
                self.comboBox_nombre_local.addItem(valores[1])

            cursor.close()
            con.close()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = porcientoMediosBasicos()
    GUI.show()
    app.exec()
