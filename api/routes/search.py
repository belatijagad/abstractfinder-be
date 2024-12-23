from typing import List
from fastapi import APIRouter, HTTPException
from services.retrieval_service import RetrievalService
from schemas.retrieval import SearchResult

router = APIRouter()
retrieval_service = RetrievalService()

@router.get('/index')
async def index() -> str:
	try:
		await retrieval_service._create_index()
		return 'Successfully indexed'
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get('/search', response_model=List[SearchResult], response_model_exclude_none=True)
async def search(query: str, k: int = 30):
  try:
    results = retrieval_service.retrieve(query, k)
    return [{'docno': doc['docno'], 'text': doc['text'], 'score': score} for doc, score in results]
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))