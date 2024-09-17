from typing import List

from domain.models.BaseFileEntityModel import BaseFileEntity
from infrastructure.DataUploadRepository import DataUploadRepository


class DataUploadService:
    @staticmethod
    def clean_data(data_from_file: List[BaseFileEntity]):
        # Por defecto recibe un arreglo con las filas del archivo que se envía
        print("Acá irá todo el código de la limpieza y eliminación de nulos")
        # Debe retornar un arreglo con los nuevos elementos después de la limpieza, imputación, etc.
        # Esto para poder llamar la función: DataUploadRepository.insert() y pasarle ese arreglo en vez del vacío

        return DataUploadRepository.insert([])
    

    #Método de e.g. insertar usuario
    @staticmethod
    def insert_user(user):
        #Se deben todas las validaciones correspondientes
        return DataUploadRepository.insert_user(user)
    
    #Método de e.g. para traer todos los usuarios
    @staticmethod
    def get_data():
        return DataUploadRepository.get()
