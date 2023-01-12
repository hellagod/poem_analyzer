import re
import string
from pymorphy2 import MorphAnalyzer

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
