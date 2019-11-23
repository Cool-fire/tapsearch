import json

from collections import defaultdict, OrderedDict
from invertedindex.database import getClient, getDB
from invertedindex.index import load_stoplist
from invertedindex.rank import bm25


def getMongoDb():
    client = getClient()
    return getDB(client)


def loadlexicon(db):
    lexicon_collection = db.lexicon
    return lexicon_collection


def load_doc_lengths(db):
    doclengths = db.doclength
    avg = 0
    totalLength = 0
    total = 0
    for doc in doclengths.find():
        totalLength += doc['doclength']
        total += 1
    avg = totalLength / total
    return avg, total


def getTermDetails(db, term):
    lexicon_collection = db.lexicon
    termDetails = lexicon_collection.find_one({'term': term})
    if not termDetails: return None, None
    return termDetails['idf'], termDetails['posting']


def getDocumentLength(db, doc_id):
    doc_length_collection = db.doclength
    doclengthDetails = doc_length_collection.find_one({'id': doc_id})
    return doclengthDetails['doclength']


def processQuery(term):
    if term in load_stoplist():
        print("The term is a stoplist word")
        return None
    db = getMongoDb()
    doc_scores = defaultdict(float)
    stoplist = load_stoplist()
    avg_doc_length, collection_size = load_doc_lengths(db)
    term_freq, documents = getTermDetails(db, term)
    containing_documents = 0 if not documents else len(documents)
    if not documents: return []
    for document in documents:
        doc_id = document['id']
        doc_freq = document['docfreq']
        doc_length = getDocumentLength(db, doc_id)
        score = bm25(int(term_freq), int(doc_freq), doc_length, avg_doc_length, collection_size, containing_documents)
        doc_scores[doc_id] = score

    doc_scores = OrderedDict(sorted(doc_scores.items(), key=lambda x: x[1], reverse=True))
    return doc_scores


def getDocumentText(doc_id):
    db = getMongoDb()
    document_collection = db.documents
    doctext = document_collection.find_one({'id': doc_id})
    return doctext['text']


if __name__ == '__main__':
    query = input()
    docscores = processQuery(query)
    print(docscores)
