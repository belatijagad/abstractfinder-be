from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.routes import search, query_refinement

app = FastAPI(
  title=settings.PROJECT_NAME,
  version=settings.PROJECT_VERSION,
  description='LLM-powered search engine'
)

# Configure CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(
  search.router,
  prefix=f'{settings.API_STR}/search',
  tags=['search']
)

app.include_router(
  query_refinement.router,
  prefix=f'{settings.API_STR}/refine',
  tags=['refine']
)

@app.get('/')
async def root():
  return {
    'message': 'Welcome to Abstract Finder!',
    'version': settings.PROJECT_VERSION
  }