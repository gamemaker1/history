"""The knowledge-graph schema: entity types, predicates, and the JSON schema for extracted claims.

A claim is one sourced statement: subject PREDICATE object, optionally with
the resource involved (what is sold, lent, charged for or carried), a
quantity, months, a place where it holds and a time, and always with the
verbatim quote and PDF page that support it. Claims are the edges of the
graph. Entities (data/entities.csv) are the nodes.

extract_claims.py, verify_claims.py and build_graph.py all import this file,
so the vocabulary is defined once.
"""

ENTITY_TYPES = {
    "place": "A village, pasture (dhar, jot), pass, winter grazing ground, town, market or region.",
    "river": "A river or stream.",
    "group": "A caste, tribe or community (Gaddi, Brahman, Rajput, Sipi, Kanet, Koli, Lohar, Gujjar ...).",
    "person": "A named individual or household (a lambardar, a moneylender, a shepherd interviewed by the survey ...).",
    "role": "An occupational role (pohal, fawal, grazier, road labourer, moneylender, shopkeeper, fee contractor ...).",
    "authority": "A ruler, state body or office (Raja of Chamba, Bushahr ruler, Forest Department, panchayat ...).",
    "resource": "Animals, goods, rights or documents (sheep, goats, wool, salt, grain, ghee, permit, grazing right ...).",
    "event": "A dated change (merger of 1948, Scheduled Tribe listing, sheep disease, India-China dispute ...).",
}

# Predicate -> (family, meaning, subject types, object types).
# Families group predicates for the graph views: the Annales views use
# movement and geography, the Marxist views use property, extraction and labour.
PREDICATES = {
    # movement and season
    "GRAZES_AT": ("movement", "flocks of the subject graze at the object place in the given months",
                  ["group", "person", "place", "role"], ["place"]),
    "MIGRATES_TO": ("movement", "people of the subject go to the object place for a season (with or without flocks)",
                    ["group", "person", "place", "role"], ["place"]),
    "MOVES_VIA": ("movement", "the subject's route passes through the object (a pass, road or valley)",
                  ["group", "person", "place", "role"], ["place"]),
    # geography
    "LOCATED_ON": ("geography", "the subject place lies on or near the object river",
                   ["place"], ["river"]),
    "LOCATED_IN": ("geography", "the subject place lies in the object region",
                   ["place"], ["place"]),
    # property
    "OWNS": ("property", "the subject owns the object (animals, land, rights); qty and unit give the number",
             ["group", "person", "place", "role", "authority"], ["resource"]),
    "HAS_POPULATION": ("property", "the subject (a village or group in it) numbers qty households or persons",
                       ["place", "group", "person"], ["resource"]),
    "HOLDS_RIGHTS_OVER": ("property", "the subject holds ownership or control of the object pasture, forest or right",
                          ["authority", "group", "person", "place", "role"], ["place", "resource"]),
    "CLOSES": ("property", "the subject closes, fences or restricts the object pasture or forest",
               ["authority"], ["place", "resource"]),
    # extraction: who takes a share of whose product
    "COLLECTS_FEE_FROM": ("extraction", "the subject collects grazing fees or tax from the object; qty and unit give the rate",
                          ["authority", "role", "group", "person"], ["group", "person", "role", "place"]),
    "AUCTIONS_RIGHT_TO": ("extraction", "the subject sells or auctions a right (for example fee collection) to the object",
                          ["authority"], ["group", "person", "role"]),
    "ISSUES_PERMIT_TO": ("extraction", "the subject issues grazing permits to the object, possibly limiting numbers",
                         ["authority"], ["group", "person", "role", "place"]),
    "PAYS_DUES_TO": ("extraction", "the subject pays revenue, dues or begar to the object",
                     ["group", "person", "place", "role"], ["authority", "role"]),
    "LENDS_TO": ("extraction", "the subject lends money or grain to the object; qty and unit give interest or amount",
                 ["role", "group", "person", "authority"], ["group", "person", "place", "role"]),
    "SELLS_TO": ("exchange", "the subject sells goods to the object; terms go in the note",
                 ["group", "person", "place", "role"], ["group", "person", "role", "place"]),
    "BUYS_FROM": ("exchange", "the subject buys goods or animals from the object",
                  ["group", "person", "place", "role"], ["group", "person", "role", "place"]),
    "TRADES_AT": ("exchange", "the subject trades at the object fair or market",
                  ["group", "person", "place", "role"], ["place"]),
    "CARRIES": ("exchange", "the subject's flocks or people carry the object goods",
                ["group", "person", "place", "role"], ["resource"]),
    # labour
    "HIRES": ("labour", "the subject hires the object (shepherds, graziers, labourers); qty and unit give the wage",
              ["group", "person", "place", "role", "authority"], ["role", "group", "person"]),
    "WORKS_AS": ("labour", "people of the subject work as the object role; qty and unit give the wage",
                 ["group", "person", "place"], ["role"]),
    # events
    "AFFECTED_BY": ("event", "the subject was affected by the object event",
                    ["group", "person", "place", "resource", "authority"], ["event"]),
    # voice
    "SAYS": ("voice", "a person of the subject says the quoted words (direct speech in the survey)",
             ["group", "person", "role", "place"], ["resource"]),
}

# When a claim holds. The conjuncture is assigned later by build_graph.py from
# this value, the date text and the predicate, so the rule is visible in code.
WHEN = {
    "recurring": "every year, part of the seasonal cycle",
    "at_survey": "the state of things when the survey was made (about 1961)",
    "before_1948": "under princely or colonial rule, before the 1948 merger",
    "after_1948": "after the merger, before or at the survey",
    "unspecified": "the text does not say",
}

MONTHS = list(range(1, 13))

CLAIM_FIELDS = ["subject", "subject_type", "predicate", "object", "object_type", "resource",
                "qty", "unit", "months", "place", "when", "date_text", "quote", "note"]

# JSON schema for structured output from the extraction model.
_nullable = lambda t: {"anyOf": [{"type": t}, {"type": "null"}]}
CLAIM_SCHEMA = {
    "type": "object",
    "properties": {
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "subject_type": {"type": "string", "enum": list(ENTITY_TYPES)},
                    "predicate": {"type": "string", "enum": list(PREDICATES)},
                    "object": {"type": "string"},
                    "object_type": {"type": "string", "enum": list(ENTITY_TYPES)},
                    "resource": _nullable("string"),
                    "qty": _nullable("number"),
                    "unit": _nullable("string"),
                    "months": {"type": "array", "items": {"type": "integer", "enum": MONTHS}},
                    "place": _nullable("string"),
                    "when": {"type": "string", "enum": list(WHEN)},
                    "date_text": _nullable("string"),
                    "quote": {"type": "string"},
                    "note": _nullable("string"),
                },
                "required": CLAIM_FIELDS,
                "additionalProperties": False,
            },
        }
    },
    "required": ["claims"],
    "additionalProperties": False,
}


def predicate_table():
    """The predicate vocabulary as text, for prompts and documentation."""
    lines = []
    for name, (family, meaning, subj, obj) in PREDICATES.items():
        lines.append(f"- {name} [{family}]: {meaning}. Subject: {'/'.join(subj)}. Object: {'/'.join(obj)}.")
    return "\n".join(lines)
