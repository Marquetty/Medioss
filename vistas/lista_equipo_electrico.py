from datetime import datetime, date

from PyQt5.QtWidgets import QMessageBox, QApplication, QDialog, QTableWidgetItem, QTableWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate
import pymysql
import sys
from PyQt5 import uic
from fpdf import FPDF

from modelo.equipo_electrico import EquipoElectrico


class DialogoEquiposElectricos(QDialog):
    total=[]
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/lista_equipos_electricos.ui", self)
        self.cargar_tabla()
        self.llenar_combo_reposanble()
        self.llenar_combo_marca()
        self.llenar_combo_modelo()
        self.txt_buscar.textChanged.connect(self.buscar)
        self.comboBox_marca.currentTextChanged.connect(self.llenar_combo_modelo)
        self.btn_insertar.clicked.connect(self.insertar_equipos_electricos)
        self.btn_modificar.clicked.connect(self.modificar_equipos_electricos)
        self.btn_eliminar.clicked.connect(self.eliminar_equipos_electricos)
        self.table.itemClicked.connect(self.llenar_formulario)
        self.btn_exportar.clicked.connect(self.exportar_a_pdf)

    def cargar_tabla(self):
        self.vaciar_tabla()
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        voltaje = con.open
        if voltaje == False:
            print("no")
        else:
            sql = "SELECT ee_id, ee_numero_inventario,ee_fecha, \
            ee_nombre_objeto, ee_nombre_local, ee_ci_responsable,\
             ee_consumo,ee_voltaje,ee_marca,ee_modelo, responsable.r_nombre FROM equipos_electricos INNER JOIN responsable ON equipos_electricos.ee_ci_responsable = responsable.r_id"
            cursor.execute(sql)
            row = 0
            datos = cursor.fetchall()
            self.total=datos
            for valores in datos:
                self.table.insertRow(row)
                # id = QTableWidgetItem(str(valores[0]))
                num_inv = QTableWidgetItem(str(valores[1]))
                fecha = QTableWidgetItem(str(valores[2]))
                nombre_objeto = QTableWidgetItem(str(valores[3]))
                nombre_local = QTableWidgetItem(str(valores[4]))
                responsable = QTableWidgetItem(str(valores[10]))
                consumo = QTableWidgetItem(str(valores[6]))
                voltaje = QTableWidgetItem(str(valores[7]))
                marca = QTableWidgetItem(str(valores[8]))
                modelo = QTableWidgetItem(str(valores[9]))

                self.table.setItem(row, 0, num_inv)
                self.table.setItem(row, 1, fecha)
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

    def llenar_combo_reposanble(self):
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            QMessageBox.warning(self, "Error", "No", QMessageBox.OK)
        else:
            row = 0
            cursor.execute("SELECT * FROM responsable")
            tuple = cursor.fetchall()
            self.combo_responsable.addItem("-Seleccione-")
            for valores in tuple:
                self.combo_responsable.addItem(valores[1] + "-" + valores[2])
                row = row + 1
            cursor.close()
            con.close()

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
            self.combo_responsable.addItem("-Seleccione-")
            for valores in tuple:
                self.comboBox_marca.addItem(valores[1])
                row = row + 1
            cursor.close()
            con.close()

    def llenar_combo_modelo(self):
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            QMessageBox.warning(self, "Error", "No", QMessageBox.OK)
        else:
            sql = ("SELECT marca.marca_nombre,\
            marca.id_marca FROM marca WHERE marca.marca_nombre = %s")
            valor = self.comboBox_marca.currentText()
            cursor.execute(sql, valor)
            marca = cursor.fetchall()
            id_marca = marca[0]
            row = 0
            sql2 = ("SELECT modelo.modelo_nombre,\
                marca_modelo.id_marca_modelo,\
                marca_modelo.id_marca,\
                marca_modelo.id_modelo,\
                marca.marca_nombre\
                FROM\
                modelo\
                INNER JOIN marca_modelo ON marca_modelo.id_modelo = modelo.id_modelo\
                INNER JOIN marca ON marca_modelo.id_marca = marca.id_marca\
                WHERE\
                marca_modelo.id_marca = %s")
            cursor.execute(sql2, id_marca[1])
            tuple = cursor.fetchall()
            self.comboBox_modelo.clear()
            self.comboBox_modelo.addItem("-Seleccione-")
            for valores in tuple:
                self.comboBox_modelo.addItem(valores[0])
                row = row + 1
            cursor.close()
            con.close()
            "asd"

    def insertar_equipos_electricos(self):
        try:
            nume_invetario = self.spin_inventario.text()
            nom_objeto = self.txt_nom_objeto.text()
            fecha = self.fecha.text()
            nom_local = self.txt_nom_local.text()
            responsable = self.combo_responsable.currentText()
            consumo = self.spin_consumo.text()
            voltaje = self.combo_voltaje.currentText()
            marca = self.comboBox_marca.currentText()
            modelo = self.comboBox_modelo.currentText()
            variables = responsable.split('-')
            self.validar()
            self.existe_medio_basico(nume_invetario)
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            sql = "SELECT responsable.r_id, responsable.r_nombre FROM responsable WHERE responsable.r_ci =%s"
            cursor.execute(sql, variables[0])
            res = cursor.fetchall()
            respon = res[0][0]
            query = (
                "insert into equipos_electricos(ee_numero_inventario, ee_fecha,ee_nombre_objeto, ee_nombre_local, ee_ci_responsable,\
             ee_consumo,ee_voltaje,ee_marca,ee_modelo) values (%s,%s,%s,%s,%s,%s,%s,%s)")
            cursor.execute(query,
                           (nume_invetario, fecha, nom_objeto, nom_local, respon, consumo, voltaje, marca, modelo))
            con.commit()
            self.cargar_tabla()

        except Exception as e:
            self.mostrar_error(e.args[0])

    def modificar_equipos_electricos(self):
        try:
            ind = self.table.currentRow()
            if ind == -1:
                raise Exception("Debe Seleccionar una Fila")
            id = self.table.item(ind, 0).text()
            nume_invetario = self.spin_inventario.text()
            nom_objeto = self.txt_nom_objeto.text()
            nom_local = self.txt_nom_local.text()
            responsable = self.combo_responsable.currentText()
            consumo = self.spin_consumo.text()
            voltaje = self.combo_voltaje.currentText()
            marca = self.comboBox_marca.text()
            modelo = self.txt_modelo.text()
            variables = responsable.split('-')
            self.validar()
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            sql = "SELECT responsable.r_id, responsable.r_nombre FROM responsable WHERE responsable.r_ci =%s"
            cursor.execute(sql, variables[0])
            res = cursor.fetchall()
            respon = res[0][0]
            query = (
                    "update equipos_electricos set ee_numero_inventario='" + nume_invetario + "',ee_nombre_objeto='" + nom_objeto + "',\
                  ee_nombre_local='" + nom_local + "',ee_ci_responsable='" + str(
                respon) + "',ee_consumo='" + consumo + "',\
                  ee_voltaje='" + voltaje + "',ee_marca='" + marca + "',ee_modelo='" + modelo + "' where ee_id='" + id + "'")

            cursor.execute(query)
            con.commit()
            self.cargar_tabla()
            self.restablecer_controles()
        except Exception as e:
            self.mostrar_error(e.args[0])

    def eliminar_equipos_electricos(self):
        dialogo = QMessageBox.warning(
            self, "Diálogo de aviso", "¿Estás seguro de eliminar el equipo_electrico",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No)
        if dialogo == QMessageBox.Yes:

            try:
                ind = self.table.currentRow()
                if ind == -1:
                    raise Exception("Debe seleccionar fila")
                id = self.table.item(ind, 0).text()
                con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
                cursor = con.cursor()
                query = ("delete from equipos_electricos where ee_id=%s")
                cursor.execute(query, id)
                con.commit()
                cursor.close()
                con.close()
                self.cargar_tabla()
                self.restablecer_controles()
            except Exception as e:
                self.mostrar_error(e.args[0])
        else:
            pass

    def vaciar_tabla(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

    def validar(self):
        msg = "El campo {} no puede estar vacío"
        if len(self.txt_nom_objeto.text()) == 0:
            raise Exception(msg.format("Nombre de Objeto"))
        if len(self.txt_nom_local.text()) == 0:
            raise Exception(msg.format("Nombre local"))
        if self.combo_responsable.currentIndex() == 0:
            raise Exception(msg.format("Responsable"))


    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def existe_medio_basico(self, nume_inventario):
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            print("mom")
        else:
            cursor.execute("SELECT * FROM mueble where m_numero_inventario='" + nume_inventario + "'")
            mueble_tuple = cursor.fetchone()
            cursor.execute("SELECT * FROM equipos_electricos where ee_numero_inventario='" + nume_inventario + "'")
            equipos_electricos_tuple = cursor.fetchone()
            if (mueble_tuple != None or equipos_electricos_tuple != None):
                raise Exception("Ya existe ese Medio Básico")

            cursor.close()
            con.close()

    def restablecer_controles(self):
        self.spin_inventario.setValue(0)
        self.txt_nom_objeto.setText("")
        self.txt_nom_local.setText("")
        self.combo_responsable.setCurrentIndex(0)
        self.spin_consumo.setValue(0)
        self.combo_voltaje.setCurrentIndex(0)
        self.txt_marca.setText("")
        self.txt_modelo.setText("")

    def llenar_formulario(self):
        ind = self.table.currentRow()
        if ind == -1:
            print("no")
        else:
            try:
                numero_inventario = self.table.item(ind, 0).text()
                con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
                cursor = con.cursor()
                query = ("SELECT equipos_electricos.ee_numero_inventario, equipos_electricos.ee_fecha, "
                         "equipos_electricos.ee_nombre_objeto, equipos_electricos.ee_nombre_local, "
                         "equipos_electricos.ee_ci_responsable,equipos_electricos.ee_consumo,"
                         "equipos_electricos.ee_voltaje, equipos_electricos.ee_marca, equipos_electricos.ee_modelo, "
                         "responsable.r_ci, responsable.r_nombre FROM equipos_electricos "
                         "INNER JOIN responsable ON equipos_electricos.ee_ci_responsable = responsable.r_id    WHERE ee_numero_inventario = %s")

                cursor.execute(query, (numero_inventario))
                EquiposElectricos = cursor.fetchone()
                self.spin_inventario.setValue(int(EquiposElectricos[0]))
                fecha = EquiposElectricos[1].isoformat()
                fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
                self.fecha.setDate(fecha_dt)
                self.txt_nom_objeto.setText(EquiposElectricos[2])
                self.txt_nom_local.setText(EquiposElectricos[3])
                self.combo_responsable.setCurrentText(EquiposElectricos[9] + "-" + EquiposElectricos[10])
                self.spin_consumo.setValue(int(EquiposElectricos[5]))
                self.combo_voltaje.setCurrentText(str(EquiposElectricos[6]))
                self.comboBox_marca.setCurrentText(EquiposElectricos[7])
                self.comboBox_modelo.setCurrentText(EquiposElectricos[8])

                con.commit()
                cursor.close()
                con.close()
            except Exception as e:
                self.mostrar_error(e.args[0])

    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def fecha(self, ho):
        una_fecha = '20/04/2019'


    def buscar(self):
        self.vaciar_tabla()
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        voltaje = con.open
        if voltaje == False:
            print("no")
        else:

            nombre = self.txt_buscar.text()
            if len(nombre) == 0:
                self.cargar_tabla()
            sql = "SELECT equipos_electricos.ee_id, \
                        equipos_electricos.ee_numero_inventario, equipos_electricos.ee_fecha,\
                        equipos_electricos.ee_nombre_objeto,\
                        equipos_electricos.ee_nombre_local,\
                        equipos_electricos.ee_ci_responsable,\
                        equipos_electricos.ee_consumo,\
                        equipos_electricos.ee_voltaje,\
                        equipos_electricos.ee_marca,\
                        equipos_electricos.ee_modelo,\
                        responsable.r_id\
                        FROM\
                        equipos_electricos\
                        INNER JOIN responsable ON equipos_electricos.ee_ci_responsable = responsable.r_id\
                        WHERE\
                        equipos_electricos.ee_nombre_objeto =%s"
            cursor.execute(sql, nombre)
            row = 0
            datos = cursor.fetchall()
            self.total=datos
            for valores in datos:
                self.table.insertRow(row)
                # id = QTableWidgetItem(str(valores[0]))
                num_inv = QTableWidgetItem(str(valores[1]))
                fecha = QTableWidgetItem(str(valores[2]))
                nombre_objeto = QTableWidgetItem(str(valores[3]))
                nombre_local = QTableWidgetItem(str(valores[4]))
                responsable = QTableWidgetItem(str(valores[10]))
                consumo = QTableWidgetItem(str(valores[6]))
                voltaje = QTableWidgetItem(str(valores[7]))
                marca = QTableWidgetItem(str(valores[8]))
                modelo = QTableWidgetItem(str(valores[9]))

                self.table.setItem(row, 0, num_inv)
                self.table.setItem(row, 1, fecha)
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

    def exportar_a_pdf(self,):
        self.exportar(self.total)
    def mostrar_mensaje(self, msg):
        QMessageBox.information(self, 'Export', msg)
    def exportar(self,lista_tabla):
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        # Texto
        pdf.set_font('Arial', '', 13)

        # Titulo
        pdf.cell(w=60, h=15, txt='Reporte Equipos Electricos', border=1, ln=1, align='C', fill=0)

        # encabezado
        pdf.cell(w=10, h=15, txt="ID", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="No. Inve", border=1, align='C', fill=0)
        pdf.cell(w=30, h=15, txt="Fecha", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="Nom del Ob", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="Nom del local", border=1, align='C', fill=0)
        pdf.cell(w=25, h=15, txt="Responsable", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="Consumo", border=1, align='C', fill=0)
        pdf.cell(w=30, h=15, txt="Voltaje", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="Marca", border=1, align='C', fill=0)
        pdf.multi_cell(w=20, h=15, txt="Modelos", border=1, align='C', fill=0)
        val = 1
        for valor in lista_tabla:
            pdf.cell(w=10, h=15, txt=str(val), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[1]), border=1, align='C', fill=0)
            pdf.cell(w=30, h=15, txt=str(valor[2]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[3]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[4]), border=1, align='C', fill=0)
            pdf.cell(w=25, h=15, txt=str(valor[10]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[6]), border=1, align='C', fill=0)
            pdf.cell(w=30, h=15, txt=str(valor[7]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[8]), border=1, align='C', fill=0)
            pdf.multi_cell(w=20, h=15, txt=str(valor[9]), border=1, align='C', fill=0)
            val = val + 1
        pdf.output('EquipoElectricos.pdf')
        self.mostrar_mensaje("pdf exportado correctamente")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = DialogoEquiposElectricos()
    GUI.show()
    app.exec()
