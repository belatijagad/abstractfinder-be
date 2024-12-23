from pydantic_settings import BaseSettings
from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Information Retrieval Final Project')
  PROJECT_VERSION: str = os.getenv('PROJECT_VERSION', '1.0.0')
  API_STR: str = os.getenv('API_STR', '/api')
  LLM_API_KEY: str = os.getenv('LLM_API_KEY', '69420')
  MODEL_TYPE: str = os.getenv('MODEL_TYPE', 'gemini-1.5-flash')
  INDEX_PATH: str = os.getenv('INDEX_PATH', '/index')
  DEBUG: bool = os.getenv('DEBUG', False)

  class Config:
    case_sensitive = True
    env_file = '.env'

@lru_cache()
def get_settings() -> Settings:
  return Settings()

settings = get_settings()