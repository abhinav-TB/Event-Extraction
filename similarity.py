from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from mongodb import db

collection = db["kashmir_news"]

THRESHOLD = 0.5

def get_similarity(text1, text2):
    vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf[0], tfidf[1])[0][0]


if __name__ == '__main__':
    
    data = []
    similar_data = []
    for x in collection.find():
        data.append(x)
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            similarity = get_similarity(data[i]['description'], data[j]['description'])
            if similarity > THRESHOLD:
                similar_data.append(data[i])
            
    print(len(similar_data))
