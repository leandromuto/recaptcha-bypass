import speech_recognition as sr
import urllib
import requests
import os
import pathlib
import random
import datetime
from pydub import AudioSegment

class Speech():
    def __init__(self):
        pass

    # TODO: improve this method to handle the exceptions
    def __download_file(self, url):
        req = requests.get(url, allow_redirects = True)
        if req.headers.get('content-type') == 'audio/mp3':
            now = datetime.datetime.now()

            mp3_name = "/../../tmp/audio_file_%d%d%d%d%d%d.mp3" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
            open(mp3_name, mode = "wb").write(req.content)
            file_path = pathlib.Path(mp3_name)

            if file_path.exists:
                wav_audio_path = self.__convert_mp3_to_wav(str(file_path))

                if wav_audio_path.exists:
                    print("File downloaded and converted successfully.")
                    return wav_audio_path

    def __convert_mp3_to_wav(self, mp3_audio_path):
        if pathlib.Path(mp3_audio_path).exists:
            now = datetime.datetime.now()
            wav_name = "/../../tmp/audio_file_%d%d%d%d%d%d.wav" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
            print("AUDIO PATH: " + mp3_audio_path)
            audio = AudioSegment.from_mp3(mp3_audio_path)
            audio.export(out_f = wav_name, format = "wav") # exporting mp3 to wav format

            wav_audio_file_path = pathlib.Path(wav_name)
            return wav_audio_file_path

    def speech_to_text(self, url):
        if url is not None:
            wav_audio = self.__download_file(url)

            if wav_audio.exists:
                r = sr.Recognizer()

                with sr.AudioFile(str(wav_audio)) as source:
                    audio = r.record(source)
                    result = r.recognize_google(audio)
                    print("Speech to text: {}".format(result))
                    return result
        else:
            print("Error. URL is null.")

if __name__ == "__main__":
    pass
