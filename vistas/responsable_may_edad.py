from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QDialog, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import uic
import sys
from fpdf import FPDF
import pymysql





class ResponsableMayEdad(QDialog):
    total = []
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/responsable_may_edad.ui", self)
        self.btn_buscar.clicked.connect(self.responsable_may_edad)
        self.btn_exportar.clicked.connect(self.exportar_a_pdf)


    def vaciar_tabla(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)



    def responsable_may_edad(self):

        self.vaciar_tabla()
        try:
            edad = int(self.txt_buscar.text())
            if edad<0:
                raise Exception("El campo no puede estar vacio")
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            estado = con.open
            if estado == False:
                print("error de conexion")
            else:

                sql = "select * from responsable  where r_edad > %s"
                cursor.execute(sql, edad)
                responsable = cursor.fetchall()
                self.total=responsable
                row = 0
                for valores in responsable:
                    self.table.insertRow(row)
                    id = QTableWidgetItem(str(valores[0]))
                    ci = QTableWidgetItem(str(valores[1]))
                    nombre = QTableWidgetItem(str(valores[2]))
                    edad = QTableWidgetItem(str(valores[3]))
                    sexo = QTableWidgetItem(str(valores[4]))
                    rol = QTableWidgetItem(str(valores[5]))
                    ocupacion = QTableWidgetItem(str(valores[6]))
                    self.table.setItem(row, 0, id)
                    self.table.setItem(row, 1, ci)
                    self.table.setItem(row, 2, nombre)
                    self.table.setItem(row, 3, edad)
                    self.table.setItem(row, 4, sexo)
                    self.table.setItem(row, 5, rol)
                    self.table.setItem(row, 6, ocupacion)
                con.commit()
                cursor.close()
                con.close()

        except Exception as e:
            self.mostrar_error(e.args[0])

    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def mostrar_mensaje(self, msg):
        QMessageBox.information(self, 'Export', msg)

    def exportar_a_pdf(self,):
        self.exportar(self.total)

    def exportar(self,lista_tabla):
        try:
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            # Texto
            pdf.set_font('Arial', '', 13)

            # Titulo
            pdf.cell(w=30, h=15, txt='Reporte', border=1, ln=1, align='C', fill=0)

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
            pdf.output('ResponsableDeMayorEdad.pdf')
            self.mostrar_mensaje("pdf exportado correctamente")
        except Exception as e:
            self.mostrar_error("Por favor cierre el pdf")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = ResponsableMayEdad()
    GUI.show()
    app.exec()
