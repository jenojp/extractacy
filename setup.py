from setuptools import setup, find_packages
import io

setup(
    name = 'extractacy',
    version = 'v0.1.2',
    url = 'https://github.com/jenojp/extractacy',
    author = 'Jeno Pizarro',
    author_email = 'jenopizzaro@gmail.com',
    description = 'A SpaCy pipeline object for extracting values that correspond to a named entity (e.g., birth dates, account numbers, or laboratory results)',
    long_description=io.open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    keywords = ["nlp, spacy, SpaCy, NER, entity extraction, value extraction"],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    license="MIT",
    install_requires=[
        "spacy>=2.1.8",
        ],
    tests_require=[
        "pytest",
        ],
    python_requires='>=3.6.0',
)