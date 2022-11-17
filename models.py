from pydantic import BaseModel


class DiseaseModel(BaseModel):
    name: str
