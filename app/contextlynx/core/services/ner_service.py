import spacy
from ..models import NodeTopicDataType


class NERService:
    def __init__(self):
        self.model = 'en_core_web_lg'
        self.nlp = spacy.load('en_core_web_lg')

    def get_named_entities(self, text):
        doc = self.nlp(text)
        entities = []

        # Step 1: Collect all entities
        for ent in doc.ents:
            data_type = NERService._map_entity(ent.label_)
            text = ent.text
            entities.append({
                'title': text,
                'data_type': data_type,
            })

        # Step 2: Filter out entities that are contained within others
        filtered_entities = []
        for i, entity in enumerate(entities):
            is_contained = False
            for j, other in enumerate(entities):
                if i != j and other['data_type'] == entity['data_type'] and \
                        entity['title'].lower() in other['title'].lower() and \
                        entity['title'].lower() != other['title'].lower():
                    # If the entity is contained within another entity
                    is_contained = True
                    break

            if not is_contained:
                filtered_entities.append(entity)

        # Step 3: Remove duplicates based on title and data_type
        unique_entities = []
        seen = set()
        for entity in filtered_entities:
            key = (entity['title'].lower(), entity['data_type'])
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)

        return unique_entities

    @staticmethod
    def _map_entity(ent_type):
        """Map spaCy entity types to NodeTopicDataType"""
        mapping = {
            "PERSON": NodeTopicDataType.PERSON,
            "ORG": NodeTopicDataType.ORGANIZATION,
            "GPE": NodeTopicDataType.LOCATION,
            "LOC": NodeTopicDataType.LOCATION,
            "DATE": NodeTopicDataType.DATE,
            "EVENT": NodeTopicDataType.EVENT,
            "PRODUCT": NodeTopicDataType.PRODUCT,
            "WORK_OF_ART": NodeTopicDataType.WORK_OF_ART,
            "LAW": NodeTopicDataType.LAW,
            "LANGUAGE": NodeTopicDataType.LANGUAGE,
            "QUANTITY": NodeTopicDataType.QUANTITY,
            "PERCENT": NodeTopicDataType.PERCENT,
            "MONEY": NodeTopicDataType.MONEY,
            "TIME": NodeTopicDataType.TIME,
            "NORP": NodeTopicDataType.NATIONALITY,  # Nationalities, religious or political groups
            "FAC": NodeTopicDataType.ORGANIZATION,  # Buildings, airports, highways, bridges, etc.
            "CARDINAL": NodeTopicDataType.QUANTITY,
            #"ORDINAL": NodeTopicDataType.QUANTITY,
        }
        return mapping.get(ent_type, NodeTopicDataType.OTHER)