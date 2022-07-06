"""
TheNexusAvenger

Handles HTTP requests to YouTube.
"""

import youtube_dl


def downloadMp3(url: str, path: str) -> None:
    """Downloads a YouTube video as an MP3.

    :param url: URL to download from.
    :param path: Path to save to.
    """

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': path.replace(".mp3", ".m4a"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])