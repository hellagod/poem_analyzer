import ast
import numpy as np
from tokenizing import create_vocabularies


def create_adj_matrix(poem):
    poem_vocab, lines_vocab = create_vocabularies(poem)
    p_size = len(lines_vocab)
    adj_matrix = np.zeros((p_size, p_size))
    for line_1 in range(p_size):
        vocab1 = lines_vocab[line_1]
        for line_2 in range(p_size):
            if line_1 != line_2:
                vocab2 = lines_vocab[line_2]
                similarity = compute_cosine_similarity(vocab1, vocab2, poem_vocab)
                adj_matrix[line_1, line_2] = similarity
    return adj_matrix


def compute_lines_degrees(adj_matrix):
    size = len(adj_matrix)
    edges = np.zeros(size, int)
    for i in range(size):
        for j in range(size):
            if i != j and adj_matrix[i, j] > 0:
                edges[i] += 1
    return list(edges)


def compute_cosine_similarity(vocab1, vocab2, poem_vocab):
    words1 = vocab1.keys()
    words2 = vocab2.keys()
    common_words = list(words1 & words2)
    if not common_words:
        return 0.
    numerator = 0.
    for i in range(len(common_words)):
        tf_line1 = vocab1.get(common_words[i])
        tf_line2 = vocab2.get(common_words[i])
        idf = poem_vocab.get(common_words[i]) - 0.85*tf_line1 - 0.85*tf_line2
        numerator += tf_line1 * tf_line2 * np.power(idf, 2)
    tf_sum1 = 0.
    tf_sum2 = 0.
    for w in words1:
        tf = vocab1.get(w)
        idf = poem_vocab.get(w) - tf
        tf_sum1 += tf * idf
    for w in words2:
        tf = vocab2.get(w)
        idf = poem_vocab.get(w) - tf
        tf_sum2 += tf * idf
    denominator = np.sqrt(tf_sum1)*np.sqrt(tf_sum2)
    return numerator if denominator == 0. else numerator/denominator


def generate_title(poem):
    poem = ast.literal_eval(poem)
    matrix = create_adj_matrix(poem)
    degrees = compute_lines_degrees(matrix)
    line_prob = sum([line for line in matrix]) * degrees
    indexed_prob = np.array([[i, lst] for i, lst in enumerate(line_prob)])
    sorted_ind = indexed_prob[:, 1].argsort()
    print("3 most_prob lines ", [poem[i] for i in sorted_ind[::3]])
    title_ind = sorted_ind[0] if sorted_ind[0] != 0 else sorted_ind[1]
    return poem[title_ind]
