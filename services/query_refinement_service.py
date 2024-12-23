from core.config import get_settings
from openai import OpenAI

class QueryRefinementService:
  def __init__(self):
    self.settings = get_settings()
    self.client = OpenAI(api_key=self.settings.LLM_API_KEY, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
  async def refine_query(self, query:str) -> str:
    messages = [
      {'role': 'system', 'content': 'You\'re a research paper\'s abstract query refinement assistant. Your task is to rewrite the search queries to be more precise and focused, while maintaining the user\'s original intent.'},
      {'role': 'user', 'content': f'Given the research paper abstract query: [{query}]. Provide only the refined query as the output.'}
    ]
    response = self.client.chat.completions.create(
      model=self.settings.MODEL_TYPE,
      messages=messages,
      temperature=0.5,
      max_tokens=50,
    )
    refined_query = response.choices[0].message.content.strip()
    return refined_query