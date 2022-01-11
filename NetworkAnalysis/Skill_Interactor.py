from gtts import gTTS
import speech_recognition as sr

import subprocess
import utilities
import os
import re
import time

from tqdm.notebook import tqdm
import Recorder


class Skill_Interaction:
    def __init__(self, data_dir, persona, skill):
        # persona
        self.PERSONA = persona
        self.SKILL = skill

        # List of skills
        self.DATA_DIR = data_dir
        SKILLS_ADDR = os.path.join(self.DATA_DIR, 'data/subgrouped_skills.json')
        self.all_skills = utilities.read_json(SKILLS_ADDR)[self.PERSONA]

        # default fil names
        self.LAST_RECORDING = 'last-recording'
        self.CURRENT_RECORDING = 'current-recording'
        self.CURRENT_UTTERANCE = 'current-utterance'
        self.ALEXA_STOP = 'alexa-stop'

    def get_responses(self, file_name):
        responses = [self.get_last_response(file_name + '-1.wav'), self.get_last_response(file_name + '-2.wav')]
        return list(filter(None, responses))

    def get_last_response(self, last_recording):
        speech_to_text = sr.Recognizer()
        text = ''

        try:
            with sr.AudioFile(last_recording) as source:
                # listen for the data (load audio to memory)
                audio_data = speech_to_text.record(source)
                # recognize (convert from speech to text)
                text = speech_to_text.recognize_google(audio_data, language="en")
                text = text['alternative'][0]['transcript']
        except:
            pass

        if len(text) == 0:
            return ''

        return text.strip()

    def file_clean_up(self):
        os.remove(self.LAST_RECORDING + '-1.wav')
        os.remove(self.LAST_RECORDING + '-2.wav')

        os.rename(self.CURRENT_RECORDING + '-1.wav', self.LAST_RECORDING + '-1.wav')
        os.rename(self.CURRENT_RECORDING + '-2.wav', self.LAST_RECORDING + '-2.wav')

        utterance_wav = gTTS(text='None', lang='en', slow=False)
        utterance_wav.save(self.CURRENT_RECORDING + '-1.wav')
        utterance_wav.save(self.CURRENT_RECORDING + '-2.wav')

    def get_utterances(self):
        total_extracted = 0
        skills_utterances = []

        for command in self.all_skills[self.SKILL]['Sample_Invocation_Utterances']:
            if command.strip() == '':
                continue
            command = command.replace('”', '').replace('“', '').replace('.', '').strip()

            if not command.lower().startswith('alexa'):
                command = 'Alexa, ' + command

            skills_utterances.append(command)

        skill_desc = self.all_skills[self.SKILL]['Skill_description']. \
            replace('”', '"').replace('“', '"').replace('‘', '').replace('’', '')
        more_commands = re.findall(r'"([^"]*)"', skill_desc)

        more_commands_counter = 0
        for command in more_commands:
            if command.lower().startswith('alexa') and len(command.strip()) > len('alexa'):
                if any(x in command for x in ['*', '#', '(', ')', '[', ']', '{', '}', '<', '>']):
                    continue

                if command.strip().count(' ') > 1 and command.replace('.', '').strip() not in skills_utterances[self.SKILL]:
                    skills_utterances.append(command.replace('.', '').strip())

                    # Only recording 5 occurrences at max from description.
                    more_commands_counter += 1
                    if more_commands_counter >= 5:
                        break

        return skills_utterances

    def play_utterances(self, skills_utterances):
        total_utterances = 0
        for utterance in skills_utterances:
            total_utterances += 1

        for utterance in skills_utterances:
            utterance_wav = gTTS(text=utterance, lang='en', slow=False)
            utterance_wav.save(self.CURRENT_UTTERANCE + '.wav')
            subprocess.call(['aplay', self.CURRENT_UTTERANCE + '.wav'])

            last_responses = self.get_responses(self.LAST_RECORDING)

            # continue to next skill after listening
            record_response = Recorder.Recorder()
            force_stop = record_response.listen(self.CURRENT_RECORDING)
            del record_response

            if force_stop:
                subprocess.call(['aplay', self.ALEXA_STOP + '.wav'])
                print("Stop")

            else:
                current_responses = self.get_responses(self.CURRENT_RECORDING)
                print('LAST:', last_responses)
                print('CURRENT:', current_responses)

                if any(x in current_responses for x in last_responses):
                    subprocess.call(['aplay', self.ALEXA_STOP + '.wav'])

            #self.file_clean_up()
            time.sleep(2)

    def skill_interactor(self):
        print("INTERACTING")
        skills_utterances = self.get_utterances()
        self.play_utterances(skills_utterances)





