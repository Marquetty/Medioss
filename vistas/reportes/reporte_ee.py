"""from pymysql import connect


class reportePDF(object):

    def __init__ (self , titulo,cabecera,datos,nombrePDF):
        super (reportePDF,self).__init()


        self.titulo=titulo
        self.cabecera=cabecera
        self.datos=datos
        self.nombrePDF=nombrePDF
        self.estilos=.getSampleStyleSheet()

    @staticmethod
    def _encabezadoPiePagina(canvas,archivoPDF):
    canvas.saveState()
    estilos=getSampleStyleSheet()

    #Encabezado
    encabezadoNOmbre=Paragraph("Andres nio 1.0",estilos["Normal"])
    anchura,altura=encabezadoNombre.wrap(archivoPDF.width,archivoPDF.topMargin)

    fecha = utcnow().to("local").format("dddd,DD-MMMM-YYYY", locale="es")
    encabezadoFecha = Paragraph(fechaReporte,alineacion)
    anchura,altura=encabezadoFecha.wrap(archivoPDF.whidth,archivoPDF,topMargin)
    encabezadoFecha.drawOn(canvas,archivoPDF.leftMargin,736)





    piePagina.drawOn(canvas,archivoPDF,leftMargin,15*mm+(0.2*inch))

def generarReporte():
    def dic_factory (cursor,row):
        d={}
        for idx,col in enumerate(cursor.description):
            d[col[0]]= row[idx]
        return d
    conexionDB= connect("Medios_basicos")
    conexionDB.row_factory=dic_factory
    cursor=conexionDB.cursor()
    cursor.execute("Select ")
    datos= cursor.fetchall()
    conexionDB.close()

    titulo= "Listado de Usuario"
    cabecera = (
                ("DNI","D.N.I"),
                ("nombre","NOmbre"),
                ("apellido","Apellido"),
                ("fecha","fecha"),

    )
    nombrePDF="Listado de Usuario.pdf"
    reporte =reportePDF(titulo,cabecera,datos,nombrePDF).exportar()
    print(reporte)"""