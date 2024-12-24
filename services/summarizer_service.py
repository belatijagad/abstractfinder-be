from typing import List
from core.config import get_settings
from openai import OpenAI

class SummarizerService:
  def __init__(self):
    self.settings = get_settings()
    self.client = OpenAI(api_key=self.settings.LLM_API_KEY, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
  async def summarize_retrieval(self, query:str, documents: List[str]) -> str:
    topk_concat = ''
    for i, doc in enumerate(documents): topk_concat += f'Document {i}: {doc}; '
    messages = [
      {'role': 'system', 'content': 'You\'re a research paper\'s abstract summarizer. Your task is to summarize the top-k retrieved research abstract and elaborate to the user whether it\'s relevant or not to the user\'s query.'},
      {'role': 'user', 'content': f'# Query: {query}\n # Retrieved Documents: {topk_concat}. \nProvide only the whole summarization of given document and whether the query fits with the given documents and state the reasoning, there\'s no need to point which document.'}
    ]
    response = self.client.chat.completions.create(
      model=self.settings.MODEL_TYPE,
      messages=messages,
      temperature=0.5,
      max_tokens=250,
    )
    retrieval_summarization = response.choices[0].message.content.strip()
    return retrieval_summarization