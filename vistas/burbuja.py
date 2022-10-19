import pymysql

def burbuja():
    con = pymysql.connect(host="localhost", user="root", passwd="", db="medios_basicos")
    cursor = con.cursor()
    estado = con.open
    # verifica que la conexion con la base de datos este correcta
    if estado == False:
        print("error de conexion")
    else:
        lista=[]
        cursor.execute("SELECT * FROM responsable")
        datos = cursor.fetchall()
        for valores in datos:
          lista.append(int(valores[3]))
        return lista
def ordenamientoBurbuja(unaLista):
    for numPasada in range(len(unaLista)-1,0,-1):
        for i in range(numPasada):
            if unaLista[i]>unaLista[i+1]:
                temp = unaLista[i]
                unaLista[i] = unaLista[i+1]
                unaLista[i+1] = temp


print(burbuja())
unaLista=burbuja()
ordenamientoBurbuja(unaLista)
print(unaLista)