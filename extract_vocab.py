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


labellines = booklines[booklines.index("ab. - about"):booklines.index("BASIC CONCEPTS")]
labels = [l.split(' - ') for l in labellines if '-' in l]

def get_labels(eng):
    labs = []
    for abbrev, label in labels:
        brackets = f'({abbrev})'
        if brackets in eng:
            labs.append(label)
            eng = eng.replace(brackets, '').strip()
    if len(labs) > 1:
        raise RuntimeError('More than one label on english word')
    if labs:
        labs = labs[0]
    else:
        labs = ""
    return labs, eng


vocab_alphabet = "ABCDEÉFGHIJKLMNOPQRSŠTUVWXYZŽÅÄÖÜ"
filename_chars = [char for char in vocab_alphabet]
filename_chars += [char.lower() for char in vocab_alphabet]
filename_chars += [' ', '-']

def finnish_to_filename(suo):
    return "".join(char for char in suo if char in filename_chars)


#I, me - minä [minæ]
word_regex = re.compile('(.+) - (.+?) \[(.+)\]')

# Find word line, do a check, split into english/suomea/pronunciation
def get_word(l):
    findall = re.findall(word_regex, l)
    if len(findall) == 0:
        return None
    if len(findall) > 1:
        raise RuntimeError('More than one match found on vocab line')
    eng, suo, pro = findall[0]
    labs, eng_no_labs = get_labels(eng)
    pro = pro.replace('[', '').replace(']', '')
    suo_fname = finnish_to_filename(suo)
    return eng, eng_no_labs, suo, suo_fname, pro, labs


vocablines = booklines[booklines.index("BASIC CONCEPTS"):booklines.index("T&P Books Publishing")]


maxlen = {
    "English": "",
    "Finnish": "",
    "Topic and group combined": ""
}


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
        t_and_g = topic + " - " + group
        if len(t_and_g) > len(maxlen["Topic and group combined"]):
            maxlen["Topic and group combined"] = t_and_g
    elif l == '':
        empty_line_count += 1
    else:
        getword = get_word(l)
        if getword:
            eng, eng_no_labs, suo, suo_fname, pro, labs = getword
            word = {
                "Word Number": str(word_counter),
                "English": eng,
                "English no labels": eng_no_labs,
                "Finnish": suo,
                "Finnish for filename": suo_fname,
                "Pronunciation": pro,
                "Label": labs,
            }
            if empty_line_count >= 3:
                vocab[section][topic][group].append([])
            vocab[section][topic][group][-1].append(word)
            word_counter += 1
            empty_line_count = 0
            if len(eng) > len(maxlen["English"]):
                maxlen["English"] = eng
            if len(suo) > len(maxlen["Finnish"]):
                maxlen["Finnish"] = suo




with open('vocab.json', 'w') as f:
    json.dump(vocab, f, ensure_ascii=False, indent=4)


print(f"Number of words: {word_counter}")
print("Longest words:")
for lang, length in maxlen.items():
    print(f"{lang}: {length}")