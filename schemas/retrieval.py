from pydantic import BaseModel

class SearchResult(BaseModel):
  docno: str
  text: str 
  score: float