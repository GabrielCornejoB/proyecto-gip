from pydantic import BaseModel
from datetime import date
from typing import Literal

class PersonEntityModel(BaseModel):
    identification_type: str
    consultation_date: date
    consultation_code: int
    city: str
    gender: Literal['Masculino', 'Femenino']
    birth_date: date
    subject: str
    commitment_type: Literal['Repetida', 'Primera vez']
    appointment_status: Literal['Asistió', 'No asistió', 'Cancelada']
    procedure_type: str
    user_type: str