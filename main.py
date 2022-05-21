from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from konlpy.tag import Komoran
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

komoran = Komoran()

class Body(BaseModel):
    content: str

@app.post("/analyze")
def analyze(body:Body):
    body_dict = body.dict()
    raw_keywords = list(komoran.pos(body_dict['content']))
    keywords = list(map(lambda x:x[0], filter(lambda x: len(x[0]) > 1 and (x[1] in ["NNG", "NNP", "SL"]),  raw_keywords)))
    result = {} 
    for keyword in keywords:
      if result.get(keyword) == None:
        result[keyword] = 1
      else:
        result[keyword] += 1

    return result
