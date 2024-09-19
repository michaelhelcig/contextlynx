from .node_embedding_service import NodeEmbeddingService
from threading import Thread

class BackgroundWorkerService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BackgroundWorkerService, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.node_embedding_service = NodeEmbeddingService()

    def recalculate_node_embeddings(self, project):
        thread = Thread(target=self.node_embedding_service.recalculate_node_embeddings, args=(project,))
        thread.start()