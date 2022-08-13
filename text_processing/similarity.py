"""
Program to find the similarity between texts and delete the common texts .
"""

# imports
import sys

sys.path.append("/workspaces/Event-Extraction")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from mongodb.config import db

# initialize mongodb
collection = db["kashmir_news"]

# Threshold for similarity
THRESHOLD = 0.5


def get_similarity(text1, text2):
    """
    Finds the similarity between two texts.

    Parameters:
    text1(str) - the first text
    text2(str) - the second text

    Returns:
    float - the similarity between the two texts
    """
    vectorizer = TfidfVectorizer(analyzer="word", stop_words="english")
    tfidf = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf[0], tfidf[1])[0][0]


if __name__ == "__main__":

    data = []
    similar_data = []

    # get data from mongodb
    for x in collection.find():
        data.append(x)

    # find similarity between all pairs of texts and delete the common texts
    for i in range(len(data)):
        for j in range(i + 1, len(data)):

            # finds similarity between two texts
            similarity = get_similarity(data[i]["description"], data[j]["description"])

            # checks if similarity is greater than threshold
            if similarity > THRESHOLD:
                similar_data.append(data[j])

                # delete the common text from mongodb
                collection.delete_one({"_id": data[j]["_id"]})
                break

    print(len(similar_data), " similar articles found and deleted")
