"""
TheNexusAvenger

Handles HTTP requests to BeatSaver.
"""

import json
import os
import requests
import time
from data.Song import Song
from typing import List


def get(url: str) -> bytes:
    """Fetches the contents for a URL.

    :param url: URL to fetch.
    :return: The binary response.
    """

    # Get the response.
    response = requests.get(url).content

    # Try to parse the JSON response and re-run if it is requires a retry.
    try:
        responseString = response.decode()
        responseJson = json.loads(responseString)
        if "identifier" in responseJson and responseJson["identifier"] == "RATE_LIMIT_EXCEEDED":
            delay = (responseJson["resetAfter"] / 1000) + 1
            print("Rate limit reached. Retrying in " + str(delay) + " seconds.")
            time.sleep(delay)
            return get(url)
    except Exception:
        pass

    # Return the response.
    return response


def getPage(page: int) -> List[Song]:
    """Returns the songs for the specified page.

    :param page: Page to fetch.
    :return: The songs on the page.
    """

    songs = []
    pageData = json.loads(get("https://api.beatsaver.com/search/text/" + str(page) + "?sortOrder=Latest").decode())
    for songData in pageData["docs"]:
        song = Song()
        song.artist = songData["metadata"]["songAuthorName"]
        song.songName = songData["metadata"]["songName"]
        song.songSubName = songData["metadata"]["songSubName"]
        song.beatSaverKey = songData["id"]
        songs.append(song)
    return songs


def downloadMap(beatSaverId: str, downloadLocation: str) -> None:
    """Downloads a map.

    :param beatSaverId: BeatSaver id to download.
    :param downloadLocation: Location to save the downloaded file to.
    """

    # Get the map information.
    mapData = json.loads(get("https://api.beatsaver.com/maps/id/" + beatSaverId).decode())
    downloadUrl = mapData["versions"][0]["downloadURL"]

    # Download the map.
    parentDirectory = os.path.dirname(downloadLocation)
    if not os.path.exists(parentDirectory):
        os.makedirs(parentDirectory)
    with open(downloadLocation, "wb") as file:
        file.write(get(downloadUrl))
