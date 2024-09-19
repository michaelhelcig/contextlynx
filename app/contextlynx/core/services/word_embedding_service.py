from transformers import BertModel, BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
import numpy as np
from ..models import WordEmbedding

class WordEmbeddingService:
    def __init__(self):
        self.embedding_model = 'bert-base-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(self.embedding_model)
        self.model = BertModel.from_pretrained(self.embedding_model)

    def create_word_embedding(self, text):
        if not text:
            raise ValueError("Input text cannot be empty.")

        embedding = self._get_embedding(text)
        word_embedding = WordEmbedding(
            embedding_model=self.embedding_model,
            embedding_vector=embedding
        )
        return word_embedding

    def _get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        normalized_embeddings = embeddings / np.linalg.norm(embeddings)
        return normalized_embeddings.tolist()

    @staticmethod
    def get_cosine_similarity(embedding1, embedding2):
        return cosine_similarity([embedding1], [embedding2])[0, 0]

def get_word_embedding_service():
    return WordEmbeddingService()
