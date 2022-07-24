from stanza.server import CoreNLPClient

text = "Two people were killed in a car crash in Kashmir."
with CoreNLPClient(
    annotators=[
        "tokenize",
        "ssplit",
        "pos",
        "lemma",
        "ner",
        "parse",
        "depparse",
        "coref",
    ],
    timeout=30000,
    memory="6G",
) as client:
    ann = client.annotate(text)

    # get the first sentence
    sentence = ann.sentence[0]

    for token in sentence.token:
        print(token.word, token.lemma, token.pos, token.ner)