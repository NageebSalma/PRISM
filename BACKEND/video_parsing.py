import yt_dlp
print('video_parsing.py')
ydl_opts = {
    "format": "best[ext=mp4]",  # Combine video and audio streams
    "merge_output_format": "mp4",          # Ensure output is a single file
    "noplaylist": True,                    # noplaylist option incase a playlist is passed, not to download the whole thing
    "retries": 5,
    'quiet' : True,
}


def get_video_information(youtube_video_url):
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_video_url , download=False)
    
    video_information = {
    'id' : info['id'],
    'title' : info['title'],
    'url' : info['url'],
    'comment_count' : info["comment_count"],
    'fps' : info['fps'],
    }
    print('end of video_parsing.py')
    return video_information

