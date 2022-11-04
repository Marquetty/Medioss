from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QDialog, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import uic
import sys
import pymysql
from datetime import date
from fpdf import FPDF
from modelo.responsable import Responsable


class DialogoResponsable(QDialog):
    total = []

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/lista_responsable.ui", self)
        self.cargar_tabla()
        self.txt_ci.textChanged.connect(self.Calcular_edad)
        self.txt_buscar.textChanged.connect(self.buscar)
        self.btn_insertar.clicked.connect(self.insertar_responsable)
        self.btn_modificar.clicked.connect(self.modificar_responsable)
        self.btn_eliminar.clicked.connect(self.eliminar_responsable)
        self.table.itemClicked.connect(self.llenar_formulario)
        self.btn_exportar.clicked.connect(self.exportar_a_pdf)

    # carga los datos desde la base de datos
    def cargar_tabla(self):
        self.vaciar_tabla()
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        # verifica que la conexion con la base de datos este correcta
        if estado == False:
            print("error de conexion")
        else:
            row = self.table.rowCount()
            cursor.execute("SELECT * FROM responsable")
            datos = cursor.fetchall()
            self.total = datos
            # recorre los valores y los va insertando en la tabla
            for valores in datos:
                self.table.insertRow(row)
                # id = QTableWidgetItem(str(valores[0]))
                ci = QTableWidgetItem(str(valores[1]))
                nombre = QTableWidgetItem(str(valores[2]))
                edad = QTableWidgetItem(str(valores[3]))
                sexo = QTableWidgetItem(str(valores[4]))
                rol = QTableWidgetItem(str(valores[5]))
                ocupacion = QTableWidgetItem(str(valores[6]))
                self.table.setItem(row, 0, ci)
                self.table.setItem(row, 1, nombre)
                self.table.setItem(row, 2, edad)
                self.table.setItem(row, 3, sexo)
                self.table.setItem(row, 4, rol)
                self.table.setItem(row, 5, ocupacion)
                # self.table.setItem(row, 6, ocupacion)
            # guradar los datos
            con.commit()
            # se cierra el cursor y  la BD
            cursor.close()
            con.close()

    def insertar_responsable(self):
        # tomamos los valores del formulario
        nombre = self.txt_nombre.text()
        ci = self.txt_ci.text()
        edad = self.spin_edad.value()
        sexo = self.combo_sexo.currentText()
        rol = self.combo_rol.currentText()
        ocupacion = self.combo_ocupacion.currentText()
        try:
            # validamos que los datos esten correctamente
            self.validar_controles()
            # verificamos que el responsable no este en la base de dato dado el CI
            self.existe_responsable(ci)
            self.validar_edad()
            print(edad)
            responsable = Responsable(ci, nombre, edad, sexo, rol, ocupacion)
            # conexion con la base de datos
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            query = (
                "insert into responsable(r_ci,r_nombre,r_edad,r_sexo,r_rol,r_ocupacion)  values (%s,%s,%s,%s,%s,%s)")
            cursor.execute(query, (
                responsable.ci, responsable.nombre, responsable.edad, responsable.sexo, responsable.rol_entidad,
                responsable.ocupacion))
            con.commit()
            cursor.close()
            con.close()
            self.cargar_tabla()
            # se restblece el formulario por defecto
            self.restablecer_controles()
        except Exception as e:
            self.mostrar_error(e.args[0])

    def modificar_responsable(self, ):
        # se toman los valores del formulario
        nombre = self.txt_nombre.text()
        ci = self.txt_ci.text()
        edad = self.spin_edad.text()
        sexo = self.combo_sexo.currentText()
        rol = self.combo_rol.currentText()
        ocupacion = self.combo_ocupacion.currentText()
        try:
            ind = self.table.currentRow()
            if ind == -1:
                raise Exception("Debe seleccionar fila")
            id = self.table.item(ind, 0).text()
            # validamos los datos
            self.validar_controles()
            responsable = Responsable(ci, nombre, edad, sexo, rol, ocupacion)
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            query = "update responsable set r_ci='" + responsable.ci + "',r_nombre='" + responsable.nombre + "',r_edad='" + responsable.edad + "',r_sexo='" + responsable.sexo + "',r_rol='" + responsable.rol_entidad + "',r_ocupacion='" + responsable.ocupacion + "' where r_id='" + id + "'"
            cursor.execute(query)
            con.commit()
            cursor.close()
            con.close()
            self.cargar_tabla()
            self.restablecer_controles()
        except Exception as e:
            self.mostrar_error(e.args[0])

    def eliminar_responsable(self):
        dialogo = QMessageBox.warning(
            self, "Diálogo de aviso", "¿Estás seguro de eliminar el responsable",
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
                query = ("delete from responsable where r_ci=%s")
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

    def validar_controles(self):
        msg = "El campo {} no puede estar vacío"
        nombre_responsable = self.txt_nombre.text()
        if not nombre_responsable.isalpha():
            raise Exception("El nombre no puede contener numeros")
        ci = self.txt_ci.text()
        if len(ci) == 0:
            raise Exception(msg.format("CI"))
        if not ci.isnumeric():
            raise Exception("El campo CI solo puede contener números")
        if len(ci) != 11:
            raise Exception("El CI debe tener 11 dígitos")
        mes = int(ci[2:4])
        dia = int(ci[4:6])
        mes_mas_dias = [1, 3, 5, 7, 8, 10, 12]
        mes_menos_dias = [4, 6, 9, 11]

        if mes in mes_mas_dias and (dia < 1 or dia > 31):
            raise Exception("El días en este mes debe estar en el rango de 01 a 31")
        elif mes in mes_menos_dias and (dia < 1 or dia > 30):
            raise Exception("El días en este mes debe estar en el rango de 01 a 30")
        elif mes == 2 and (dia < 1 or dia > 29):
            raise Exception("El días en este mes debe estar en el rango de 01 a 28 (29 en años bisiesto)")
        elif mes not in range(1, 13):
            raise Exception("El mes en el CI debe estar entre 01 y 12")
        if len(self.txt_nombre.text()) == 0:
            raise Exception(msg.format("Nombre Responsable"))
        # if len(self.txt_ocupacion.text()) == 0:
        #   raise Exception(msg.format("Ocupación Responsable"))
        # ocupacion_responsable = self.txt_ocupacion.text()

    #  if not ocupacion_responsable.isalpha():
    #     raise Exception("La ocupacion del responsable no puede contener numeros")

    def vaciar_tabla(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

    def restablecer_controles(self):
        self.txt_ci.setText("")
        self.txt_nombre.setText("")

        self.spin_edad.setValue(18)
        self.combo_rol.setCurrentIndex(0)
        self.combo_sexo.setCurrentIndex(0)

    def llenar_formulario(self):
        ind = self.table.currentRow()
        if ind == -1:
            print("no")
        else:
            ci = self.table.item(ind, 0).text()
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            query = ("SELECT r_ci,r_nombre,r_edad,r_sexo,r_rol,r_ocupacion FROM responsable WHERE r_ci = %s")
            cursor.execute(query, (ci))
            responsable = cursor.fetchone()
            self.txt_ci.setText(responsable[0])
            self.txt_nombre.setText(responsable[1])
            self.spin_edad.setValue(int(responsable[2]))
            self.combo_ocupacion.setCurrentText(responsable[5])
            self.combo_rol.setCurrentText(responsable[4])
            self.combo_sexo.setCurrentText(responsable[3])
            con.commit()
            cursor.close()
            con.close()

    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def existe_responsable(self, ci):
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            print("error de conexion")
        else:
            cursor.execute("SELECT * FROM responsable where r_ci='" + ci + "'")
            tuple = cursor.fetchone()
            if tuple != None:
                raise Exception("Ya existe esa persona")

    def Calcular_edad(self):
        fecha_actual = date.today().year
        texto = self.txt_ci.text()
        if texto.__len__() > 2 and texto.isnumeric():
            anno_ci = int(fecha_actual)
            ci = self.txt_ci.text()
            anno = int(ci[0:2])
            edad2 = (anno_ci - anno)
            edad = edad2.__str__()[2:4]
            self.spin_edad.setValue(int(edad))
        elif texto.__len__() < 2:
            self.spin_edad.setValue(0)

    def validar_edad(self):
        if not self.spin_edad.value() < 18 and self.spin_edad.value() > 65:
            raise Exception("La edad debe estar comprendida entre 18 y 65 años")

    def buscar(self):
        self.vaciar_tabla()
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            QMessageBox.warning(self, "Error", "No", QMessageBox.OK)
        else:
            row = 0
            nombre = self.txt_buscar.text()
            if len(nombre) == 0:
                self.cargar_tabla()
            else:
                sql2 = ("SELECT responsable.r_id,\
                    responsable.r_ci,\
                    responsable.r_nombre,\
                    responsable.r_edad,\
                    responsable.r_sexo,\
                    responsable.r_rol,\
                    responsable.r_ocupacion\
                    FROM\
                    responsable WHERE \
                    responsable.r_nombre = %s")
                cursor.execute(sql2, nombre)
                datos = cursor.fetchall()
                self.total = datos
                for valores in datos:
                    self.table.insertRow(row)
                    # id = QTableWidgetItem(str(valores[0]))
                    ci = QTableWidgetItem(str(valores[1]))
                    nombre = QTableWidgetItem(str(valores[2]))
                    edad = QTableWidgetItem(str(valores[3]))
                    sexo = QTableWidgetItem(str(valores[4]))
                    rol = QTableWidgetItem(str(valores[5]))
                    ocupacion = QTableWidgetItem(str(valores[6]))
                    self.table.setItem(row, 0, ci)
                    self.table.setItem(row, 1, nombre)
                    self.table.setItem(row, 2, edad)
                    self.table.setItem(row, 3, sexo)
                    self.table.setItem(row, 4, rol)
                    self.table.setItem(row, 5, ocupacion)
            cursor.close()
            con.close()

    def mostrar_mensaje(self, msg):
        QMessageBox.information(self, 'Export', msg)

    def exportar_a_pdf(self):
        self.exportar(self.total)

    # Exportr reportes de Responsables

    def exportar(self, lista_tabla):
        try:
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            # Texto
            pdf.set_font('Arial', '', 13)

            # Titulo
            pdf.cell(w=60, h=15, txt='Reporte de Responsables', border=1, ln=1, align='C', fill=0)

            # encabezado
            pdf.cell(w=10, h=15, txt="ID", border=1, align='C', fill=0)
            pdf.cell(w=40, h=15, txt="C. de Identidad", border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt="Nombre", border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt="edad", border=1, align='C', fill=0)
            pdf.cell(w=25, h=15, txt="Sexo", border=1, align='C', fill=0)
            pdf.cell(w=50, h=15, txt="Rol", border=1, align='C', fill=0)
            pdf.multi_cell(w=30, h=15, txt="Ocupacion", border=1, align='C', fill=0)
            val = 1
            for valor in lista_tabla:
                pdf.cell(w=10, h=15, txt=str(val), border=1, align='C', fill=0)
                pdf.cell(w=40, h=15, txt=str(valor[1]), border=1, align='C', fill=0)
                pdf.cell(w=20, h=15, txt=valor[2], border=1, align='C', fill=0)
                pdf.cell(w=20, h=15, txt=str(valor[3]), border=1, align='C', fill=0)
                pdf.cell(w=25, h=15, txt=valor[4], border=1, align='C', fill=0)
                pdf.cell(w=50, h=15, txt=valor[5], border=1, align='C', fill=0)
                pdf.multi_cell(w=30, h=15, txt=valor[6], border=1, align='C', fill=0)
                val = val + 1
            pdf.output('ReportesResponsable.pdf')
            self.mostrar_mensaje("pdf exportado correctamente")
        except Exception as e:
            self.mostrar_error("Por favor cierre el pdf")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = DialogoResponsable()
    GUI.show()
    app.exec()
