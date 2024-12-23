from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

router = APIRouter()

async def search():
  return 'Hello world'