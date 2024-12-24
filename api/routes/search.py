from typing import List
from fastapi import APIRouter, HTTPException
from services.retrieval_service import RetrievalService
from services.summarizer_service import SummarizerService
from schemas.retrieval import SearchResponse
from api.routes.query_refinement import qr_service

router = APIRouter()
retrieval_service = RetrievalService()
summarizer_service = SummarizerService()

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
    top_texts = [text['text'] for text in original_results[:3]] + [text['text'] for text in refined_results[:3]]
    summarization = await summarizer_service.summarize_retrieval(query, top_texts)
    return {
      'original': {'query': query, 'results': original_results},
      'refined': {'query': refined_query,'results': refined_results},
      'summarization': summarization,
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))