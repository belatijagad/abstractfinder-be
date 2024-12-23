from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Information Retrieval Final Project')
  PROJECT_VERSION: str = os.getenv('PROJECT_VERSION', '1.0.0')
  API_V1_STR: str = os.getenv('API_STR', '/api/')
  DEBUG: bool = os.getenv('DEBUG', False)

  class Config:
    case_sensitive = True
    env_file = '.env'

@lru_cache()
def get_settings() -> Settings:
  return Settings()

settings = get_settings()