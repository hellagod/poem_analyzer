import ast

import numpy as np
import re
import string
from pymorphy2 import MorphAnalyzer


def create_adj_matrix(poem):
    lines_vocab, poem_vocab = create_vocabularies(poem)
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
    size = len(sorted_ind)
    title_ind = sorted_ind[size-1] if sorted_ind[0] != 0 else sorted_ind[size-2]
    return poem[title_ind]


def generate_title_with_probabilities(poem):
    poem = make_one_line(poem)
    words = list(map(lambda x: x.lower(), get_line_words(poem)))
    ngramms = split_to_ngramms(words, 2)
    matrix = create_adj_matrix(ngramms)
    degrees = compute_lines_degrees(matrix)
    line_sum = sum([line for line in matrix])
    print("l_sum ", line_sum)
    line_prob = []
    for i, line in enumerate(line_sum):
        el = line if degrees[i] == 0 else line/(2*degrees[i])
        if el > 0:
            line_prob.append(el)
    indexed_prob = np.array([[i, lst] for i, lst in enumerate(line_prob)])
    print("ind_pr ", indexed_prob)
    sorted_ind = indexed_prob[:, 1].argsort()
    lines_with_prob = []
    size = len(sorted_ind)
    start_ind = size - 6 if size > 6 else 0
    for i in range(start_ind, size):
        ind = sorted_ind[i]
        lines_with_prob.append([ngramms[ind], indexed_prob[ind, 1]])
    return lines_with_prob


morph = MorphAnalyzer()


def create_vocabularies(poem):
    poem_vocab = {}
    lines_vocab = []
    closest_nouns = {'femn': '', 'masc': '', 'neut': ''}
    for i in range(len(poem)):
        line = get_line_words(poem[i])
        if len(line) != 0:
            line_vocab = {}
            for word in line:
                parsed = morph.parse(word)[0]
                lemma = parsed.normal_form
                pos = str(parsed.tag)
                poem_vocab = change_poem_vocab(poem_vocab, lemma, pos, closest_nouns)
                line_vocab = change_line_vocab(line_vocab, lemma, pos, closest_nouns)
            lines_vocab.append(line_vocab)
    return lines_vocab, poem_vocab


def get_line_words(line):
    word = ""
    words = []
    for i, char in enumerate(line):
        if char in " -" and word != "":
            words.append(word)
            word = ""
        elif (char in " -\n" and word == "") or (char in "«»…"):
            continue
        elif char not in string.punctuation:
            word += char
    return words


def change_line_vocab(line_vocab, lemma, pos, closest_nouns):
    if lemma in line_vocab:
        line_vocab[lemma] += 1
    else:
        changed = False
        if re.match(r'NPRO(.*),3per(.*)sing', pos):
            lemma, changed = update_noun_count(closest_nouns, pos, lemma)
        if not changed and not (re.match(r'(PRCL|PREP|CONJ|PNCT)', pos)):
            line_vocab[lemma] = 1

        if changed:
            if lemma in line_vocab:
                line_vocab[lemma] += 1
    return line_vocab


def change_poem_vocab(poem_vocab, lemma, pos, closest_nouns):
    if lemma in poem_vocab:
        poem_vocab[lemma] += 1
    else:
        changed = False
        if re.match(r'NOUN', pos):
            closest_nouns = change_closest_noun(closest_nouns, pos, lemma)
        elif re.match(r'NPRO(.*),3per(.*)sing', pos):
            lemma, changed = update_noun_count(closest_nouns, pos, lemma)

        if not changed and not (re.match(r'PRCL|PREP|CONJ|PNCT', pos)):
            poem_vocab[lemma] = 1
        elif changed and lemma in poem_vocab:
            poem_vocab[lemma] += 1
    return poem_vocab


def change_closest_noun(closest_nouns, analysis, lemma):
    for gender in closest_nouns.keys():
        if re.search(gender, analysis):
            closest_nouns[gender] = lemma
    return closest_nouns


def update_noun_count(closest_nouns, analysis, lemma):
    for gender in closest_nouns.keys():
        if re.search(gender, analysis):
            if closest_nouns.get(gender) == '':
                return lemma, False
            else:
                return closest_nouns.get(gender), True


def split_to_ngramms(words, n):
    forbidden = re.compile(r"PRCL|PREP|CONJ|PNCT")
    filtered = [w for w in words if not re.search(forbidden, str(morph.parse(w)[0].tag))]
    if n == 1:
        return filtered
    if n > 1:
        ngrams = zip(*[filtered[i:] for i in range(n)])
        ngrams = [' '.join(ngram) for ngram in ngrams]
        return ngrams


def get_one_line_words(line):
    word = ""
    for char in line:
        if not(char in string.punctuation) and not(char in "-«»…"):
            word += char.lower()
    words = re.split(r' ', word)
    return words


def make_one_line(poem):
    res = re.split(r'\n', poem)
    result = ""
    for i, r in enumerate(res):
        if len(r) == 0:
            continue
        elif i != len(res) - 1:
            result += (r + ' ')
        else:
            result += r
    return result
