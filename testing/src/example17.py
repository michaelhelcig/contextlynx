import spacy
from typing import List, Tuple


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


# Load spaCy model
nlp = spacy.load('en_core_web_lg')


def map_entity(ent_type: str) -> str:
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
        "ORDINAL": NodeTopicDataType.QUANTITY,
    }
    return mapping.get(ent_type, NodeTopicDataType.OTHER)


def get_named_entities(text: str) -> List[Tuple[str, str, int, int]]:
    """
    Extract named entities from the given text.

    Args:
        text (str): Input text to process.

    Returns:
        List[Tuple[str, str, int, int]]: List of tuples containing
        (entity_text, entity_type, start_index, end_index)
    """
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        mapped_type = map_entity(ent.label_)
        entities.append((ent.text, mapped_type, ent.start_char, ent.end_char))

    return entities


# Example usage
if __name__ == "__main__":
    sample_text = """
    Apple Inc. is planning to open a new store in Paris, France next month. 
    The company's CEO, Tim Cook, announced this during a press conference on May 15, 2023. 
    The store will be located near the Eiffel Tower and is expected to create about 200 new jobs. 
    Apple's stock price rose 2% following the announcement.
    """

    results = get_named_entities(sample_text)

    print("Named Entities:")
    for entity, entity_type, start, end in results:
        print(f"{entity} - {entity_type} ({start}, {end})")