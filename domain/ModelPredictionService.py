import datetime
import os
from pandas import DataFrame 
from fastapi import HTTPException
import pandas as pd

from infrastructure.ModelPredictionRepository import ModelPredictionRepository
import pickle



class ModelPredictionService:

    # Método para transformar los valores de persona
    @staticmethod
    def transformate_dataframe(person: dict):
        # Se deben todas las validaciones correspondientes
        # Construir la ruta basada en la ubicación del archivo actual
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, '..', 'core', 'models', 'modelo.pkl')
        model_boos,variables, labelencoder, min_max_scaler = pickle.load(open(filename, 'rb'))

        min_max_scaler1 = min_max_scaler[0]
        min_max_scaler2 = min_max_scaler[1]
        min_max_scaler3 = min_max_scaler[2]

        # Validar 'identification_type' es un string no vacío
        if not isinstance(person['identification_type'], str) or not person['identification_type'].strip():
            raise ValueError("El campo 'identification_type' debe ser un string no vacío.")

        # Validar 'consultation_date' es una fecha válida y no futura
        if not isinstance(person['consultation_date'], datetime.date):
            raise ValueError("El campo 'consultation_date' debe ser una fecha válida.")
        if person['consultation_date'] > datetime.date.today():
            raise ValueError("El campo 'consultation_date' no puede ser una fecha futura.")

        # Validar 'consultation_code' es un entero positivo
        if not isinstance(person['consultation_code'], int) or person['consultation_code'] <= 0:
            raise ValueError("El campo 'consultation_code' debe ser un entero positivo.")
        
        # Validar 'city' es un string no vacío
        if not isinstance(person['city'], str) or not person['city'].strip():
            raise ValueError("El campo 'city' debe ser un string no vacío.")

        # Validar 'gender' es 'Masculino' o 'Femenino'
        if person['gender'] not in ['Masculino', 'Femenino']:
            raise ValueError("El campo 'gender' debe ser 'Masculino' o 'Femenino'.")

        # Validar 'birth_date' es una fecha válida y en el pasado
        if not isinstance(person['birth_date'], datetime.date):
            raise ValueError("El campo 'birth_date' debe ser una fecha válida.")
        if person['birth_date'] >= datetime.date.today():
            raise ValueError("El campo 'birth_date' debe ser una fecha en el pasado.")
        if person['birth_date'] > person['consultation_date']:
            raise ValueError("El campo 'birth_date' debe ser anterior a 'consultation_date'.")

        # Validar 'subject' es un string no vacío
        if not isinstance(person['subject'], str) or not person['subject'].strip():
            raise ValueError("El campo 'subject' debe ser un string no vacío.")

        # Validar 'commitment_type' es 'Repetida' o 'Primera vez'
        if person['commitment_type'] not in ['Repetida', 'Primera vez']:
            raise ValueError("El campo 'commitment_type' debe ser 'Repetida' o 'Primera vez'.")

        # Validar 'appointment_status' es 'Asistió', 'No asistió' o 'Cancelada'
        if person['appointment_status'] not in ['Asistió', 'No asistió', 'Cancelada']:
            raise ValueError("El campo 'appointment_status' debe ser 'Asistió', 'No asistió' o 'Cancelada'.")

        # Validar 'procedure_type' es un string no vacío
        if not isinstance(person['procedure_type'], str) or not person['procedure_type'].strip():
            raise ValueError("El campo 'procedure_type' debe ser un string no vacío.")

        # Validar 'user_type' es un string no vacío
        if not isinstance(person['user_type'], str) or not person['user_type'].strip():
            raise ValueError("El campo 'user_type' debe ser un string no vacío.")
        
        #Transformar el diccionario a un DataFrame
        person_df = pd.DataFrame([person])

        # Diccionario de mapeo de nombres de columnas
        column_mapping = {
            'consultation_code': 'codigo de la consulta',
            'user_type': 'Tipo de Usuario',
            'commitment_type': 'Tipo de Compromiso',
            'identification_type': 'tipo de identificacion',  # Aquí puedes ajustar según el valor específico de cada tipo
            'city': 'Ciudad',                            # Ajusta según la ciudad específica
            'appointment_status': 'Estado de la Cita',   # Ajusta según el estado específico
            'gender': 'Género',                         # Ajusta según el género específico
            'subject': 'Asunto',                       # Ajusta según el asunto específico
            'procedure_type': 'Tipo de Procedimiento',
            'consultation_date': 'fecha de consulta',
            'birth_date': 'Fecha Nacimiento'
        }

        # Renombrar las columnas en el DataFrame
        person_df.rename(columns=column_mapping, inplace=True)



        #Transformaciones para predición

        person_prepared=person_df.copy()
        person_prepared = pd.get_dummies(person_prepared, columns=['Tipo de Usuario','Tipo de Compromiso'], drop_first=True)
        person_prepared = pd.get_dummies(person_prepared, columns=['tipo de identificacion','Ciudad', 'Estado de la Cita', 'Género', 'Asunto', 'Tipo de Procedimiento'], drop_first=False)

        

        person_prepared['fecha de consulta'] = pd.to_datetime(person_prepared['fecha de consulta'], errors='coerce')
        person_prepared['Fecha Nacimiento'] = pd.to_datetime(person_prepared['Fecha Nacimiento'], errors='coerce')

        person_prepared['fecha_de_consulta_ordinal'] = person_prepared['fecha de consulta'].apply(lambda x: x.toordinal())
        person_prepared['fecha_nacimiento_ordinal'] = person_prepared['Fecha Nacimiento'].apply(lambda x: x.toordinal())
        person_prepared = person_prepared.drop(columns=['fecha de consulta','Fecha Nacimiento'])

        #Se adicionan las columnas faltantes
        person_prepared=person_prepared.reindex(columns=variables,fill_value=0)

        #Normalización

        person_prepared[['codigo de la consulta']]= min_max_scaler1.transform(person_prepared[['codigo de la consulta']])
        person_prepared[['fecha_de_consulta_ordinal']]= min_max_scaler2.transform(person_prepared[['fecha_de_consulta_ordinal']])
        person_prepared[['fecha_nacimiento_ordinal']]= min_max_scaler3.transform(person_prepared[['fecha_nacimiento_ordinal']])

        return ModelPredictionRepository.prediction(person_prepared)

