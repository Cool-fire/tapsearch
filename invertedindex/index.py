import os
from collections import Counter, defaultdict
from string import punctuation
from invertedindex.database import getClient, getDB, insertDocuments, insertDoclengths, insertLexicon
import uuid

SEPARATORS = (',', ':')

def corpus():
    return input("Enter Corpus: ")


def load_stoplist(stoplistFile='stopwords.txt'):
    stoplistFile = os.getcwd()+'/'+stoplistFile
    with open(stoplistFile, 'r') as f:
        return {r.strip() for r in f}


def getDocuments(corpus):
    return corpus.split('\\n\\n')


def getRandomId():
    return str(uuid.uuid4())


def tokenize(document):
    tokens = document.lower().split()
    return tokens


def countFrequency(tokens, stoplist):
    term_counter = Counter()
    for token in tokens:
        token = token.strip(punctuation).strip()
        if stoplist and token in stoplist or not token:
            continue
        term_counter[token] += 1
    return term_counter


def parseDocument(document, stoplist):
    doc_id = getRandomId()
    term_freqs = Counter()
    tokens = tokenize(document)
    term_freqs += countFrequency(tokens, stoplist)
    return doc_id, term_freqs, sum(term_freqs.values())


def getMongoDb():
    client = getClient()
    db = getDB(client)
    return db


def avg_doc_length(doc_lengths):
    return int(sum(doc_lengths.values()) / len(doc_lengths))


def write(corpus_size, term_freq, doc_freq, doc_lengths, doc_list,
          doc_lengths_fn='doc_lengths', lexicon_fn='lexicon',
          posting_fn='posting'):
    doc_map = dict(average=avg_doc_length(doc_lengths),
                   documents=doc_lengths)

    db = getMongoDb()
    insertDocuments(db, dict(doc_list))
    insertDoclengths(db, doc_lengths)
    print(doc_freq, term_freq)
    insertLexicon(db, corpus_size, doc_freq, term_freq)


def indexCorpus(corpus, stoplistFile='stopwords.txt'):
    stoplist = load_stoplist(stoplistFile)
    in_collections_freq = Counter()
    postings = defaultdict(list)
    doc_list = defaultdict(list)
    doc_length = defaultdict(int)

    documents = getDocuments(corpus)
    corpus_size = len(documents)
    if len(documents) != 0:
        print('There are {} documents to index'.format(len(documents)))
        for document in documents:
            id, docfreqs, doclength = parseDocument(document, stoplist)
            doc_length[id] = doclength
            doc_list[id] = document
            in_collections_freq += docfreqs

            for word in docfreqs:
                postings[word].append([id, docfreqs[word]])

        write(corpus_size, in_collections_freq, postings, doc_length, doc_list)
        print("Finished writing")

    else:
        print("There are no documents in the corpus")


if __name__ == '__main__':
    corpus = corpus()
    stoplistFile = 'stopwords.txt'
    indexCorpus(corpus, stoplistFile)
