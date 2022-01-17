import time
from pytube import YouTube
import os
import ffmpy
from pathlib import Path
import requests
from pydub import AudioSegment
from ParseID import parse_id
import pandas as pd
def download_audio(line, output_path):
    print(YouTube('http://youtube.com/watch?v=' + line).streams.filter(only_audio=True).first().download(output_path))
    try:
        YouTube('http://youtube.com/watch?v=' + line).streams.filter(only_audio=True).first().download(output_path)
        return True
    except:
        return False


def download_audious(video, output_path):
    with open(video, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print('downloading audio:' + line)
            result = download_audio(line, output_path)
            print(result)
            time.sleep(30)

            if not result:
                result = download_audio(line, output_path)
                time.sleep(30)
                if not result:
                    print(f'file {line} is not downloaded')

def reformat_audio(data_path):
    i = 0
    file_names = []
    new_names = []
    for filename in os.listdir(data_path):
        i = i+1
        old_file = os.path.join(data_path, filename)
        print(old_file)
        if old_file.endswith(".mp4"):
            file_names.append(filename)
            base, ext = os.path.splitext(old_file)
            new_file = "video" + str(i) + ext
            #new_file = old_file
            new_names.append(new_file.replace('mp4', 'wav'))
            os.rename(old_file, new_file)
            actual_filename = new_file[:-4]
            os.system('ffmpeg -i {} -acodec pcm_s16le -ac 1 -ar 16000 {}.wav'.format(new_file, actual_filename))
            os.remove(new_file)
    return file_names, new_names


def make_mashups(data_path, save_path, interval_between_slice):
    lengths = []
    for filename in os.listdir(data_path):
        old_file = os.path.join(data_path, filename)
        if old_file.endswith('.wav'):
            print(old_file)
            audio = AudioSegment.from_wav(old_file)
            length = audio.duration_seconds
            print(length)
            a = 0
            audio_mashup = 0
            lengths.append(length)
            for i in range(int(round(length)/interval_between_slice)):
                five_second = 5 * 1000 + a
                sample = audio[a:five_second]
                audio_mashup += sample
                a += interval_between_slice * 1000

            print(f'done with {filename}')
            try:
                audio_mashup.export(f'{save_path}/audio_mashup_{filename}', format="wav")
            except:
                print('Mashup cant be done due to file problems: too short or bad audio')
                continue
    return lengths

def main(videos_txt_path, data_path, save_path, request_string, pages_to_search, interval_between_slice):
    urls = parse_id(request_string, videos_txt_path, pages_to_search)
    download_audious(videos_txt_path, data_path)
    names = reformat_audio(data_path)
    lengths = make_mashups(data_path, save_path, interval_between_slice)
    df = pd.DataFrame(urls, columns=['URL-S'])
    df1 = pd.DataFrame(names[0], columns=['Actual_name'])
    df2 = pd.DataFrame(names[1], columns=['audiosample_name'])
    df3 = pd.DataFrame(lengths, columns=['Length of video in secs'])
    df_sum = df.join(df1, how='outer')
    df_sum = df_sum.join(df2, how='outer')
    df_sum = df_sum.join(df3, how='outer')
    df_sum.to_excel('Data.xlsx')

if __name__ == "__main__":
    pages_to_search = 1 # Сколько страниц просмотреть
    interval_between_slice = 300 # Интервал между сэмплами в мэшапе
    request_string = 'rofl' # Строка, что ищем
    #downloaded = '/Users/maxwhite/PycharmProjects/yotube/downloaded.txt' # TXT
    videos = '/Users/maxwhite/PycharmProjects/yotube/videos.txt' # Путь до txt куда будут сохраняться ID видео
    data_path = '/Users/maxwhite/PycharmProjects/yotube/videos' # Папка куда будут сохраняться видео и эксель
    save_path = '/Users/maxwhite/PycharmProjects/yotube/mashups' # Папка куда будуть сохраняться мэшапы
    main(videos, data_path, save_path,request_string,pages_to_search, interval_between_slice)
