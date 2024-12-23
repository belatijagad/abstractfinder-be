from typing import List
from fastapi import APIRouter, HTTPException
from services.retrieval_service import RetrievalService
from schemas.retrieval import SearchResponse
from api.routes.query_refinement import qr_service

router = APIRouter()
retrieval_service = RetrievalService()

@router.get('/index')
async def index() -> str:
	try:
		await retrieval_service._create_index()
		return 'Successfully indexed'
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get('/search', response_model=SearchResponse)
async def search(query: str, k: int = 30):
  try:
    original_results = retrieval_service.retrieve(query, k)
    refined_query = await qr_service.refine_query(query)
    refined_results = retrieval_service.retrieve(refined_query, k)
    return {
      'original': {
        'query': query,
        'results': [{'docno': doc['docno'], 'text': doc['text'], 'title': doc['title'].title(), 'score': score} for doc, score in original_results],
      },
      'refined': {
        'query': refined_query,
        'results': [{'docno': doc['docno'], 'text': doc['text'], 'title': doc['title'].title(), 'score': score} for doc, score in refined_results],
      }
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))