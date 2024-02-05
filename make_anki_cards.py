import genanki
import json
import re


# non-greedy; different bracketed qualifiers will be on separate lines
bracket_pattern = re.compile('\(.+?\)')

def format_english_for_card(eng_no_labs, label):
    findall = re.findall(bracket_pattern, eng_no_labs)
    brackets_info_html = ""
    for match in findall:
        brackets_info_html += f'{match}<br>'
        eng_no_labs = eng_no_labs.replace(match, "").strip()
    label_style = "label label-" + label.replace(' ', '_').replace(',', '')
    label_html = f'<br><span class="{label_style}">{label}</span><br>' if label else ""
    return eng_no_labs, brackets_info_html, label_html


with open("eng_finn_question_format.html", "r") as f:
    eng_finn_question_format = f.read()

with open("eng_finn_answer_format.html", "r") as f:
    eng_finn_answer_format = f.read()

with open("finn_eng_question_format.html", "r") as f:
    finn_eng_question_format = f.read()

with open("finn_eng_answer_format.html", "r") as f:
    finn_eng_answer_format = f.read()

with open("style.css", "r") as f:
    style = f.read()


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
      'name': 'Eng Finn',
      'qfmt': eng_finn_question_format,
      'afmt': eng_finn_answer_format
    },
    {
      'name': 'Finn Eng',
      'qfmt': finn_eng_question_format,
      'afmt': finn_eng_answer_format
    },
  ],
  sort_field_index=0,
  css=style
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


def make_anki_cards(vocab, deck_name):

    my_deck = genanki.Deck(
        1219026390,
        deck_name
    )
    mp3_files = []

    for s_title, section in vocab.items():
        for t_title, topic in section.items():
            for g_title, group in topic.items():
                for subgroup in group:
                    for word in subgroup:

                        eng_no_labs = word["English no labels"]
                        label = word["Label"]

                        eng_no_labs, brackets_info_html, label_html = \
                            format_english_for_card(eng_no_labs, label)
                        
                        suo = word["Finnish"]
                        
                        suo_fname = word["Finnish for filename"]
                        mp3 = f'[sound:{suo_fname}.mp3]'
                        mp3_files.append(f'../suomea_mp3s/{suo_fname}.mp3')

                        fields = [
                            "2",
                            eng_no_labs,
                            brackets_info_html,
                            label_html,
                            suo,
                            t_title,
                            g_title,
                            mp3
                        ]

                        my_note = SuomiNote(
                            model=my_model,
                            fields=fields
                        )

                        my_deck.add_note(my_note)

    my_package = genanki.Package(my_deck)
    my_package.media_files = mp3_files
    deck_file = deck_name + '.apkg'
    my_package.write_to_file(deck_file)

    print(f"Deck written to:", deck_file)



with open('test_vocab.json') as f:
    vocab = json.load(f)

#vocab = {"BASIC CONCEPTS": vocab["BASIC CONCEPTS"]}

make_anki_cards(vocab, "Group_1")
