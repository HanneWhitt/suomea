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


def make_card_id(s_idx, t_idx, direction, g_idx, sg_idx, w_idx, x_idx):
    s_str = "S" + str(s_idx).zfill(2) + "0000"
    t_str = "T" + str(t_idx).zfill(4) + "0000"
    if direction not in ['eng-finn', 'finn-eng']:
         raise ValueError("direction arg must be in ['eng-finn', 'finn-eng']")
    g_str = "G" + str(g_idx).zfill(6) + "0000"
    sg_str = "SG" + str(sg_idx).zfill(6) + "0000"
    w_str = "W" + str(w_idx).zfill(4) + "0000"
    x_str = "X" + str(x_idx).zfill(4) + "0000"
    card_id = f"0000{s_str}{t_str}{direction}{g_str}{sg_str}{w_str}{x_str}"
    return card_id, s_str, t_str, direction, g_str, sg_str, w_str, x_str


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


fields=[
    {'name': 'Card ID'},
    {'name': 'Section ID'},
    {'name': 'Section'},
    {'name': 'Topic ID'},
    {'name': 'Topic'},
    {'name': 'Direction of translation'},
    {'name': 'Group ID'},
    {'name': 'Group'},
    {'name': 'Subgroup ID'},
    {'name': 'Subgroup'},
    {'name': 'Word ID'},
    {'name': 'Word Number'},
    {'name': 'X ID'},
    {'name': 'X'},
    {'name': 'English word, labels'},
    {'name': 'English word, no labels'},
    {'name': 'English word bracketed info html'},
    {'name': 'English word label html'},
    {'name': 'Finnish'},
    {'name': 'Finnish for filename'},
    {'name': 'Pronunciation'},
    {'name': 'Label'},
    {'name': 'Finnish MP3'}
]


eng_finn_model = genanki.Model(
  1832495622,
  'Eng-Finn Model',
  fields=fields,
  templates=[
    {
      'name': 'Original Template',
      'qfmt': eng_finn_question_format,
      'afmt': eng_finn_answer_format
    },
  ],
  sort_field_index=0,
  css=style
)

finn_eng_model = genanki.Model(
  1832495623,
  'Eng-Finn Model',
  fields = fields,
  templates=[
    {
      'name': 'Original Template',
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
# rng 2 
# rng 3 1542558840


def make_anki_cards(vocab):

    mp3_files = []
    subdecks = []
    subdeck_id = 1702826815
    t_idx = 0
    g_idx = 0

    for s_idx, (s_title, section) in enumerate(vocab.items()):
        for t_title, topic in section.items():

            t_idx += 1
            topic_zfill = str(t_idx).zfill(2)

            for g_title, group in topic.items():

                g_idx = int(g_title[:g_title.find('.')])
                group_zfill = str(g_idx).zfill(3)
                subdeck_name = f'Suomea::T{topic_zfill} - {t_title}::G{group_zfill} - {g_title}'

                subdeck_id += 1

                group_subdeck = genanki.Deck(
                    subdeck_id,
                    subdeck_name
                )

                for sg_idx, subgroup in enumerate(group):
                    for word in subgroup:

                        eng_no_labs = word["English no labels"]
                        label = word["Label"]

                        eng_no_labs, brackets_info_html, label_html = \
                            format_english_for_card(eng_no_labs, label)
                        
                        suo = word["Finnish"]
                        
                        suo_fname = word["Finnish for filename"]
                        mp3 = f'[sound:{suo_fname}.mp3]'
                        mp3_files.append(f'../suomea_mp3s/{suo_fname}.mp3')

                        direction = 'eng-finn'
                        word_number = word["Word Number"]

                        card_id, s_str, t_str, direction, g_str, sg_str, w_str, x_str = \
                            make_card_id(s_idx, t_idx, direction, g_idx, sg_idx, word_number, 0)

                        eng_finn_fields = [
                            card_id,
                            s_str,
                            s_title,
                            t_str,
                            t_title,
                            direction, 
                            g_str,
                            g_title,
                            sg_str,
                            str(sg_idx),
                            w_str,
                            word_number,
                            x_str,
                            "0",
                            word["English"],
                            eng_no_labs,
                            brackets_info_html,
                            label_html,
                            suo,
                            suo_fname,
                            word["Pronunciation"],
                            word["Label"],
                            mp3
                        ]

                        eng_finn_note = SuomiNote(
                            model=eng_finn_model,
                            fields=eng_finn_fields
                        )
                        group_subdeck.add_note(eng_finn_note)

                for sg_idx, subgroup in enumerate(group):
                    for word in subgroup:

                        eng_no_labs = word["English no labels"]
                        label = word["Label"]

                        eng_no_labs, brackets_info_html, label_html = \
                            format_english_for_card(eng_no_labs, label)
                        
                        suo = word["Finnish"]
                        
                        suo_fname = word["Finnish for filename"]
                        mp3 = f'[sound:{suo_fname}.mp3]'
                        mp3_files.append(f'../suomea_mp3s/{suo_fname}.mp3')


                        direction = 'finn-eng'
                        word_number = word["Word Number"]


                        card_id, s_str, t_str, direction, g_str, sg_str, w_str, x_str = \
                            make_card_id(s_idx, t_idx, direction, g_idx, sg_idx, word_number, 0)

                        finn_eng_fields = [
                            card_id,
                            s_str,
                            s_title,
                            t_str,
                            t_title,
                            direction, 
                            g_str,
                            g_title,
                            sg_str,
                            str(sg_idx),
                            w_str,
                            word_number,
                            x_str,
                            "0",
                            word["English"],
                            eng_no_labs,
                            brackets_info_html,
                            label_html,
                            suo,
                            suo_fname,
                            word["Pronunciation"],
                            word["Label"],
                            mp3
                        ]

                        finn_eng_note = SuomiNote(
                            model=finn_eng_model,
                            fields=finn_eng_fields
                        )
                        group_subdeck.add_note(finn_eng_note)

                subdecks.append(group_subdeck)

    package = genanki.Package(subdecks)
    package.media_files = mp3_files
    deck_file = "Suomea.apkg"
    package.write_to_file(deck_file)

    print(f"Deck written to:", deck_file)



with open('vocab.json') as f:
    vocab = json.load(f)

#vocab = {"BASIC CONCEPTS": vocab["BASIC CONCEPTS"]}

make_anki_cards(vocab)
