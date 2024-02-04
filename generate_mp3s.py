from time import sleep
import json
import os
from gtts import gTTS


with open('vocab.json') as f:
    vocab = json.load(f)

for s_title, section in vocab.items():
    for t_title, topic in section.items():
        for g_title, group in topic.items():
            for subgroup in group:
                for word in subgroup:
                    suo = word["Finnish"]
                    suo_fname = word["Finnish for filename"]
                    filename = f'../suomea_mp3s/{suo_fname}.mp3'
                    if not os.path.exists(filename):
                        tts = gTTS(suo, lang='fi')
                        tts.save(filename)
                        print(f'\n\n{suo}\n{filename}')
                        sleep(5)
