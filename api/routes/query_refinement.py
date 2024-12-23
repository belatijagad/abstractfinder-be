from fastapi import APIRouter, HTTPException
from services.query_refinement_service import QueryRefinementService

router = APIRouter()
qr_service = QueryRefinementService()

@router.get('/', response_model=str)
async def refine_query(query: str) -> str:
	try:
		refined_query = qr_service.refine_query(query)
		return await refined_query
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	
@router.get("/test")
async def test_route():
  return {"message": "Test route working"}
