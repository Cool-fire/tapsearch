from pymongo import MongoClient


def getClient(url='localhost', port=27017):
    try:
        url = "mongodb+srv://upendra:upendra2@cluster0-ym4ge.mongodb.net/test?retryWrites=true&w=majority"
        client = MongoClient(url)
        return client
    except:
        print("Error Connecting to database")


def getDB(client, database='tapchief'):
    db = client[database]
    return db


def insertDocuments(db, docs):
    doc_collection = db['documents']
    for doc in docs:
        doc_collection.insert_one({'id': doc, 'text': docs[doc]})
    print("inserted documents into database")


def insertDoclengths(db, doclength):
    doclength_collection = db['doclength']
    for doc in doclength:
        doclength_collection.insert_one({'id': doc, 'doclength': doclength[doc]})
    print("inserted doc lengths")


def deleteDatabase():
    db = getDB(getClient())
    try:
        db.documents.remove()
        db.doclength.remove()
        db.lexicon.remove()
        return True
    except:
        print("Error occured while Deleting")
        return False


def insertLexicon(db, corpus_size, doc_freq, term_freq):
    lexicon_collection = db['lexicon']

    for term, idf in doc_freq.items():
        posting_list = []
        prev_doc = lexicon_collection.find_one({'term': term})
        prev_idf = 0
        prev_postings = []
        if prev_doc:
            prev_idf = prev_doc['idf']
            prev_postings = prev_doc['posting']

        for pos_term in idf:
            id, doc_freq = pos_term
            posting_list.append({'id': id, 'docfreq': doc_freq})
        prev_postings.extend(posting_list)
        lexicon_collection.replace_one({'term': term},
                                       {'term': term, 'idf': prev_idf + term_freq[term], 'posting': prev_postings},
                                       upsert=True)
    print("inserted lexicon")


if __name__ == "__main__":
    client = getClient()
    db = getDB(client, 'tapchief')
