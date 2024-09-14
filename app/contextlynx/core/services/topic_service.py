from .word_embedding_service import WordEmbeddingService
from ..models import NodeTopic

class TopicService:
    def __init__(self):
        self.word_embedding_service = WordEmbeddingService()
        pass

    def create_topic(self, user, title, language):
        embedding = self.word_embedding_service.create_word_embedding(title)

        topic = NodeTopic.objects.create(
            user=user,
            title=title,
            language=language,
            word_embedding=embedding
        )

        return topic