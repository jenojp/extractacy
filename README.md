# extractacy

[![Built with spaCy](https://img.shields.io/badge/made%20with%20❤%20and-spaCy-09a3d5.svg)](https://spacy.io) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

spaCy pipeline object for extracting values that correspond to a named entity (e.g., birth dates, account numbers, or laboratory results)

## Installation and usage
Install the library.
```bash
pip install extractacy
```

Import library and spaCy.
```python
import spacy
from extractacy.extract import ValueExtractor
```

Load spacy language model. Set up an EntityRuler for the example. Define the entites and value extraction patterns and add to nlp pipeline.

```python
nlp = spacy.load("en_core_web_sm")
# Set up entity ruler
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
nlp.add_pipe(ruler, last=True)

# Define ent_patterns for value extraction
ent_patterns = {
    "DISCHARGE_DATE": {"n_tokens": {"n": 1, "direction":"right"}},
    "TEMP_READING": {"pattern_match": {"patterns": [
                [{"LIKE_NUM": True},{"LOWER": {"IN": ["degrees", "farenheit", "celcius", "centigrade"]}}]],
                "n": 3, "direction": "right"
        }
    },
}

valext = ValueExtractor(nlp, ent_patterns)
nlp.add_pipe(valext, last=True)

doc = nlp("Discharge Date: November 15, 2008. Patient had temp reading of 102.6 degrees.")
for e in doc.ents:
    if e._.value_extract:
        print(e.text, e.label_, e._.value_extract)
## Discharge Date DISCHARGE_DATE November 15, 2008
## temp reading TEMP_READING 102.6 degrees
```

### Value Extraction patterns
There are two options for extracting values: n tokens and first found pattern.

#### N Tokens
This method will return n tokens past an entity of interest. 

**Note:**
* if the immediate next token is whitespace or punctuation, it will be skipped.
* if the span of n tokens is part of an entity, the entire entity will be returned, even if it is past n tokens
```python
{"ENTITY_NAME": {"n_tokens": {"n": 1, "direction": "right"}}}
```

#### Pattern Match
This method will return the first found pattern past an entity of interest within n tokens or within the same sentence. It relies on [spaCy token matching syntax](https://spacy.io/usage/rule-based-matching#matcher).

```python
{"ENTITY_NAME": {"pattern_match": {"patterns":[{"LOWER":"awesome"}, {"LOWER":"pattern"}], "n": 5, "direction": "right"}}}
```
Use `"n":"sent"` for within sentence method rather than n tokens.


## Contributing
[contributing](https://github.com/jenojp/negspacy/blob/master/CONTRIBUTING.md)

## Authors
* Jeno Pizarro

## License
[license](https://github.com/jenojp/extractacy/blob/master/LICENSE)