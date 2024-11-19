import pandas as pd

from slot import Slot
import datetime 


class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):
            self.slots[i] = Slot()

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Series:
        onboard_time= self.tiempo_embarque_nat
        if row["tipo_vuelo"] == "INTERNAT":
            onboard_time= self.tiempo_embarque_internat
        
        retraso= 0
        if row["retraso"] != "-":
            tmp= pd.to_datetime(row["retraso"])
            retraso = (tmp.second + tmp.minute * 60)
        
        row["fecha_despegue"]= row["fecha_llegada"] + pd.Timedelta(seconds= retraso) + pd.Timedelta(minutes= onboard_time)
        return row
        


    def encuentra_slot(self, fecha_vuelo) -> int:#dada la fecha de llegada de un vuelo intera sobre los slots del aeropuerto para comprobar 
        #si existe algún slot libre.Si no hay devuelve -1, en caso contrario devuelve el id(la clave que tiene dentro del dict "slots")
        slot= -1# Cuando tiene valor -1 significa que está ocupado. Valor 0 es que está libre.
        for id in self.slots:
            time = self.slots[id].slot_esta_libre_fecha_determinada(fecha_vuelo)#Recorro cada uno de los slots y compruebo si hay alguno libre 
            if time == 0:#Para realizar la comprobacion uso la funcion auxiliar y en caso de que el resultado sea 0,significa que esta libre.
                return id#En ese caso devuleve el slot libre.Parando la busqueda en el momento que encuentra uno libre.
    
            return slot#Si no hay ninguno libre, volvemos a poner el -1, que recuerdo que significa que están todos ocupados.



    def asigna_slot(self, vuelo) -> pd.Series:#dado un vuelo le asigna un slot, calcula la fecha de despegue del vuelo, actualiza el diccionario slot
        #con la asignacion del vuelo y delvuelve el vuelo con los campos fecha de despegue y slot actualizados.
        # Para asegurar que todo vuelo tiene un slot asociado, incrementamos la fecha de despegue en 10 minutos cada vez que no se encuentre un slot.
        #Por cada asignacion se debe de imprimir un mensaje con el slot asociado y la info del vuelo
        slot =-1
        while slot==-1:
            vuelo["fecha_llegada"]= fecha_vuelo
            slot= self.encuentra_slot(vuelo["fecha_llegada"])
            fecha_vuelo= fecha_vuelo + datetime.timedelta(minutes=10)

        vuelo= self.calcula_fecha_despegue(vuelo)
        self.slots[slot].asigna_vuelo(vuelo["id"], vuelo["fecha_llegada"], vuelo["fecha_despegue"])
        print(f"El vuelo {vuelo["id"]} con fecha de llegada{vuelo["fecha_llegada"]} y fecha de despegue {vuelo['fecha_despegue']}, tiene el slot {slot} asignado.")
        vuelo["slot"] = slot
        return slot


        

    def asigna_slots(self):#Ordenar dt de vuelos según la fecha de llegada, aplicarle a cada vuelo la funcion asigna slots(utilizar apply axis=1)para ejecutar la funcion 
        #fila por fila
       self.df_vuelos.sort_values(by=["fecha_llegada"], inplace=True)
       while len(self.df_vuelos) >0:
           af = self.df_vuelos.iloc[0:self.n_slots, :]
           af = af.apply(lambda vuelo: self.asigna_slot(vuelo), axis=1)
           self.df_vuelos = self.df_vuelos.iloc[self.n_slots:, :]

        
    
            







