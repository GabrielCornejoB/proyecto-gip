from pandas import DataFrame 
from fastapi import HTTPException
import pandas as pd
from infrastructure.DataUploadRepository import DataUploadRepository
from core import domain_constants as constants
from cie.cie10 import CIECodes


class DataUploadService:
    @staticmethod
    def clean_data(rips_df: DataFrame, monthly_df: DataFrame):

        # Verificación de que las columnas necesarias existen
        if len(rips_df.columns) != constants.COLUMNAS_RIPS:
            raise HTTPException(status_code=400, detail="Columnas faltantes en el archivo RIPS")
        
        if len(monthly_df.columns) != constants.COLUMNAS_MENSUAL:
            raise HTTPException(status_code=400, detail="Columnas faltantes en el archivo mensual")
        
        # Verificación de que las columnas necesarias existen

        required_columns_rips = [
        constants.IDENTIFICACION_ENCRIPTADA,
        constants.TIPO_IDENTIFICACION,
        constants.FECHA_CONSULTA,
        constants.NRO_AUTORIZACION,
        constants.CODIGO_CONSULTA,
        constants.FINALIDAD_CONSULTA,
        constants.CAUSA_EXTERNA,
        constants.COD_DX_PRINCIPAL,
        constants.COD_DX_REL_1,
        constants.COD_DX_REL_2,
        constants.COD_DX_REL_3,
        constants.TIPO_DIAGNOSTICO,
        constants.VALOR_CONSULTA,
        constants.VALOR_CUOTA_MODERADORA,
        constants.VALOR_NETO_PAGAR
        ]
        
        # Verificación de que todas las columnas existen en el DataFrame de RIPS
        for col in required_columns_rips:
            if col not in rips_df.columns:
                raise HTTPException(status_code=400, detail=f"Columna '{col}' no encontrada en el archivo RIPS")
        
        required_columns_mensual = [
        constants.TIPO_IDENTIFICACION_PACIENTE,
        constants.CIUDAD,
        constants.DIRECCION,
        constants.BARRIO,
        constants.CORREO_ELECTRONICO,
        constants.GENERO,
        constants.FECHA_NACIMIENTO,
        constants.EDAD,
        constants.CONSECUTIVO,
        constants.ASUNTO,
        constants.TIPO_COMPROMISO,
        constants.FECHA_CITA,
        constants.ESTADO_CITA,
        constants.TIPO_PROCEDIMIENTO,
        constants.TIPO_USUARIO,
        constants.IDENTIFICACION_ENCRIPTADA  # Esta ya estaba definida, puedes reutilizarla
        ]

        # Verificación de que todas las columnas existen en el DataFrame mensual
        for col in required_columns_mensual:
            if col not in monthly_df.columns:
                raise HTTPException(status_code=400, detail=f"Columna '{col}' no encontrada en el archivo Mensual")
        
        
        
        #Limpieza y transformación de datos

        try:
            #1) Integración de los datos (Join)

            #Se eliminan las columnas que no se van a usar
            rips_df = rips_df.drop('cod dx rel 1', axis=1)
            rips_df = rips_df.drop('cod dx rel 2', axis=1)
            rips_df = rips_df.drop('cod dx rel 3', axis=1)
            rips_df = rips_df.drop('nro de autorizacion', axis=1)
            rips_df = rips_df.drop('finalidad de la consulta', axis=1)
            rips_df = rips_df.drop('causa externa', axis=1)
            rips_df = rips_df.drop('tipo de diagnostico', axis=1)


            monthly_df = monthly_df.drop('Tipo de Identificación del Paciente', axis=1)
            monthly_df = monthly_df.drop('Correo Electrónico', axis=1)
            monthly_df = monthly_df.drop('Dirección', axis=1)
            monthly_df = monthly_df.drop('Ciudad', axis=1)

            #Se renombra la columna de la fecha de la cita para que coincida con la tabla Rips
            monthly_df.rename(columns={'Fecha de la Cita': 'fecha de consulta'}, inplace=True)

            # Reemplaza los valores en la columna 'Asunto' usando un diccionario
            monthly_df.replace({'Asunto': constants.VALORES_CORRECTOS}, inplace=True)

            #Join
            data = pd.merge(rips_df, monthly_df, on=['identificacion encriptada','fecha de consulta'],how='inner')

            #Corrección del tipo de datos object a categorías
            data['tipo de identificacion']=data['tipo de identificacion'].astype('category')
            data['cod dx principal']=data['cod dx principal'].astype('category')
            data['identificacion encriptada']=data['identificacion encriptada'].astype('category')
            data['Barrio']=data['Barrio'].astype('category')
            data['Género']=data['Género'].astype('category')
            data['Asunto']=data['Asunto'].astype('category')
            data['Tipo de Compromiso']=data['Tipo de Compromiso'].astype('category')
            data['Estado de la Cita']=data['Estado de la Cita'].astype('category')
            data['Tipo de Procedimiento']=data['Tipo de Procedimiento'].astype('category')
            data['Tipo de Usuario']=data['Tipo de Usuario'].astype('category')

            #2) Eliminación de vars redundantes e irrelevantes para tabla resultante
            data = data.drop('Edad',axis=1)
            data = data.drop('Consecutivo',axis=1)
            data = data.drop('identificacion encriptada',axis=1)

            #Se eliminan las columnas que tienen solamente un valor
            data = data.drop('valor de la consulta',axis=1)
            data = data.drop('valor cuota moderadora',axis=1)
            data = data.drop('valor neto a pagar',axis=1)

            #Descripción de códigos CIE
            cie = CIECodes()

            cie_dict = {} 

            for code, content in cie.tree.items():
                full_info = cie.info(code=code)  # Cargar la propiedad 'multiple_descriptions'
                
                # Verificar que 'full_info' y 'description' existan antes de asignar
                if full_info and 'description' in full_info:
                    cie_dict[code] = full_info['description']  # Asignar directamente la descripción

            data['Descripcion dx principal'] = data['cod dx principal'].map(cie_dict)
            #Convertimos el tipo de fecha
            
            # Convertir las fechas en el DataFrame 'data' a formato YYYY-MM-DD
            data['fecha de consulta'] = pd.to_datetime(data['fecha de consulta'], format='%d/%m/%Y', errors='coerce')
            data['Fecha Nacimiento'] = pd.to_datetime(data['Fecha Nacimiento'], format='%d/%m/%Y', errors='coerce')


            return DataUploadRepository.insert(data)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno durante la limpieza de datos: {str(e)}")
        



        

    # Método de e.g. insertar usuario
    @staticmethod
    def insert_user(user):
        # Se deben todas las validaciones correspondientes
        return DataUploadRepository.insert_user(user)

    # Método de e.g. para traer todos los usuarios
    @staticmethod
    def get_data():
        return DataUploadRepository.get()
