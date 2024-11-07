from io import BytesIO
import pandas as pd
from fastapi import UploadFile, APIRouter, HTTPException

from domain.ModelPredictionService import ModelPredictionService
from infrastructure.models.UserModel import User
from domain.models.PersonEntityModel import PersonEntityModel


ModelPredictionController = APIRouter(prefix="/model")


@ModelPredictionController.post("/")
async def transformate_dataframe(person: PersonEntityModel):
    try:
        # se convierte el objeto persona a un diccionario El operador ** se utiliza para desempaquetar un diccionario, de manera que los pares clave-valor se conviertan en argumentos nombrados al momento de llamar a una función o crear un objeto. En este caso, **person.model.dump() desempaqueta todos los valores del diccionario devuelto por dump() y los pasa como argumentos nombrados a la función o clase que sigue. Por ejemplo, si dump() devuelve {"name": "Alice", "age": 30}, entonces **person.model.dump() sería equivalente a escribir name="Alice", age=30.

        # Se convierte el objeto persona a un diccionario
        person_dic = person.model_dump()
    except HTTPException as e:
        # Captura las excepciones HTTP lanzadas desde el servicio
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail="Error al recibir al usuario y convertirlo en un dataframe")

    return ModelPredictionService.transformate_dataframe(person_dic)


