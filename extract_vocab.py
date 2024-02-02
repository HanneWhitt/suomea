import re
import json


with open('finnish_english.txt', 'r') as f:
    booklines = f.read().splitlines()


vocab = {}

word_counter = 0
section = "None"
topic = "None"
group_no = 0
group = "None"
empty_line_count = 0


sections = [
    "BASIC CONCEPTS",
    "HUMAN BEING",
    "HUMAN HABITAT",
    "HUMAN HABITAT",
    "HUMAN ACTIVITIES",
    "TECHNICAL EQUIPMENT. TRANSPORTATION",
    "PEOPLE. LIFE EVENTS",
    "NATURE",
    "REGIONAL GEOGRAPHY",
    "MISCELLANEOUS",
    "MAIN 500 VERBS"
]

def is_section(l):
    return l in sections


def is_topic(l):
    "Line can be section and topic. Deals with sections without constituent topics"
    return l == l.upper() and l != ''


group_regex = re.compile('[0-9]+\..+')

def is_group(l):
    return re.fullmatch(group_regex, l)


#I, me - minä [minæ]
word_regex = re.compile('(.+) - (.+) \[(.+)\]')

# Find word line, do a check, split into english/suomea/pronunciation
def get_word(l):
    findall = re.findall(word_regex, l)
    if len(findall) == 0:
        return None
    if len(findall) > 1:
        raise RuntimeError('More than one match found on vocab line')
    return findall[0]


labellines = booklines[booklines.index("ab. - about"):booklines.index("BASIC CONCEPTS")]
labels = [l.split(' - ') for l in labellines if '-' in l]

def get_labels(eng):
    labs = []
    for abbrev, label in labels:
        brackets = f'({abbrev})'
        if brackets in eng:
            labs.append(label)
            eng = eng.replace(brackets, '').strip()
    return labs, eng


vocablines = booklines[booklines.index("BASIC CONCEPTS"):booklines.index("T&P Books Publishing")]

for l in vocablines:
    if is_section(l):
        section = l
        vocab[section] = {}
    if is_topic(l):
        topic = l
    elif is_group(l):
        group = l
        vocab[section][topic] = vocab[section].get(topic, {})
        vocab[section][topic][group] = [[]]
        empty_line_count = 0
    elif l == '':
        empty_line_count += 1
    else:
        getword = get_word(l)
        if getword:
            eng, suo, pro = getword
            labs, eng_no_labs = get_labels(eng)
            word = {
                "English": eng,
                "English no labels": eng_no_labs,
                "Finnish": suo,
                "Pronunciation": pro,
                "Labels": labs
            }
            if empty_line_count >= 3:
                vocab[section][topic][group].append([])
            vocab[section][topic][group][-1].append(word)
            word_counter += 1
            empty_line_count = 0 





with open('vocab.json', 'w') as f:
    json.dump(vocab, f, ensure_ascii=False, indent=4)


print(f"Number of words: {word_counter}")