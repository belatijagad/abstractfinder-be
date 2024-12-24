from typing import List
from core.config import get_settings
from openai import OpenAI

class SummarizerService:
  def __init__(self):
    self.settings = get_settings()
    self.client = OpenAI(api_key=self.settings.LLM_API_KEY, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
  async def summarize_retrieval(self, query:str, documents: List[str]) -> str:
    tagged_docs = []
    for i, doc in enumerate(documents):
        tag = f"[{(i % 3 + 1)}{'a' if i < 3 else 'b'}]"
        tagged_docs.append(f"{tag} {doc}")
    topk_concat = ';'.join(tagged_docs)
    messages = [
      {
        'role': 'system',
        'content': '''You're a research paper's abstract summarizer. Your task is to summarize retrieved research abstracts 
        and analyze their relevance to the user's query. Use the provided citation tags (e.g., [1a], [2a], etc.) when 
        referencing specific content from the documents. Each claim or piece of information in your summary should be 
        supported by at least one citation.'''
      },
      {
        'role': 'user',
        'content': f'''# Query: {query}
        # Retrieved Documents: {topk_concat}.
        
        Provide a comprehensive summary of the documents and analyze their relevance to the query, maximum of 200 words. 
        Include specific citations using the provided tags to support your points. Make sure to reference evidence from 
        both sets of documents (a and b series) when possible. Focus on how the documents collectively address the query.'''
      }
    ]
    response = self.client.chat.completions.create(
      model=self.settings.MODEL_TYPE,
      messages=messages,
      temperature=0.5,
      max_tokens=250,
    )
    retrieval_summarization = response.choices[0].message.content.strip()
    return retrieval_summarization