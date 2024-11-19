import pandas as pd
import os.path
import json

class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self, extension):
        file= os.path.splitext(self.path)[1]
        if file != extension:
            raise Exception("Archivo no encontrado.")
        else:
            return True

    def lee_archivo(self):
        pass

    @staticmethod
    def convierte_dict_a_csv(data: dict):
        df = pd.DataFrame.from_dict(data)
        return df


class LectorCSV(Lector):

    def lee_archivo(self):
        df= None
        if super()._comprueba_extension(".csv"):
            df = pd.read_csv(self.path)
        return df
    


class LectorJSON(Lector):

    def lee_archivo(self):
        data= None
        if super()._comprueba_extension(".json"):
            with open(self.path, "r") as file:
                data= json.load(file)
        return data
       


class LectorTXT(Lector):

    def lee_archivo(self):
        if super()._comprueba_extension(".txt"):
            with open(self.path, "r", encoding="utf8") as file:
                header= file.readline().strip().split(", ")
                tdata= []
                for lines in file:
                    values = lines.strip().split(", ")
                    registro= {header[i]: values[i] for i in range(len(header))}
                    tdata.append(registro)
        return(tdata)

        






