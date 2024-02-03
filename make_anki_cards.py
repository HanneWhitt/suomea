import genanki
import json


with open("question_format.html", "r") as f:
    question_format = f.read()


with open("answer_format.html", "r") as f:
    answer_format = f.read()


my_model = genanki.Model(
  1832495620,
  'Simple Model',
  fields=[
    {'name': 'Word Number'},
    {'name': 'English'},
    {'name': 'Finnish'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': question_format,
      'afmt': answer_format
    },
  ],
  sort_field_index=0
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

def make_anki_cards(vocab):

    my_deck = genanki.Deck(
        1219026387,
        'test_deck'
    )

    my_note = SuomiNote(
        model=my_model,
        fields=["0", "I, me", "minä"]
    )

    my_deck.add_note(my_note)

    my_note2 = SuomiNote(
        model=my_model,
        fields=["1", "you", "sinä"]
    )

    my_deck.add_note(my_note2)

    genanki.Package(my_deck).write_to_file('test_deck_output.apkg')




    return 



with open('vocab.json') as f:
    vocab = json.load(f)

vocab = {"BASIC CONCEPTS": vocab["BASIC CONCEPTS"]}

make_anki_cards(vocab)
