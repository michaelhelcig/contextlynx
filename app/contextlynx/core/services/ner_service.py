import spacy
from ..models import NodeTopicType


class NERService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NERService, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.model = 'en_core_web_lg'
        self.nlp = spacy.load(self.model)

    def get_named_entities(self, text, existing_topics=None):
        doc = self.nlp(text)
        entities = []

        # Step 1: Collect all entities
        for ent in doc.ents:
            data_type = NERService._map_entity(ent.label_)
            text = ent.text
            if data_type:  # Only add entities that are not in the ignored categories
                entities.append({
                    'title': text,
                    'data_type': data_type,
                })

        # Step 2: Add existing topics to the entities list
        if existing_topics:
            entities.extend(existing_topics)

        # Step 3: Filter out entities that are contained within others
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

        # Step 4: Remove duplicates based on title and data_type
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
            "PERSON": NodeTopicType.PERSON,
            "ORG": NodeTopicType.ORGANIZATION,
            "GPE": NodeTopicType.LOCATION,
            "LOC": NodeTopicType.LOCATION,
            "DATE": NodeTopicType.DATE,
            "EVENT": NodeTopicType.EVENT,
            "PRODUCT": NodeTopicType.PRODUCT,
            "WORK_OF_ART": NodeTopicType.WORK_OF_ART,
            "LAW": NodeTopicType.LAW,
            "LANGUAGE": NodeTopicType.LANGUAGE,
            "QUANTITY": NodeTopicType.QUANTITY,
            "TIME": NodeTopicType.TIME,
            "NORP": NodeTopicType.NATIONALITY,  # Nationalities, religious or political groups
            "FAC": NodeTopicType.ORGANIZATION,  # Buildings, airports, highways, bridges, etc.
        }

        ignored_categories = {
            "CARDINAL": NodeTopicType.QUANTITY,
            "ORDINAL": NodeTopicType.QUANTITY,
            "PERCENT": None,
            "MONEY": None,
        }

        if ent_type in ignored_categories:
            return None  # Skip entities in ignored categories

        return mapping.get(ent_type, NodeTopicType.OTHER)
