"""
TheNexusAvenger

Handles HTTP requests to YouTube.
"""

import yt_dlp


def downloadMp3(url: str, path: str) -> None:
    """Downloads a YouTube video as an MP3.

    :param url: URL to download from.
    :param path: Path to save to.
    """

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': path.replace(".mp3", ""),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])