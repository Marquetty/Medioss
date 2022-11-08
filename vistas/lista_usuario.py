import hashlib

from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QDialog, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import uic
import sys
import pymysql
from datetime import date
from fpdf import FPDF


class DialogoUsuario(QDialog):
    total = []
    idGlobal = None

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("ui/lista_usuario.ui", self)
        self.cargar_tabla()

        self.btn_insertar.clicked.connect(self.insertar_usuario)
       # self.btn_actualizar.clicked.connect(self.modificar_usuario)
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
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
            cursor.execute("SELECT * FROM usuario")
            datos = cursor.fetchall()
            self.total = datos
            # recorre los valores y los va insertando en la tabla
            for valores in datos:
                self.table.insertRow(row)
                # id = QTableWidgetItem(str(valores[0]))
                nombre = QTableWidgetItem(str(valores[1]))
                rol_usuario = QTableWidgetItem(str(valores[2]))
                contrasenna = QTableWidgetItem(str(valores[3]))

                self.table.setItem(row, 0, nombre)
                self.table.setItem(row, 1, rol_usuario)
                self.table.setItem(row, 2, contrasenna)
            # guradar los datos
            con.commit()
            # se cierra el cursor y  la BD
            cursor.close()
            con.close()

    def insertar_usuario(self):
        # tomamos los valores del formulario
        nombre = self.txt_nombre.text()
        rol_usuario = self.combo_rol.currentText()
        pas=self.txt_pwd.text()
        print(pas)
        contrasenna = self.cifrarConstranna(pas)
        try:
            # validamos que los datos esten correctamente
            self.validar_controles()
            self.existe_usuario(nombre)
            # conexion con la base de datos
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            query = (
                "insert into usuario(nombre_usuario,rol_usuario,password_usuario)  values (%s,%s,%s)")
            cursor.execute(query, (nombre, rol_usuario, contrasenna))
            con.commit()
            cursor.close()
            con.close()
            self.cargar_tabla()
            # se restblece el formulario por defecto
            self.restablecer_controles()
        except Exception as e:
            self.mostrar_error(e.args[0])

    def modificar_usuario(self, ):
        # se toman los valores del formulario
        nombre = self.txt_nombre.text()
        rol_usuario = self.combo_rol.currentText()
        contrasenna = self.txt_pwd.text()
        try:
            ind = self.table.currentRow()
            if ind == -1:
                raise Exception("Debe seleccionar fila")
            id = self.idGlobal
            # validamos los datos
            self.validar_controles()
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            query = "update usuario set nombre_usuario='" + nombre + "',rol_usuario='" + rol_usuario + \
                    "',password_usuario='" + contrasenna + "' where id_usuario='" + id + "'"
            cursor.execute(query)
            con.commit()
            cursor.close()
            con.close()
            self.cargar_tabla()
            self.restablecer_controles()
        except Exception as e:
            self.mostrar_error(e.args[0])

    def eliminar_usuario(self):
        dialogo = QMessageBox.warning(
            self, "Diálogo de aviso", "¿Estás seguro de eliminar el responsable",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No)
        if dialogo == QMessageBox.Yes:
            try:
                ind = self.table.currentRow()
                if ind == -1:
                    raise Exception("Debe seleccionar fila")
                id = self.idGlobal
                con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
                cursor = con.cursor()
                query = ("delete from usuario where id_usuario =%s")
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
        if len(self.txt_nombre.text()) == 0:
            raise Exception(msg.format("nombre"))
        if len(self.txt_pwd.text()) == 0:
            raise Exception(msg.format("contraseña"))
        if self.combo_rol.currentIndex() == 0:
            raise Exception(msg.format("Rol"))

    def vaciar_tabla(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)

    def restablecer_controles(self):
        self.txt_pwd.setText("")
        self.txt_nombre.setText("")
        self.combo_rol.setCurrentIndex(0)

    def llenar_formulario(self):
        ind = self.table.currentRow()
        if ind == -1:
            print("no")
        else:
            id = self.table.item(ind, 0).text()
            con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
            cursor = con.cursor()
            query = ("SELECT id_usuario,nombre_usuario,rol_usuario,password_usuario"
                     " FROM usuario WHERE nombre_usuario = %s")
            cursor.execute(query, (id))
            responsable = cursor.fetchone()
            self.idGlobal= responsable[0]
            self.txt_nombre.setText(responsable[1])
            self.combo_rol.setCurrentText(responsable[2])
            self.txt_pwd.setText("")

            con.commit()
            cursor.close()
            con.close()

    def mostrar_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)

    def existe_usuario(self, nombre):
        con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
        cursor = con.cursor()
        estado = con.open
        if estado == False:
            print("error de conexion")
        else:
            cursor.execute("SELECT * FROM usuario where nombre_usuario='" + nombre + "'")
            tuple = cursor.fetchone()
            if tuple != None:
                raise Exception("Ya existe ese Usuario")

    def cifrarConstranna(self,contrasenna):
        clave = contrasenna.encode('utf-8')
        letra = hashlib.sha1(clave).hexdigest()
        return letra

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
                sql2 = ("SELECT usuario.id_usuario,usuario.nombre_usuario,"
                        "  usuario.rol_usuario,usuario.password_usuario\
                    FROM\
                    usuario WHERE \
                    usuario.nombre_usuario = %s")
                cursor.execute(sql2, nombre)
                datos = cursor.fetchall()
                self.total = datos
                for valores in datos:
                    self.table.insertRow(row)
                    # id = QTableWidgetItem(str(valores[0]))
                    nombre = QTableWidgetItem(str(valores[1]))
                    rol_usuario = QTableWidgetItem(str(valores[2]))
                    contrasenna = QTableWidgetItem(str(valores[3]))

                    self.table.setItem(row, 0, nombre)
                    self.table.setItem(row, 1, rol_usuario)
                    self.table.setItem(row, 2, contrasenna)

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
            pdf.cell(w=40, h=15, txt="nombre", border=1, align='C', fill=0)
            pdf.cell(w=20, h=15, txt="Rol", border=1, align='C', fill=0)
            pdf.multi_cell(w=30, h=15, txt="contrasena", border=1, align='C', fill=0)
            val = 1
            for valor in lista_tabla:
                pdf.cell(w=10, h=15, txt=str(val), border=1, align='C', fill=0)
                pdf.cell(w=40, h=15, txt=str(valor[1]), border=1, align='C', fill=0)
                pdf.cell(w=20, h=15, txt=valor[2], border=1, align='C', fill=0)
                pdf.multi_cell(w=30, h=15, txt=valor[3], border=1, align='C', fill=0)
                val = val + 1
            pdf.output('Usuarios.pdf')
            self.mostrar_mensaje("pdf exportado correctamente")
        except Exception as e:
            self.mostrar_error("Por favor cierre el pdf")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = DialogoUsuario()
    GUI.show()
    app.exec()
