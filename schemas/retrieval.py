from typing import List
from pydantic import BaseModel

class SearchResult(BaseModel):
  docno: str
  title: str
  text: str 
  score: float
  
class SearchResults(BaseModel):
  query: str
  results: List[SearchResult]

class SearchResponse(BaseModel):
  original: SearchResults
  refined: SearchResults
  summarization: str