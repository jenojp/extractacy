from spacy.matcher import Matcher
from spacy.tokens import Token, Doc, Span

#TODO: error handling for out of bounds token indexes (start and end of doc)

class ValueExtractor(object):
    def __init__(self, nlp, ent_patterns):

        Span.set_extension("value_extract", default=[], force=True)
        self.nlp = nlp
        self.ent_patterns = ent_patterns

        self.matcher = Matcher(nlp.vocab)

        for key, value in self.ent_patterns.items():
            patterns = value["patterns"]
            self.matcher.add("_"+str(key), patterns)

    def __call__(self, doc):
        """Apply the pipeline component on a Doc object and Return 
        the Doc, so it can be processed by the next component
        in the pipeline, if available.
        """
        matches = self.matcher(doc)
        for e in doc.ents:
            if e.end >= len(doc) or e.label_ not in self.ent_patterns.keys():
                e._.value_extract = []
            else:
                # if "n_tokens" in self.ent_patterns[e.label_].keys():
                #     e._.value_extract = self.get_n_tokens(
                #         doc, e, self.ent_patterns[e.label_]["n_tokens"]["n"], 
                #         self.ent_patterns[e.label_]["n_tokens"]["direction"]
                #       )
                # if "pattern_match" in self.ent_patterns[e.label_].keys():
                e._.value_extract = self.get_pattern_match(
                    doc, e, matches, self.ent_patterns[e.label_]["n"],
                    self.ent_patterns[e.label_]["direction"]
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
                start_i = max(entity.start-n, 0)
            else:
                boundary_i = min(entity.end+(n-1), len(doc))
                if direction == "right":
                    start_i = entity.end
                if direction == "both":
                    start_i = max(entity.start-n, 0)

        elif n == "sent":
            if direction == "right":
                start_i = entity.end
                boundary_i = entity.sent.end-1
            if direction == "both":
                start_i = entity.sent.start
                boundary_i = entity.sent.end-1
            if direction == "left":
                start_i = entity.sent.start
                boundary_i = entity.start

        else:
            raise ValueError("If using pattern_match, expecting n to be an int or equal to 'sent'")
        for match_id, start, end in matches:
        filtered_matches = [
            doc[start:end].text
            for match_id, start, end in matches 
            if (self.nlp.vocab.strings[match_id] == "_"+entity.label_) 
            and (start >= start_i)
            and (start <= boundary_i)
        ]
        return filtered_matches         
        # if first_match:
        #     return doc[first_match[1]:first_match[2]].text
        # else:
        #     return None

    # def get_n_tokens(self, doc, entity, n, direction):
    #     """
    #     gets first n tokens to the right or left. If token is
    #     part of named entity, the whole span is returned.
    #     If first token is punctuation or whitespace, moves to next.
    #     """
    #     print(entity.text, direction, entity.start, entity.end, len(doc))
    #     if direction == "right":
    #         if (entity.end+1 >= len(doc)):
    #             return None
    #         if (doc[entity.end].is_punct == True) or (doc[entity.end].is_space == True):
    #             text = self.get_whole_entity(doc, entity.end + 1, n, "right")
    #         else:
    #             text = self.get_whole_entity(doc, entity.end, n, "right")

    #     if direction == "left":
    #         if entity.start == 0:
    #             return None
    #         if (doc[entity.start - 1].is_punct == True) or (doc[entity.start - 1].is_space == True):
    #             text = self.get_whole_entity(doc, entity.start - 2, n, "left")
    #         else:
    #             text = self.get_whole_entity(doc, entity.start - 1, n, "left")

    #     return text

    # def get_whole_entity(self, doc, token_i, n, direction):
    #     """Ensures that if a token is part of a named entity span, 
    #     the whole span is returned.
    #     Span tokens count towards n tokens, however will move past
    #     n tokens if a span continues past.
    #     """
    #     start = token_i

    #     if direction == "right":
    #         if doc[token_i].ent_type_ != "":
    #             # continue to iterate if token is the beginning or inside ent
    #             # OR if haven't reached n tokens yet
    #             while ((doc[token_i].ent_iob_ in ["B", "I"]) or ((token_i - start) < n)) and (token_i < (len(doc)-1)):
    #                 token_i += 1
    #             text = doc[start:token_i].text
    #         else:
    #             text = doc[start : token_i + n].text

    #         return text

    #     if direction == "left":
    #         if doc[token_i].ent_type_ != "":
    #             # continue to iterate if token is the beginning or inside ent
    #             # OR if haven't reached n tokens yet
    #             while ((doc[token_i].ent_iob_ in ["I"]) or ((start - token_i) < n)) and (token_i > 0):
    #                 token_i -= 1
    #             text = doc[token_i:start+1].text
    #         else:
    #             text = doc[token_i - n : start+1].text

    #         return text