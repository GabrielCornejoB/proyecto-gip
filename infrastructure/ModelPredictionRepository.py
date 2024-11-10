from typing import List
from infrastructure.models.UserModel import User
from infrastructure.models.ConsultationModel import Consultation
from pandas import DataFrame 
from dotenv import load_dotenv
load_dotenv()
import os
import pickle
from core import infrastructure_constants as constants

class ModelPredictionRepository:
    
    
    #Método de e.g. insertar usuario capa Infraestructura
    @staticmethod
    def prediction(user_df: DataFrame):

        desc_code = { 
            'R': 'Síntomas inespecíficos', 
            'Z': 'Factores preventivos', 
            'F': 'Trastornos mentales/comportamiento',
        }

        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, '..', 'core', 'models', 'modelo.pkl')
        model_boos,variables, labelencoder, min_max_scaler = pickle.load(open(filename, 'rb'))

        y_fut = model_boos.predict(user_df)
        user_df['pred']=labelencoder.inverse_transform(y_fut)


        response = user_df['pred'][0]
        desc = desc_code.get(response, 'Código no válido')

        return {
            "status": 200,
            "message": f"{response} - {desc}"
        }
    