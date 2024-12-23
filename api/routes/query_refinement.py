from fastapi import APIRouter, HTTPException
from services.query_refinement_service import QueryRefinementService

router = APIRouter()
qr_service = QueryRefinementService()

@router.get('/')
async def refine_query(query: str = 'test') -> str:
	try:
		refined_query = await qr_service.refine_query(query)
		return refined_query
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	
@router.get("/test")
async def test_route():
  return {"message": "Test route working"}