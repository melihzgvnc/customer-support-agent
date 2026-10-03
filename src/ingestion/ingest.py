import json
import os
from datetime import datetime
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from rank_bm25 import BM25Okapi

class HybridIngestion:

    def __init__(self):
        self.client = PersistentClient("../index/dense")
        self.collection = self.client.get_or_create_collection(
            name="company_support_guidelines",
            embedding_function=SentenceTransformerEmbeddingFunction(
                model_name="BAAI/bge-small-en-v1.5"
            ),
            metadata={
                "description": "first ingestion of FAQs",
                "created": str(datetime.now())
            }
        )
        self.load_data()
        self.parse_data()
        self.chromadb_ingestion()
        self.bm25_ingestion()

    def load_data(self):
        with open("../data/mock_kb_chunks.json") as f:
            self.data = json.load(f)

    def parse_data(self):
        self.ids = []
        self.documents = []
        self.metadatas = []
        for doc in self.data:
            self.ids.append(doc['id'])
            self.documents.append(doc['text'])
            self.metadatas.append(doc['metadata'])
        
    def chromadb_ingestion(self):
        self.collection.add(ids=self.ids, documents=self.documents, metadatas=self.metadatas)

    def bm25_ingestion(self):
        tokenized_corpus = [doc.split(" ") for doc in self.documents]

        os.makedirs("../index/sparse", exist_ok=True)
        with open("../index/sparse/corpus.json", "x", encoding="utf-8") as f:
            json.dump(tokenized_corpus, f, ensure_ascii=False)
        
        with open("../index/sparse/ids.json", "x", encoding="utf-8") as f:
            json.dump(self.ids, f, ensure_ascii=False)

if __name__ == "__main__":
    ingestion = HybridIngestion()