from tkinter.filedialog import askDirectory
from pytube import YouTube
import shutil
import os


def DownloadYT():
    link = input('Enter Link: ')
    yt = YouTube(link)

    print(f'Title: {yt.title}\nNumber of Views: {yt.views}\nLength of Video: {yt.length/60:.2f}\nRating: {yt.rating:.2f}')

    isAudioOnly = input("Audio Only?: ").lower()

    path = askDirectory()

    if isAudioOnly == 'yes':
        ys = yt.streams.get_audio_only()
        print('Downloading...')
        
        ys.download()
        os.rename(f'{yt.title}.mp4', f'{yt.title}.mp3')

        shutil.move(f'{yt.title}.mp3', f'Music/{yt.title}.mp3')
        print('Download Complete')

    else:
        ys = yt.streams.get_highest_resolution()
        print('Downloading, This may take a while due to large file sizes...')

        ys.download()

        shutil.move(f'{yt.title}.mp4', f'Videos/{yt.title}.mp4')
        print('Download Complete')
