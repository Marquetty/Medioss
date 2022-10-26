from datetime import datetime
from weakref import finalize

from PyQt5.QtWidgets import QMessageBox, QApplication, QDialog, QTableWidgetItem, QTableWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pymysql
import sys
from PyQt5 import uic
from fpdf import FPDF

from modelo.mueble import Mueble


class DialogoMuebles(QDialog):
    total=[]
    idMuebleGlobal=0
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/lista_mueble.ui", self)
        self.cargar_tabla()
        self.llenar_combo_reposanble()
        self.txt_buscar.textChanged.connect(self.buscar)
        self.btn_insertar.clicked.connect(self.insertar_mueble)
        self.btn_modificar.clicked.connect(self.modificar_muebles)
        self.btn_eliminar.clicked.connect(self.eliminar_muebles)
        self.table.itemClicked.connect(self.llenar_formulario)
        self.btn_exportar.clicked.connect(self.exportar_a_pdf)

    def cargar_tabla(self):
        self.vaciar_tabla()
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
            self.total=datos
            for valores in datos:
                self.table.insertRow(row)
                num_inv = QTableWidgetItem(str(valores[1]))
                fecha = QTableWidgetItem(str(valores[2]))
                nombre_objeto = QTableWidgetItem(str(valores[3]))
                nombre_local = QTableWidgetItem(str(valores[4]))
                responsable = QTableWidgetItem(str(valores[9]))
                descripcion = QTableWidgetItem(str(valores[6]))
                estado = QTableWidgetItem(str(valores[7]))
                material = QTableWidgetItem(str(valores[8]))
                self.table.setItem(row, 0, num_inv)
                self.table.setItem(row, 1, fecha)
                self.table.setItem(row, 2, nombre_objeto)
                self.table.setItem(row, 3, nombre_local)
                self.table.setItem(row, 4, responsable)
                self.table.setItem(row, 5, descripcion)
                self.table.setItem(row, 6, estado)
                self.table.setItem(row, 7, material)
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

    def insertar_mueble(self):
        try:
            nume_invetario = self.spin_inventario.text()
            nom_objeto = self.txt_nom_objeto.text()
            fecha = self.fecha.text()
            fecha_dt = datetime.strptime(fecha, '%d-%M-%Y')
            nom_local = self.txt_nom_local.text()
            responsable = self.combo_responsable.currentText()
            descripcion = str(self.txt_descripcion.toPlainText())
            estado = self.combo_estado.currentText()
            material = self.txt_material.currentText()
            self.validar_controles()
            self.existe_medio_basico(nume_invetario)
            variables = responsable.split('-')
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            sql = "SELECT responsable.r_id, responsable.r_nombre FROM responsable WHERE responsable.r_ci =%s"
            cursor.execute(sql, variables[0])
            res = cursor.fetchall()
            respon = res[0][0]
            query = (
                "insert into mueble(m_numero_inventario,m_fecha,m_nombre_objeto,m_nombre_local,m_ci_responsable,m_descripcion,m_estado,m_matrial) values (%s,%s,%s,%s,%s,%s,%s,%s)")
            cursor.execute(query, (nume_invetario, fecha_dt,nom_objeto, nom_local, respon, descripcion, estado, material))
            con.commit()
            self.cargar_tabla()
            self.restablecer_controles()
        except Exception as e:
            self.mostrar_error(e.args[0])

    def modificar_muebles(self):
        nume_invetario = self.spin_inventario.text()
        fecha = self.fecha.text()
        fecha_dt = datetime.strptime(fecha, '%d-%M-%Y')
        nom_objeto = self.txt_nom_objeto.text()
        nom_local = self.txt_nom_local.text()
        responsable = self.combo_responsable.currentText()
        descripcion = str(self.txt_descripcion.toPlainText())
        estado = self.combo_estado.currentText()
        material = self.txt_material.currentText()
        variables = responsable.split('-')
        try:
            ind = self.table.currentRow()
            if ind == -1:
                raise Exception("Debe Seleccionar una Fila")
            id = self.idMuebleGlobal
            self.validar_controles()
            #self.existe_medio_basico(nume_invetario)
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            sql = "SELECT responsable.r_id, responsable.r_nombre FROM responsable WHERE responsable.r_ci =%s"
            cursor.execute(sql, variables[0])
            res = cursor.fetchall()
            respon = res[0][0]
            query = ("update mueble set m_numero_inventario='" + nume_invetario + "',m_fecha='" + str(fecha_dt) + "',m_nombre_objeto='" + nom_objeto + "',\
                m_nombre_local='" + nom_local + "',m_ci_responsable='" + str(respon) + "',m_descripcion='" + descripcion + "',\
                m_estado='" + estado + "',m_matrial='" + material + "' where m_id='" + str(id)+ "'")

            cursor.execute(query)
            con.commit()
            self.cargar_tabla()
            self.restablecer_controles()
        except Exception as e:
            self.mostrar_error(e.args[0])

    def eliminar_muebles(self):
        dialogo = QMessageBox.warning(
            self, "Diálogo de aviso", "¿Estás seguro de eliminar el responsable",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No)
        if dialogo == QMessageBox.Yes:
            try:
                ind = self.table.currentRow()
                if ind == -1:
                    raise Exception("Debe seleccionar fila")
                id = self.idMuebleGlobal
                con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
                cursor = con.cursor()
                query = ("delete from mueble where m_id=%s")
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

    def restablecer_controles(self):
        self.spin_inventario.setValue(0)
        self.txt_nom_objeto.setText("")
        self.txt_nom_local.setText("")
        self.combo_responsable.setCurrentIndex(0)
        self.txt_descripcion.setText("")
        self.combo_estado.setCurrentIndex(0)
        self.txt_material.setCurrentIndex(0)

    def llenar_formulario(self):
        ind = self.table.currentRow()
        if ind == -1:
            print("no")
        else:
            try:
                id = self.table.item(ind, 0).text()
                con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
                cursor = con.cursor()
                query = ("SELECT mueble.m_id, mueble.m_numero_inventario,mueble.m_fecha, mueble.m_nombre_objeto,"
                         " mueble.m_nombre_local,mueble.m_ci_responsable,mueble.m_descripcion,"
                         "mueble.m_estado, mueble.m_matrial,responsable.r_nombre,responsable.r_ci "
                         "FROM mueble INNER JOIN responsable ON mueble.m_ci_responsable = responsable.r_id WHERE m_numero_inventario = %s")
                cursor.execute(query, (id))
                mueble = cursor.fetchone()
                self.idMuebleGlobal=mueble[0]
                self.spin_inventario.setValue(int(mueble[1]))
                fecha = mueble[2].isoformat()
                fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
                self.fecha.setDate(fecha_dt)
                self.txt_nom_objeto.setText(mueble[3])
                self.txt_nom_local.setText(mueble[4])
                self.combo_responsable.setCurrentText(mueble[10] + "-" + mueble[9])
                self.txt_descripcion.setText(mueble[6])
                self.combo_estado.setCurrentText(mueble[7])
                self.txt_material.setCurrentText(mueble[8])
                con.commit()
                cursor.close()
                con.close()
            except Exception as e:
                print(e)

    def vaciar_tabla(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

    def validar_controles(self):
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
            print("error de conexion")
        else:
            cursor.execute("SELECT * FROM mueble where m_numero_inventario='" + nume_inventario + "'")
            mueble_tuple = cursor.fetchone()
            cursor.execute("SELECT * FROM equipos_electricos where ee_numero_inventario='" + nume_inventario + "'")
            equipos_electricos_tuple = cursor.fetchone()
            if (mueble_tuple != None or equipos_electricos_tuple != None):
                raise Exception("Ya existe ese Medio Básico")
            print(equipos_electricos_tuple)
            cursor.close()
            con.close()

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
            sql = "SELECT responsable.r_id,\
                        mueble.m_id,\
                        mueble.m_numero_inventario,\
                        mueble.m_fecha,\
                        mueble.m_nombre_objeto,\
                        mueble.m_nombre_local,\
                        mueble.m_ci_responsable,\
                        mueble.m_descripcion,\
                        mueble.m_estado,\
                        mueble.m_matrial\
                        FROM\
                        responsable\
                        INNER JOIN mueble ON mueble.m_ci_responsable = responsable.r_id\
                        WHERE\
                        mueble.m_nombre_local  =%s"
            cursor.execute(sql, nombre)
            row = 0
            datos = cursor.fetchall()
            self.total=datos
            for valores in datos:
                self.table.insertRow(row)
                id = QTableWidgetItem(str(valores[0]))
                num_inv = QTableWidgetItem(str(valores[1]))
                nombre_objeto = QTableWidgetItem(str(valores[2]))
                nombre_local = QTableWidgetItem(str(valores[3]))
                responsable = QTableWidgetItem(str(valores[8]))
                descripcion = QTableWidgetItem(str(valores[5]))
                estado = QTableWidgetItem(str(valores[6]))
                material = QTableWidgetItem(str(valores[7]))
                self.table.setItem(row, 0, id)
                self.table.setItem(row, 1, num_inv)
                self.table.setItem(row, 2, nombre_objeto)
                self.table.setItem(row, 3, nombre_local)
                self.table.setItem(row, 4, responsable)
                self.table.setItem(row, 5, descripcion)
                self.table.setItem(row, 6, estado)
                self.table.setItem(row, 7, material)
                row = row + 1

        con.commit()
        cursor.close()
        con.close()
        self.table.resizeColumnsToContents()

    def exportar_a_pdf(self, ):
        self.exportar(self.total)

    def mostrar_mensaje(self, msg):
        QMessageBox.information(self, 'Export', msg)

    def exportar(self, lista_tabla):
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        # Texto
        pdf.set_font('Arial', '', 13)
        # Titulo
        pdf.cell(w=60, h=15, txt='Reporte de Muebles', border=1, ln=1, align='C', fill=0)
        # encabezado
        pdf.cell(w=10, h=15, txt="ID", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="No. Inve", border=1, align='C', fill=0)
        pdf.cell(w=30, h=15, txt="Fecha", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="Nom del Ob", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="Nom del local", border=1, align='C', fill=0)
        pdf.cell(w=25, h=15, txt="Responsable", border=1, align='C', fill=0)
        pdf.cell(w=20, h=15, txt="Descripcion", border=1, align='C', fill=0)
        pdf.cell(w=30, h=15, txt="Estado", border=1, align='C', fill=0)
        pdf.multi_cell(w=20, h=15, txt="Material", border=1, align='C', fill=0)
        val = 1
        for valor in lista_tabla:

            pdf.cell(w=10, h=15, txt=str(val), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[1]), border=1, align='C', fill=0)
            pdf.cell(w=30, h=15, txt=str(valor[2]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[3]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[4]), border=1, align='C', fill=0)
            pdf.cell(w=25, h=15, txt=str(valor[9]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt=str(valor[6]), border=1, align='C', fill=0)
            pdf.cell(w=30, h=15, txt=str(valor[7]), border=1, align='C', fill=0)
            pdf.multi_cell(w=20, h=15, txt=str(valor[8]), border=1, align='C', fill=0)
            val = val + 1
        pdf.output('Muebles.pdf')
        self.mostrar_mensaje("pdf exportado correctamente")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = DialogoMuebles()
    GUI.show()
    app.exec()
