import gensim
import nltk
from nltk.corpus import stopwords
from gensim import corpora

nltk.download('stopwords')

stop_words = set(stopwords.words('german'))

def analyze(documents):
    # Preprocess the documents (tokenization, removing stopwords, etc.)
    texts = [[word for word in document.lower().split() if word.lower() not in stop_words] for document in documents]
    
    # Create a dictionary representation of the documents
    dictionary = corpora.Dictionary(texts)

    # Convert documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Apply LDA
    lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=15)

    topics = []
    # Print the topics
    for idx, topic in lda_model.print_topics(-1):
        topics.append({idx: topic})
    
    return topics