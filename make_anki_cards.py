import genanki
import json
import re


with open("question_format.html", "r") as f:
    question_format = f.read()


with open("answer_format.html", "r") as f:
    answer_format = f.read()


# non-greedy; different bracketed qualifiers will be on separate lines
bracket_pattern = re.compile('\(.+?\)')

def format_english_for_card(eng_no_labs, label):
    findall = re.findall(bracket_pattern, eng_no_labs)
    brackets_info_html = ""
    for match in findall:
        brackets_info_html += f'{match}<br>'
        eng_no_labs = eng_no_labs.replace(match, "").strip()
    label_html = f'<span class="{label}">{label}</span><br>' if label else ""
    return eng_no_labs, brackets_info_html, label_html


my_model = genanki.Model(
  1832495621,
  'Simple Model',
  fields=[
    {'name': 'Card ID'},
    {'name': 'English word'},
    {'name': 'English word bracketed info html'},
    {'name': 'English word label html'},
    {'name': 'Finnish'},
    {'name': 'Topic'},
    {'name': 'Group'},
    {'name': 'Finnish MP3'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': question_format,
      'afmt': answer_format
    },
  ],
  sort_field_index=0,
  css="""
    .badge {
        background-color: red;
        color: white;
        padding: 4px 8px;
        text-align: center;
        border-radius: 5px;
        font-size: 12px;
    }
    """
)


class SuomiNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])
    # @property
    # def sort_field(self):
    #     return self.fields[0]





# model ID 1832495620
# rng 1 1219026387
# rng 2 1702824815
# rng 3 1542558840


test_mp3 = '[sound:aamulla_aikaisin.mp3]'


def make_anki_cards(vocab):

    my_deck = genanki.Deck(
        1219026389,
        'test_deck4'
    )

    test_eng_word = 'to be visible (castle, mountain, etc.)'
    test_label = 'badge'

    eng_no_labs, brackets_info_html, label_html = format_english_for_card(test_eng_word, test_label)
    print(eng_no_labs)
    print(brackets_info_html)
    print(label_html)



    fields = [
        "1",
        eng_no_labs,
        brackets_info_html,
        label_html,
        "Suomen sana",
        "CHARACTER. FEELINGS. EMOTIONS",
        "65. Discussion, conversation. Part 1",
        test_mp3
    ]

    my_note = SuomiNote(
        model=my_model,
        fields=fields
    )

    my_deck.add_note(my_note)

    my_note2 = SuomiNote(
        model=my_model,
        fields=fields
    )

    my_deck.add_note(my_note2)

    my_package = genanki.Package(my_deck)
    my_package.media_files = ['aamulla_aikaisin.mp3']
    my_package.write_to_file('test.apkg')

    return 



with open('vocab.json') as f:
    vocab = json.load(f)

vocab = {"BASIC CONCEPTS": vocab["BASIC CONCEPTS"]}

make_anki_cards(vocab)
