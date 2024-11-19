import datetime as dt

class Slot:
    def __init__(self):
        self.id = None
        self.fecha_inicial = None
        self.fecha_final = None

    def asigna_vuelo(self, id, fecha_llegada, fecha_despegue):
        self.id = id
        self.fecha_inicial= fecha_llegada
        self.fecha_final= fecha_despegue

    def slot_esta_libre_fecha_determinada(self, fecha):#0 significa que el slot está libre.
        if self.fecha_inicial is None or self.fecha_final is None:
            return 0#si no hay fecha de llegada o despegue,no hay ni va a haber ningun vuelo ocupando el slot. Por lo que estará libre(0). 
        elif self.fecha_inicial <= fecha and self.fecha_final >= fecha:
            return self.fecha_final - fecha#Si la fecha está entre la llegada y el despegue de un avión, ese slot estará ocupado.Devuelve el tiempo que queda hasta que se desocupe
        else:#Por último si la fecha no se encuentra entre la llegada o el despegue de un vuelo, el slot estara libre(0)
            return 0

