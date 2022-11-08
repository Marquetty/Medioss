import pymysql
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QDialog, QTableWidgetItem, QTableWidget, QMessageBox, QAction
from PyQt5 import uic
import sys


class Marca_modelo(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/Marca.ui", self)
        self.cargar_tabla_marca()
        self.cargar_tabla_modelo()
        self.btn_insertar.clicked.connect(self.insertar_marca_modelo)

    def cargar_tabla_marca(self):
        self.vaciar_tabla_marca()
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        conn = con.open
        if conn == False:
            print("no")
        else:
            sql = "SELECT  marca.id_marca,marca.marca_nombre FROM marca ORDER BY marca.marca_nombre ASC"
            cursor.execute(sql)
            row = 0
            datos = cursor.fetchall()
            self.total = datos
            for valores in datos:
                self.table_marca.insertRow(row)
                # id = QTableWidgetItem(str(valores[0]))
                nombre = QTableWidgetItem(str(valores[1]))
                self.table_marca.setItem(row, 0, nombre)

                row = row + 1

        con.commit()
        cursor.close()
        con.close()
        self.table_marca.resizeColumnsToContents()

    def vaciar_tabla_marca(self):
        while self.table_marca.rowCount() > 0:
            self.table_marca.removeRow(0)

    def cargar_tabla_modelo(self):
        self.vaciar_tabla_modelo()
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        conn = con.open
        if conn == False:
            print("no")
        else:
            sql = "SELECT modelo.id_modelo,modelo.modelo_nombre FROM modelo ORDER BY modelo.modelo_nombre ASC"
            cursor.execute(sql)
            row = 0
            datos = cursor.fetchall()
            self.total = datos
            for valores in datos:
                self.table_model.insertRow(row)
                # id = QTableWidgetItem(str(valores[0]))
                nombre = QTableWidgetItem(str(valores[1]))
                self.table_model.setItem(row, 0, nombre)

                row = row + 1

        con.commit()
        cursor.close()
        con.close()
        self.table_model.resizeColumnsToContents()

    def vaciar_tabla_modelo(self):
        while self.table_model.rowCount() > 0:
            self.table_model.removeRow(0)

    def insertar_marca_modelo(self):

        try:
            marca = self.txt_marca.text()
            modelo = self.txt_modelo.text()
            self.validar()
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM marca where marca_nombre='" + marca + "'")
            marca_lista = cursor.fetchone()
            if (marca_lista != None):
                query = ("insert into modelo(modelo_nombre) values (%s)")
                cursor.execute(query, modelo)
                # insertar en la tabla combinada
                marcaC = "SELECT  marca.id_marca,marca.marca_nombre FROM marca WHERE marca.marca_nombre =%s "
                cursor.execute(marcaC, marca)
                datos = cursor.fetchall()
                idmarca = datos[0][0]
                modeloC = "SELECT  modelo.id_modelo,modelo.modelo_nombre FROM modelo WHERE modelo.modelo_nombre =%s "
                cursor.execute(modeloC, modelo)
                datos = cursor.fetchall()
                idmodelo = datos[0][0]
                query2 = ("insert into marca_modelo(id_modelo,id_marca) values (%s,%s)")
                cursor.execute(query2, (str(idmodelo), str(idmarca)))
                con.commit()
                self.cargar_tabla_modelo()
                self.cargar_tabla_marca()
            else:
                sql = "insert into marca(marca_nombre) values (%s) "
                cursor.execute(sql, marca)
                query = ("insert into modelo(modelo_nombre) values (%s)")
                cursor.execute(query, modelo)

                # insertar en la tabla combinada
                marcaC = "SELECT  marca.id_marca,marca.marca_nombre FROM marca WHERE marca.marca_nombre =%s "
                cursor.execute(marcaC, marca)
                datos = cursor.fetchall()
                idmarca = datos[0][0]
                modeloC = "SELECT  modelo.id_modelo,modelo.modelo_nombre FROM modelo WHERE modelo.modelo_nombre =%s "
                cursor.execute(modeloC, modelo)
                datos = cursor.fetchall()
                idmodelo = datos[0][0]
                query2 = ("insert into marca_modelo(id_modelo,id_marca) values (%s,%s)")

                cursor.execute(query2, (str(idmodelo), str(idmarca)))
                con.commit()

                self.cargar_tabla_modelo()
                self.cargar_tabla_marca()
        except Exception as e:
            self.mostrar_error(e.args[0])


    def actulizar(self):
        try:
            marca = self.txt_marca.text()
            modelo = self.txt_modelo.text()
            self.validar()
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM marca where marca_nombre='" + marca + "'")
            marca_lista = cursor.fetchone()
            if (marca_lista != None):
                query = ("insert into modelo(modelo_nombre) values (%s)")
                cursor.execute(query, modelo)
                # insertar en la tabla combinada
                marcaC = "SELECT  marca.id_marca,marca.marca_nombre FROM marca WHERE marca.marca_nombre =%s "
                cursor.execute(marcaC, marca)
                datos = cursor.fetchall()
                idmarca = datos[0][0]
                modeloC = "SELECT  modelo.id_modelo,modelo.modelo_nombre FROM modelo WHERE modelo.modelo_nombre =%s "
                cursor.execute(modeloC, modelo)
                datos = cursor.fetchall()
                idmodelo = datos[0][0]
                query2 = ("insert into marca_modelo(id_modelo,id_marca) values (%s,%s)")
                cursor.execute(query2, (str(idmodelo), str(idmarca)))
                con.commit()
                self.cargar_tabla_modelo()
                self.cargar_tabla_marca()
            else:
                sql = "insert into marca(marca_nombre) values (%s) "
                cursor.execute(sql, marca)
                query = ("insert into modelo(modelo_nombre) values (%s)")
                cursor.execute(query, modelo)

                # insertar en la tabla combinada
                marcaC = "SELECT  marca.id_marca,marca.marca_nombre FROM marca WHERE marca.marca_nombre =%s "
                cursor.execute(marcaC, marca)
                datos = cursor.fetchall()
                idmarca = datos[0][0]
                modeloC = "SELECT  modelo.id_modelo,modelo.modelo_nombre FROM modelo WHERE modelo.modelo_nombre =%s "
                cursor.execute(modeloC, modelo)
                datos = cursor.fetchall()
                idmodelo = datos[0][0]
                query2 = ("insert into marca_modelo(id_modelo,id_marca) values (%s,%s)")

                cursor.execute(query2, (str(idmodelo), str(idmarca)))
                con.commit()

                self.cargar_tabla_modelo()
                self.cargar_tabla_marca()
        except Exception as e:
            self.mostrar_error(e.args[0])




    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def validar(self):
        msg = "El campo {} no puede estar vacío"
        if len(self.txt_marca.text()) == 0:
            raise Exception(msg.format("Marca"))
        if len(self.txt_modelo.text()) == 0:
            raise Exception(msg.format("Modelo"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Marca_modelo()
    GUI.show()
    app.exec()
