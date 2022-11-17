from difflib import SequenceMatcher as SM

import requests
from fastapi import FastAPI

from models import DiseaseModel
import constants as const

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}

@app.post("/search")
def icd_search(disease: DiseaseModel):
    """_summary_

    Args:
        disease (DiseaseModel): _description_
    """
    l_match = []
    matches_found = False
    disease_name = disease.name.lower().replace(' ', '-')
    url = const.ICD_URL.format(disease_name)
    response = requests.get(url)
    matches = response.json()[3]
    
    if matches:
        matches_found = True
        for match in matches:
            similarity_score = round(SM(None, disease_name, match[1].lower()).ratio(), 2)
            match_dict = {
                "icd_code": match[0],
                "icd_name": match[1],
                "disease_name": disease_name.replace('-', ' '),
                "similarity_score": similarity_score,
            }
            l_match.append(match_dict)
    
    return {
        "matches_found": matches_found,
        "data" : l_match
    }