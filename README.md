
<p align="center"><img width="40%" src="docs/icon.png" /></p>

# extractacy - pattern extraction and named entity linking for spaCy
[![Build Status](https://dev.azure.com/jenopizzaro/extractacy/_apis/build/status/jenojp.extractacy?branchName=master)](https://dev.azure.com/jenopizzaro/extractacy/_build/latest?definitionId=3&branchName=master) [![Built with spaCy](https://img.shields.io/badge/made%20with%20❤%20and-spaCy-09a3d5.svg)](https://spacy.io) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black) ![pypi Version](https://img.shields.io/pypi/v/extractacy.svg?style=flat-square) [![DOI](https://zenodo.org/badge/244012020.svg)](https://zenodo.org/badge/latestdoi/244012020)

spaCy pipeline object for extracting values that correspond to a named entity (e.g., birth dates, account numbers, or laboratory results)

## Installation and usage
Install the library.
```bash
pip install extractacy
```

Import library and spaCy.
```python
import spacy
from spacy.pipeline import EntityRuler
from extractacy.extract import ValueExtractor
```

Load spacy language model. Set up an EntityRuler for the example. 

```python
nlp = spacy.load("en_core_web_sm")
# Set up entity ruler
ruler = nlp.add_pipe("entity_ruler")
patterns = [
    {"label": "TEMP_READING", "pattern": [{"LOWER": "temperature"}]},
    {"label": "TEMP_READING", "pattern": [{"LOWER": "temp"}]},
    {
        "label": "DISCHARGE_DATE",
        "pattern": [{"LOWER": "discharge"}, {"LOWER": "date"}],
    },
    
]
ruler.add_patterns(patterns)
```

Define which entities you would like to link patterns to. Each entity needs 3 things:
1) patterns to search for (list). This relies on [spaCy token matching syntax](https://spacy.io/usage/rule-based-matching#matcher).
2) n_tokens to search around a named entity (`int` or `sent`)
3) direction (`right`, `left`, `both`)

```python
# Define ent_patterns for value extraction
ent_patterns = {
    "DISCHARGE_DATE": {"patterns": [[{"SHAPE": "dd/dd/dddd"}],[{"SHAPE": "dd/d/dddd"}]],"n": 2, "direction": "right"},
    "TEMP_READING": {"patterns": [[
                        {"LIKE_NUM": True},
                        {"LOWER": {"IN": ["f", "c", "farenheit", "celcius", "centigrade", "degrees"]}
                        },
                    ]
                ],
                "n": "sent",
                "direction": "both"
        },
}
```

Add ValueExtractor to spaCy processing pipeline

```python
nlp.add_pipe("valext", config={"ent_patterns":ent_patterns}, last=True)

doc = nlp("Discharge Date: 11/15/2008. Patient had temp reading of 102.6 degrees.")
for e in doc.ents:
    if e._.value_extract:
        print(e.text, e.label_, e._.value_extract)
        
## Discharge Date DISCHARGE_DATE 11/15/2008
## temp reading TEMP_READING 102.6 degrees
```

## Contributing
[contributing](https://github.com/jenojp/negspacy/blob/master/CONTRIBUTING.md)

## Authors
* Jeno Pizarro

## License
[license](https://github.com/jenojp/extractacy/blob/master/LICENSE)
