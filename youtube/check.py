from pydub import AudioSegment
import os
audio = '/Users/maxwhite/PycharmProjects/youtube/videos'
def check(audio_path):
    for files in os.listdir(audio_path):
        if files.endswith('.wav'):
            print(files)
            file = os.path.join(audio_path, files)
            file = AudioSegment.from_file(file)
            length = file.duration_seconds
            if length > 300:
                raise Exception('Too long audio')
            else:
                print('OK')
check(audio)