import ir_datasets
import pyterrier as pt
import pandas as pd
from pyterrier.transformer import Transformer
import numpy as np
from transformers import BertForSequenceClassification, BertTokenizer
import os
import shutil
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW

class RetrievalService:
  def __init__(self):
    self.index_ref = self.index()

    # Base retriever BM25
    self.retriever = pt.BatchRetrieve(
        self.index_ref,
        wmodel="BM25",
        metadata=["docno", "text"]
    )
    self.retriever_top50 = self.retriever % 50

    # Reranker BERT
    model_path = "reranker_weights"
    self.model = BertForSequenceClassification.from_pretrained(model_path)
    self.tokenizer = BertTokenizer.from_pretrained(model_path)
    self.reranker = BertReranker(self.model, self.tokenizer)

    self.pipeline = self.retriever_top50 >> self.reranker

  def index(self):
    # Initialize PyTerrier
    if not pt.started():
        pt.init()

    # Load Cranfield dataset
    dataset = ir_datasets.load("cranfield")

    # Convert docs into a DataFrame
    docs = list(dataset.docs_iter())
    docs_df = pd.DataFrame([{ "docno": d.doc_id, "text": d.text, "title": d.title } for d in docs])

    # Directory for the index
    base_dir = os.path.abspath("./var")
    index_dir = os.path.join(base_dir, "index")

    # Ensure the base directory exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)

    # Remove the index directory if it exists
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)

    # Create a new index directory
    os.makedirs(index_dir, exist_ok=True)

    # Index the documents
    indexer = pt.IterDictIndexer(
        index_dir,
        meta={
            "docno": 60,   # docno max length 60 chars
            "text": 10000  # text max length 10,000 chars (e.g.)
        }
    )
    index_ref = indexer.index(docs_df.to_dict(orient="records"))
    return index_ref

  def retrieve(self, query:str, k:int=30):


    test_queries_df = pd.DataFrame([
      {"qid": "q_test", "query": query}
    ])

    res = self.pipeline.transform(test_queries_df)
    res_top30 = pd.DataFrame(res).sort_values("score", ascending=False).head(k)

    
    return res_top30

class BertReranker(Transformer):
    def __init__(self, model, tokenizer, max_len=128):
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.model.eval()

    def transform(self, df):
        # df akan berisi kolom [qid, query, docno, text, rank, score] dsb.
        # Kita perlu menghitung skor relevansi BERT lalu menimpa kolom "score".

        # Buat list of queries, list of docs
        queries = df["query"].tolist()
        docs = df["text"].tolist()

        all_scores = []

        with torch.no_grad():
            for query_text, doc_text in zip(queries, docs):
                inputs = self.tokenizer(
                    query_text,
                    doc_text,
                    truncation=True,
                    max_length=self.max_len,
                    padding="max_length",
                    return_tensors="pt"
                )
                input_ids = inputs["input_ids"]
                attention_mask = inputs["attention_mask"]
                token_type_ids = inputs["token_type_ids"]

                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    token_type_ids=token_type_ids
                )
                # logits shape: [batch_size=1, num_labels=2]
                logits = outputs.logits
                # Kita ambil logit untuk label "relevan" (label=1), misal index=1
                score = logits[0, 1].item()
                all_scores.append(score)

        df["score"] = all_scores
        return df





