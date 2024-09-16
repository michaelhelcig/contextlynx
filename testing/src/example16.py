from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from collections import defaultdict
import numpy as np
from typing import List, Tuple, Dict


class NodeTopicDataType:
    OTHER = 'OTHER'
    PERSON = 'PERSON'
    ORGANIZATION = 'ORGANIZATION'
    LOCATION = 'LOCATION'
    DATE = 'DATE'
    EVENT = 'EVENT'
    PRODUCT = 'PRODUCT'
    WORK_OF_ART = 'WORK_OF_ART'
    LAW = 'LAW'
    LANGUAGE = 'LANGUAGE'
    QUANTITY = 'QUANTITY'
    PERCENT = 'PERCENT'
    MONEY = 'MONEY'
    TIME = 'TIME'
    URL = 'URL'
    EMAIL = 'EMAIL'
    PHONE_NUMBER = 'PHONE_NUMBER'
    NATIONALITY = 'NATIONALITY'
    RELIGION = 'RELIGION'
    TITLE = 'TITLE'
    VEHICLE = 'VEHICLE'
    ANIMAL = 'ANIMAL'
    PLANT = 'PLANT'
    MEDICAL_CONDITION = 'MEDICAL_CONDITION'
    SPORTS_TEAM = 'SPORTS_TEAM'
    INDUSTRY = 'INDUSTRY'
    COMPANY = 'COMPANY'


class WordEmbedding:
    def __init__(self, model, embedding_normalized):
        self.model = model
        self.embedding_normalized = embedding_normalized


class ExtendedBertService:
    def __init__(self):
        self.model_name = 'dbmdz/bert-large-cased-finetuned-conll03-english'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_name)
        self.id2label = self.model.config.id2label
        self.label_map = {
            'B-PER': NodeTopicDataType.PERSON,
            'I-PER': NodeTopicDataType.PERSON,
            'B-ORG': NodeTopicDataType.ORGANIZATION,
            'I-ORG': NodeTopicDataType.ORGANIZATION,
            'B-LOC': NodeTopicDataType.LOCATION,
            'I-LOC': NodeTopicDataType.LOCATION,
            'B-MISC': NodeTopicDataType.OTHER,
            'I-MISC': NodeTopicDataType.OTHER,
            'B-DATE': NodeTopicDataType.DATE,
            'I-DATE': NodeTopicDataType.DATE,
            'B-TIME': NodeTopicDataType.TIME,
            'I-TIME': NodeTopicDataType.TIME,
            'B-MONEY': NodeTopicDataType.MONEY,
            'I-MONEY': NodeTopicDataType.MONEY,
            'B-PERCENT': NodeTopicDataType.PERCENT,
            'I-PERCENT': NodeTopicDataType.PERCENT,
            # You can add more mappings if the model supports additional categories
        }

    def get_named_entities(self, text: str) -> Dict[str, List[Tuple[str, int, int]]]:
        inputs = self.tokenizer(text, return_tensors="pt", return_offsets_mapping=True, truncation=False)
        max_length = 512
        all_entities = defaultdict(list)

        for i in range(0, inputs.input_ids.shape[1], max_length):
            chunk_input = {k: v[:, i:i + max_length] for k, v in inputs.items() if k != 'offset_mapping'}
            offset_mapping = inputs.offset_mapping[0, i:i + max_length]

            with torch.no_grad():
                outputs = self.model(**chunk_input)

            predictions = torch.argmax(outputs.logits, dim=2)[0]

            current_entity = None
            for token_idx, (prediction, (start_char, end_char)) in enumerate(zip(predictions, offset_mapping)):
                label = self.id2label[prediction.item()]
                if label != "O":
                    if current_entity is None:
                        current_entity = (label, start_char.item(), end_char.item())
                    elif current_entity[0].split('-')[1] == label.split('-')[1]:
                        current_entity = (current_entity[0], current_entity[1], end_char.item())
                    else:
                        all_entities[self.label_map.get(current_entity[0], NodeTopicDataType.OTHER)].append(
                            (text[current_entity[1]:current_entity[2]], current_entity[1], current_entity[2])
                        )
                        current_entity = (label, start_char.item(), end_char.item())
                elif current_entity is not None:
                    all_entities[self.label_map.get(current_entity[0], NodeTopicDataType.OTHER)].append(
                        (text[current_entity[1]:current_entity[2]], current_entity[1], current_entity[2])
                    )
                    current_entity = None

            if current_entity is not None:
                all_entities[self.label_map.get(current_entity[0], NodeTopicDataType.OTHER)].append(
                    (text[current_entity[1]:current_entity[2]], current_entity[1], current_entity[2])
                )

        return dict(all_entities)


def get_cosine_similarity(embedding1, embedding2):
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity([embedding1], [embedding2])[0, 0]


# Test script
if __name__ == "__main__":
    extended_bert_service = ExtendedBertService()

    # Test text
    text = """
    The meeting is scheduled for June 5, 2024, at 10:00 AM.
    Please refer to the financial report of $1,200,000 and the percentage increase of 5% over the last quarter.
    Contact us via email at info@company.com or call +123-456-7890.
    """

    print("Testing get_named_entities method:")
    entities = extended_bert_service.get_named_entities(text)
    for entity_type, entity_list in entities.items():
        print(f"\n{entity_type}:")
        for entity in entity_list:
            print(f"  Text: {entity[0]}, Start: {entity[1]}, End: {entity[2]}")


    print("\nTest script completed.")
