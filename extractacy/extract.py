from spacy.matcher import Matcher
from spacy.tokens import Token, Doc, Span

#TODO: handle left direction

class ValueExtractor(object):
    def __init__(self, nlp, ent_patterns):

        Span.set_extension("value_extract", default=None, force=True)
        self.nlp = nlp
        self.ent_patterns = ent_patterns

        self.matcher = Matcher(nlp.vocab)

        for key, value in self.ent_patterns.items():
            if "pattern_match" in value:
                for pattern in value["pattern_match"]["patterns"]:
                    self.matcher.add("_"+str(key), None, pattern)

    def __call__(self, doc):
        """Apply the pipeline component on a Doc object and Return 
        the Doc, so it can be processed by the next component
        in the pipeline, if available.
        """
        matches = self.matcher(doc)
        for e in doc.ents:
            if e.end >= len(doc) or e.label_ not in self.ent_patterns.keys():
                e._.value_extract = None
            else:
                if "n_tokens" in self.ent_patterns[e.label_].keys():
                    e._.value_extract = self.get_n_tokens(
                        doc, e, self.ent_patterns[e.label_]["n_tokens"]["n"], 
                        self.ent_patterns[e.label_]["n_tokens"]["direction"]
                    )
                if "pattern_match" in self.ent_patterns[e.label_].keys():
                    e._.value_extract = self.get_pattern_match(
                        doc, e, matches, self.ent_patterns[e.label_]["pattern_match"]["n"],
                        self.ent_patterns[e.label_]["pattern_match"]["direction"]
                    )
        return doc

    def get_pattern_match(self, doc, entity, matches, n, direction):
        """
        gets first matched pattern within n tokens or
        in same sentence (if n == "sent")
        """
        if type(n) == int:
            boundary_idx = entity.end+(n-1)
        elif n == "sent":
            boundary_idx = entity.sent.end-1
        else:
            raise ValueError("If using pattern_match, expecting n to be an int or equal to 'sent'")
        first_match = next(
            (self.nlp.vocab.strings[match_id], start, end) 
            for match_id, start, end in matches 
            if (self.nlp.vocab.strings[match_id] == "_"+entity.label_) 
            and (start >= entity.end)
            and (start <= boundary_idx)
            )
        
        if first_match:
            return doc[first_match[1]:first_match[2]].text
        else:
            return None

    def get_n_tokens(self, doc, entity, n, direction):
        """
        gets first n tokens to the right or left. If token is
        part of named entity, the whole span is returned.
        If first token is punctuation or whitespace, moves to next.
        """
        if (doc[entity.end].is_punct == True) or (doc[entity.end].is_space == True):
            text = self.get_whole_entity(doc, entity.end + 1, n)
        else:
            text = self.get_whole_entity(doc, entity.end, n)

        return text

    def get_whole_entity(self, doc, token_idx, n):
        """Ensures that if a token is part of a named entity span, 
        the whole span is returned.
        Span tokens count towards n tokens, however will move past
        n tokens if a span continues past.
        """
        start = token_idx
        if doc[token_idx].ent_type_ != "":
            # continue to iterate if token is the beginning or inside ent
            # OR if haven't reached n tokens yet
            while (doc[token_idx].ent_iob_ in ["B", "I"]) or (token_idx - start) < n:
                token_idx += 1
            text = doc[start:token_idx].text
        else:
            text = doc[token_idx : token_idx + n].text

        return text
