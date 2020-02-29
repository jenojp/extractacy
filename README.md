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

Load spacy language model.
```python
nlp = spacy.load("en_core_web_sm")
```

## Contributing
[contributing](https://github.com/jenojp/negspacy/blob/master/CONTRIBUTING.md)

## Authors
* Jeno Pizarro

## License
[license](https://github.com/jenojp/extractacy/blob/master/LICENSE)