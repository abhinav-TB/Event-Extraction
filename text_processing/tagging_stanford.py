from stanza.server import CoreNLPClient

text = "A lot happened yesterday, and here's more from the district of Ernakulam in Kerala on January 20. Congress president Sonia Gandhi said Congress will launch a 'Bharat Jodo Yatra' from Kanyakumari to Kashmir on October 2."
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

    # print(sentence)

    for token in sentence.token:
        print(token)