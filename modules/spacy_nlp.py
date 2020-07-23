import spacy

nlp = spacy.load("en_core_web_sm")


def get_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append(ent.text)
    return entities


if __name__ == "__main__":
    text = "Reliance Jio launches video conferencing app JioMeet to take on Zoom App"
    print(get_entities(text))
