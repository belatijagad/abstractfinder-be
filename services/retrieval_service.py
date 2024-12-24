import os
import torch
import shutil
import ir_datasets 
import pyterrier as pt
from transformers import BertForSequenceClassification, BertTokenizer

class RetrievalService:
  def __init__(self) -> None:
    if not pt.started(): pt.java.init()
    self.index_ref = self._create_index()
    self.retriever = pt.BatchRetrieve(self.index_ref, wmodel='BM25', metadata=['docno', 'text', 'title'])
    model_path = 'reranker_weights'
    self.model = BertForSequenceClassification.from_pretrained(model_path)
    self.tokenizer = BertTokenizer.from_pretrained(model_path)
    self.model.eval()
  def _create_index(self) -> str:
    dataset = ir_datasets.load('cranfield')
    docs = [{'docno': d.doc_id, 'text': d.text, 'title': d.title} for d in dataset.docs_iter()]
    index_dir = os.path.abspath('index')
    if os.path.exists(index_dir): shutil.rmtree(index_dir)
    os.makedirs(index_dir, exist_ok=True)
    indexer = pt.IterDictIndexer(index_dir, meta={'docno': 60, 'text': 10000, 'title': 1000})
    return indexer.index(docs)
  def retrieve(self, query: str, k: int = 30) -> list:
    try:
      initial_results = self.retriever.search(query)[:50]
      if len(initial_results) == 0: return []
      scores = []
      with torch.no_grad():
        for doc in initial_results.itertuples():
          inputs = self.tokenizer(text=query, text_pair=doc.text, truncation=True, max_length=128, padding=True, return_tensors='pt')
          score = self.model(**inputs).logits[0, 1].item()
          scores.append({'docno': doc.docno, 'title': doc.title.title(), 'text': doc.text, 'score': score})
      return sorted(scores, key=lambda x: x['score'], reverse=True)[:k]
    except Exception as _:
      return []