from math import log
k1 = 1.2
b = 0.75

def bm25(term_freq, doc_freq, doc_length, avg_doc_length, collection_size, contain_documents):
    N = collection_size
    K = k1 * ((1 - b) + b * (doc_length / avg_doc_length))
    inverse_doc_freq = log(((N - contain_documents + 0.5) / (contain_documents + 0.5)))
    return inverse_doc_freq * ((k1 + 1) * doc_freq) / (K + doc_freq)
