from fastapi import APIRouter, HTTPException
from services.retrieval_service import RetrievalService

router = APIRouter()
rs_service = RetrievalService()

@router.get('/index')
async def index() -> str:
	try:
		await rs_service.index()
		return "success indexing"
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.get('/search')
async def search(query: str, k: int = 30):
  try:
    results = rs_service.retrieve(query, k)  # Removed await
    print(results)
    return results.to_dict(orient="records")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
