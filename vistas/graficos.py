import matplotlib.pyplot as plt
import pymysql
import numpy as np
import pandas as pd


def grafico_material():
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
        madera = []
        plastico = []
        metal = []
        otros = []

        for valor in datos:
            if valor[8] == "Madera":
                madera.append(valor[8])
            elif valor[8] == "Plástico":
                plastico.append(valor[8])
            elif valor[8] == "Metal":
                metal.append(valor[8])
            else:
                otros.append(valor[8])

        if len(madera)!=0 or len(plastico)!=0 or len(metal)!=0:
            made = [len(madera), "Madera"]
            plas = [len(plastico), "Plástico"]
            me = [len(metal), "Metal"]

            lista = [made, plas, me]

            df = pd.DataFrame(lista, columns=["Cantidad", "Tipo"])

            plt.pie(df["Cantidad"], labels=df["Tipo"],
                    shadow=True,
                    explode=[0, 0.1, 0.1, ],
                    autopct='%1.1f%%')
            plt.show()
        else:
            print("NO se puede hacer")


grafico_material()
