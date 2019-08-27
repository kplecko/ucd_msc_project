from __init__ import app_config
import json
import requests
import logging
import traceback
import spacy
from spacy import displacy


def get_entity(text, entity_type, entity_max_count):
    """
    Google NLP API for computing text entitys
    :param text: Input plain text
    :param entity_type: list(), return entity type (https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity#Type)
    e.g. ['LOCATION', 'ORGANIZATION']
    :param entity_max_count: maximum entities want to receive
    :return:
    """
    """
    Google NLP API for computing text entitys
    parm: text: Input plain text
    :return json object with entitys and additional info
    """
    entity_input = {
        "document": {
            "type": "PLAIN_TEXT",
            # 'language': 'en',
            "content": text,
        },
        "encodingType": "UTF8",
    }
    querystring = {"key": app_config["google_sentiment_key"]}
    # Convert dict to string
    payload = json.dumps(entity_input)
    headers = {"Content-Type": "application/json", "Accept": "*/*", "Host": "language.googleapis.com"}
    # List for entities
    entities = list()
    try:
        response = requests.request("POST", app_config["google_entity_url"], data=payload, headers=headers,
                                    params=querystring)
    except Exception as error:
        logging.error(f"Error while calling Google entity extraction: {error}")
        logging.error(traceback.format_exc())
        return entities

    api_rt = json.loads(response.text)
    entity = sorted(api_rt["entities"], key=lambda x: x["salience"], reverse=True)

    # entity count for restricting the return number of entities
    entity_count = 0

    for each_entity in entity:
        if entity_count == entity_max_count:
            break
        elif each_entity["type"] in entity_type and each_entity["metadata"]:
            video_entity = {"entity": each_entity["name"], "type": each_entity["type"],
                            "salience": each_entity["salience"],
                            "wikipedia_url": each_entity["metadata"]["wikipedia_url"]}
            entities.append(video_entity)
            entity_count += 1
    return entities


def get_entity_spacy(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    entities = list()
    for each_entity in doc.ents:
        entities.append({
            'entity': each_entity.text,
            'type': each_entity.label_
        })
    displacy.serve(doc, style="ent")
    return entities


if __name__ == "__main__":
    text = 'This is my python video'
    print(get_entity_spacy(text))
