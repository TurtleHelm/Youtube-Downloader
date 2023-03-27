from tkinter.filedialog import askdirectory, askopenfilename
from pytube import YouTube, Stream, Playlist
from os import curdir, rename
from tqdm import tqdm

def progress_callback(stream:Stream, data_chunk:bytes, bytes_remaining:int) -> None: 
    pbar.update(round(len(data_chunk)/1000))

def DownloadVideo(ytObj:YouTube, path:str='') -> None: 
    try:
        global pbar

        print('Fetching Highest Resolution Video')
        yt = ytObj.streams.get_highest_resolution()
        print(f'Highest Resolution Found: {yt.resolution}')
        
        print(f'Downloading {yt.title} (File Size: ~{yt.filesize_mb:.2f}mb)')
        pbar = tqdm(total=round(yt.filesize_kb), unit='kb')
        
        yt.download(path)
        pbar.close()
        print(f'\nDownloaded {yt.title} Successfully')
    except Exception as e:
        print(f'Unexpected Error Occurred\n{e}')
        pass

def DownloadAudio(ytObj:YouTube, path:str='') -> None:
    try:
        global pbar
        print('Fetching Highest Resolution Audio')
        yt = ytObj.streams.filter(only_audio=True).first()
        print(f'Highest Resolution Found: {yt.resolution}')

        print(f'Downloading {yt.title} (File Size: ~{yt.filesize_mb:.2f}mb)')
        pbar = tqdm(total=round(yt.filesize_kb), unit='kb')

        yt.download(path)
        pbar.close()
        rename(f'{path}/{yt.title}.mp4', f'{path}/{yt.title}.mp3')
        print(f'\nDownloaded {yt.title} Successfully')
    except Exception as e:
        print(f'Unexpected Error Occurred\n{e}')
        pass

def DownloadYTSingle():

    try:
        global pbar

        path = askdirectory(initialdir=curdir)
        notCorrect = 'n'
        
        while notCorrect == 'n' or notCorrect == 'no':
            url = input('Enter URL: ')
            yt = YouTube(url, on_progress_callback=progress_callback)

            print(f'Title: {yt.title}\nAcc. Name: {yt.author}\nNo. Of Views: {yt.views}\nVideo Length: {yt.length/60:.2f}m')
            notCorrect = input('Is this Information Correct? ').lower()

        selection = input("Audio Only? ").lower()

        if selection == 'yes' or selection == 'y':
            DownloadAudio(yt, path)
                   
            repeat = input('Download Another Audio Clip? ')
            
            if repeat == 'yes' or repeat == 'y': DownloadYTSingle()
            else: quit(0)

        else: 
            DownloadVideo(yt, path)
            repeat = input('Download Another Audio Clip? ')
            
            if repeat == 'yes' or repeat == 'y': DownloadYTSingle()
            else: quit(0)
   
    except Exception as e:
        print(f'An Unexpected Error Occurred: {e}')
        DownloadYTSingle()

def DownloadYTMultiple():
    
    global pbar
    
    print('Select Directory to Download All Files To')
    path = askdirectory()
    
    print('URL File Was Left Empty, Please Select the File to be used')
    urlFile = askopenfilename()
    
    selection = input('Audio Only? (This is for all Files): ').lower()

    with open(urlFile) as f: urls = f.read().split(',')
    
    if urls == []: print('Error: URL File Passed in does not have any data to work with')
    
    else:
        for i in range(len(urls)):
            print(f'{i}/{len(urls)} Downloaded')
            
            if selection == 'y' or selection == 'yes':
                yt = YouTube(urls[i], on_progress_callback=progress_callback)
                DownloadAudio(yt, path)
            else:
                yt = YouTube(urls[i], on_progress_callback=progress_callback)
                DownloadVideo(yt, path)
                
        print('\nDownloaded All URLs')

def DownloadYTPlaylist():
    
    global pbar

    print('Enter Directory to Download Files to')
    path = askdirectory()
    correct = 'n'

    while correct == 'n' or correct == 'no':
        url = input('Enter Playlist URL: ')    
    
        ytp = Playlist(url)
        ytpUrls = ytp.videos
    
        print(f'Title: {ytp.title}\nAcc. Name: {ytp.owner}\nNo. Of Views: {ytp.views}\n')
    
        correct = input('Is this correct? ').lower()
    
    selection = input('Audio Only? ').lower()
    
    if selection == 'y' or selection == 'yes':
        for i in range(len(ytpUrls)):
            yt = ytpUrls[i]
            yt.register_on_progress_callback(progress_callback)
            DownloadVideo(yt, path)
    else:
        for i in range(len(ytpUrls)):
            yt = ytpUrls[i]
            yt.register_on_progress_callback(progress_callback)
            DownloadAudio(yt, path)

    print('Downloaded All Playlist URLs')

def main() -> None:
    
    print('YouTube Downloader\nSelect a Mode')
    print('1: Download a Single File\n2: Use a URL File to Download Multiple Files\n3: Download all URLs in a Playlist')
    choice = int(input('Enter Choice: '))
    
    match choice:
        case 1: DownloadYTSingle()
        case 2: DownloadYTMultiple()
        case 3: DownloadYTPlaylist()
        case _: pass

main()