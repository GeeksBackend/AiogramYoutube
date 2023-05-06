from pytube import YouTube

url = input("URL: ")
yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
# yt.streams.filter(progressive=True, file_extension='mp4', res='360p').order_by('resolution').desc().first().download()
yt.streams.filter(only_audio=True).first().download('audio', f'{yt.title}.mp3')