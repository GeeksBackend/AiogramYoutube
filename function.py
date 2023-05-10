from pytube import YouTube
import uuid

MAX_SIZE=50000000

pattern1 = 'www.youtube.com'
pattern2 = 'youtu.be'

def is_youtube_link(link:str):
    if link.find(pattern1) != -1 or link.find(pattern2) != -1:
        return True
    else:
        return False

def resolutions(link):
    yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    res = []
    for stream in yt.streams.filter(progressive=True):
        if stream.resolution not in res:
            if stream.resolution != None:
                res.append(stream.resolution)
    return res

def download_video(link, res):
    yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    tp = yt.streams.filter(resolution=res, progressive=True).first().subtype
    name = str(uuid.uuid4()) + '.' + tp
    yt.streams.filter(resolution=res, progressive=True).first().download(filename=name)
    return name

def download_audio(link):
    yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    tp = yt.streams.filter(only_audio=True).first().subtype
    name = str(uuid.uuid4()) + '.' + tp
    yt.streams.filter(only_audio=True).first().download(filename=name)
    return name