from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.routes import search

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

# Include routers
app.include_router(
  search.router,
  prefix=f'{settings.API_STR}/search',
  tags=['search']
)

@app.get('/')
async def root():
  return {
    'message': 'Welcome to TasteGraph API',
    'version': settings.PROJECT_VERSION
  }