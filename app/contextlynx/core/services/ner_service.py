import spacy
from ..models import NodeTopicType
import re

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
        if existing_topics is None:
            existing_topics = list()

        doc = self.nlp(text)
        entities = []

        # Step 1: Collect all entities
        for ent in doc.ents:
            data_type = NERService._map_entity(ent.label_)

            text = self._get_without_start_the(text)

            if data_type in [NodeTopicType.PERSON, NodeTopicType.ORGANIZATION, NodeTopicType.LOCATION]:
                text = self._get_without_apostrophe(ent.text)
            elif data_type in [NodeTopicType.NATIONALITY]:
                text = self._get_titlecase(ent.text)
            else:
                text = self._get_lemma(ent)

            if data_type:  # Only add entities that have a valid mapped type
                entities.append({
                    'title': text,
                    'data_type': data_type,
                })

        # Step 2: Add existing topics to the entities list
        # We don't filter or change the existing topics; they are added as-is
        unique_entities = list(existing_topics)

        # Step 3: Filter out entities that are contained within others (from new entities only)
        filtered_entities = []
        for i, entity in enumerate(entities):
            is_contained = False
            for j, other in enumerate(entities):
                if i != j and other['data_type'] == entity['data_type'] and \
                        entity['title'].lower() in other['title'].lower() and \
                        entity['title'].lower() != other['title'].lower():
                    # If the entity is contained within another entity, skip it
                    is_contained = True
                    break

            if not is_contained:
                filtered_entities.append(entity)

        # Step 4: Remove duplicates based on title and data_type (checking only the newly discovered entities)
        seen = set((topic['title'].lower(), topic['data_type']) for topic in existing_topics)  # Existing topics as seen
        for entity in filtered_entities:
            key = (entity['title'].lower(), entity['data_type'])
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)

        # Step 5: Return the final list which combines existing topics and unique new entities
        return unique_entities

    @staticmethod
    def _get_titlecase(text):
        # return lower with first letter of word uppercase
        return ' '.join([token.capitalize() for token in text.split(' ')])

    @staticmethod
    def _get_lemma(ent):
        """Extract the lemmatized form of an entity"""
        return ' '.join([token.lemma_ for token in ent])
    
    @staticmethod
    def _get_without_start_the(text):
        return re.sub(r"^the ", "", text)

    @staticmethod
    def _get_without_apostrophe(text):
        # Regex pattern to match variations of 's with different types of apostrophes
        return re.sub(r"(\w+)[’'s]$", r"\1", text)

    @staticmethod
    def _map_entity(ent_type):
        """Map spaCy entity types to NodeTopicDataType"""
        mapping = {
            "PERSON": NodeTopicType.PERSON,
            "GPE": NodeTopicType.LOCATION,
            "LOC": NodeTopicType.LOCATION,
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
            "DATE": NodeTopicType.DATE,
            "ORG": NodeTopicType.ORGANIZATION,
            "CARDINAL": NodeTopicType.QUANTITY,
            "ORDINAL": NodeTopicType.QUANTITY,
            "PERCENT": None,
            "MONEY": None,
        }

        if ent_type in ignored_categories:
            return None  # Skip entities in ignored categories

        return mapping.get(ent_type, NodeTopicType.OTHER)
