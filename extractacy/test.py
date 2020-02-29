import pytest
import spacy
from spacy.pipeline import EntityRuler
from extract import ValueExtractor


def build_docs():
    docs = list()
    docs.append(
        (
            "Discharge Date: November 15, 2008. Patient had temp reading of 102.6 f",
            [
                ("Discharge Date", "November 15, 2008"),
                ("November 15, 2008", None),
                ("temp", "102.6 f"),
                ("102.6", None),
            ],
        )
    )

    return docs

def test():
    nlp = spacy.load("en_core_web_sm")
    ruler = EntityRuler(nlp)
    patterns = [
        {"label": "TEMP_READING", "pattern": [{"LOWER": "temperature"}]},
        {"label": "TEMP_READING", "pattern": [{"LOWER": "temp"}]},
        {
            "label": "DISCHARGE_DATE",
            "pattern": [{"LOWER": "discharge"}, {"LOWER": "date"}],
        },
        
    ]
    ruler.add_patterns(patterns)

    ent_patterns = {
        "DISCHARGE_DATE": {"n_tokens": {"n": 1, "direction": "right"}},
        "TEMP_READING": {
            "pattern_match": {
                "patterns": [
                    [
                        {"LIKE_NUM": True},
                        {
                            "LOWER": {
                                "IN": ["f", "c", "farenheit", "celcius", "centigrade"]
                            }
                        },
                    ]
                ],
                "n": 7,
                "direction": "right"
            }
        },
    }
    nlp.add_pipe(ruler, last=True)
    valext = ValueExtractor(nlp, ent_patterns)
    nlp.add_pipe(valext, last=True)
    docs = build_docs()
    for d in docs:
        doc = nlp(d[0])
        for i, e in enumerate(doc.ents):
            print(e.text, e._.value_extract)
            assert (e.text, e._.value_extract) == d[1][i]


if __name__ == "__main__":
    test()
