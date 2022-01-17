import os
import ffmpy
import librosa
inputdir = '/Users/maxwhite/PycharmProjects/Selenium/videos'
for filename in os.listdir(inputdir):
    old_file = os.path.join(inputdir, filename)
    if old_file.endswith(".mp4"):
        actual_filename = filename[:-4]
        new_file = os.system('ffmpeg -i {} -acodec pcm_s16le -ar 16000 {}.wav'.format(old_file, actual_filename))
        os.remove(old_file)


