import os
from entities.lector import LectorTXT, LectorJSON, LectorCSV
from entities.aeropuerto import Aeropuerto
import pandas as pd

def preprocess_data(df_list):
    dataframe = pd.concat(df_list)
    dataframe= dataframe["fecha_llegada"].apply(lambda t: t.replace("T", " "))
    dataframe= pd.to_datetime(dataframe["fecha_llegada"])
    return dataframe


if __name__ == '__main__':
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')

txtreader= LectorTXT(path_1)
csvreader= LectorCSV(path_2)
jsonreader= LectorJSON(path_3)

d1 = txtreader.lee_archivo()
df1= txtreader.convierte_dict_a_csv(d1)

df2= csvreader.lee_archivo()

d3= jsonreader.lee_archivo()
df3= jsonreader.convierte_dict_a_csv(d3)

df = preprocess_data([df1, df2, df3])


aeropuerto= Aeropuerto(vuelos=df, slots=3,t_embarque_nat=60,t_embarque_internat=100)
aeropuerto.asigna_slots()








