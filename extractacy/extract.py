from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Token, Doc, Span


@Language.factory("valext")
class ValueExtractor:
    def __init__(self, nlp: Language, name: str, ent_patterns: dict):

        Span.set_extension("value_extract", default=[], force=True)
        self.nlp = nlp
        self.ent_patterns = ent_patterns

        self.matcher = Matcher(nlp.vocab)

        for key, value in self.ent_patterns.items():
            patterns = value["patterns"]
            self.matcher.add("_" + str(key), patterns)

    def __call__(self, doc):
        """Apply the pipeline component on a Doc object and Return
        the Doc, so it can be processed by the next component
        in the pipeline, if available.
        """
        matches = self.matcher(doc)
        for e in doc.ents:
            if e.label_ not in self.ent_patterns.keys():
                e._.value_extract = []
            else:
                e._.value_extract = self.get_pattern_match(
                    doc,
                    e,
                    matches,
                    self.ent_patterns[e.label_]["n"],
                    self.ent_patterns[e.label_]["direction"],
                )
        return doc

    def get_pattern_match(self, doc, entity, matches, n, direction):
        """
        gets first matched pattern within n tokens or
        in same sentence (if n == "sent")
        """
        if type(n) == int:
            if direction == "left":
                boundary_i = entity.start
                start_i = max(entity.start - n, 0)
            else:
                boundary_i = min(entity.end + (n - 1), len(doc))
                if direction == "right":
                    start_i = entity.end
                if direction == "both":
                    start_i = max(entity.start - n, 0)

        elif n == "sent":
            if direction == "right":
                start_i = entity.end
                boundary_i = entity.sent.end - 1
            if direction == "both":
                start_i = entity.sent.start
                boundary_i = entity.sent.end - 1
            if direction == "left":
                start_i = entity.sent.start
                boundary_i = entity.start

        else:
            raise ValueError(
                "If using pattern_match, expecting n to be an int or equal to 'sent'"
            )
        filtered_matches = [
            doc[start:end].text
            for match_id, start, end in matches
            if (self.nlp.vocab.strings[match_id] == "_" + entity.label_)
            and (start >= start_i)
            and (start <= boundary_i)
        ]
        return filtered_matches
