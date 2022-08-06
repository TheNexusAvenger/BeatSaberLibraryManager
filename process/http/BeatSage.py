"""
TheNexusAvenger

Handles HTTP requests to Beat Sage.
"""

import librosa
import json
import os
import random
import string
import shutil
import requests
from data.Song import Song
from pydub import AudioSegment
from requests_toolbelt import MultipartEncoder
from zipfile import ZipFile

DIFFICULTIES = "Expert,ExpertPlus"
MODES = "Standard"
SYSTEM_VERSION = "v2-flow"


def getBpm(fileLocation: str) -> float:
    """Gets the BPM for a file name.

    :param fileLocation: Location of the file.
    :return: The BPM of the file.
    """

    y, sr = librosa.load(fileLocation)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    return float(librosa.beat.tempo(onset_envelope=onset_env, sr=sr))

def getBeatSageMap(audioFileLocation: str, coverFileLocation: str, downloadFileLocation: str) -> None:
    """Requests downloading a map from Beat Sage.

    :param audioFileLocation: Location of the audio file.
    :param coverFileLocation: Location of the cover file.
    :param downloadFileLocation: Location to save the archive file.
    """

    # Send the download request.
    fields = {
        "audio_file": ("audio", open(audioFileLocation, "rb"), "audio/mpeg"),
        "cover_art": ("cover", open(coverFileLocation, "rb"), "image/" + os.path.splitext(os.path.basename(coverFileLocation))[1][1:]),
        "audio_metadata_title": "ArtistName",
        "audio_metadata_artist": "SongName",
        "difficulties": DIFFICULTIES,
        "modes": MODES,
        "events": "",
        "environment": "DefaultEnvironment",
        "system_tag": SYSTEM_VERSION,
    }
    boundary = "----WebKitFormBoundary" + "".join(random.sample(string.ascii_letters + string.digits, 16))
    message = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {
        "Host": "beatsage.com",
        "Connection": "keep-alive",
        "Content-Type": message.content_type
    }
    createMapResponse = requests.post("https://beatsage.com/beatsaber_custom_level_create", headers=headers, data=message)
    try:
        downloadMapId = createMapResponse.json()["id"]
    except:
        print("Unexpected response from Beat Sage: " + str(createMapResponse.text))
        raise

    # Download the map.
    mapUrl = "https://beatsage.com/beatsaber_custom_level_download/" + downloadMapId
    import time
    while True:
        mapResponse = requests.get(mapUrl)
        if mapResponse.headers["content-type"] == "application/octet-stream":
            with open(downloadFileLocation, "wb") as file:
                file.write(mapResponse.content)
                break
        time.sleep(0.25)


def processBeatSageMap(song: Song, audioFileLocation: str, coverFileLocation: str, downloadLocation: str, mapLocation: str) -> None:
    """Processes a Beat Sage map.

    :param song: Song of the map.
    :param audioFileLocation: Location of the audio file.
    :param coverFileLocation: Location of the cover file.
    :param downloadLocation: Download location of the Beat Sage map.
    :param mapLocation: Location to process the map to.
    """

    with ZipFile(downloadLocation) as mapArchive:
        # Create the map directory.
        if not os.path.exists(mapLocation):
            os.makedirs(mapLocation)

        # Determine the initial delay.
        bpm = getBpm(audioFileLocation)
        startDelay = 2
        secondsPerBeat = 60 * (1 / bpm)
        initialDelayBeats = round(startDelay / secondsPerBeat)
        initialDelaySeconds = initialDelayBeats * secondsPerBeat

        # Create the new audio file.
        if not os.path.exists(mapLocation + "/song.ogg"):
            silenceSegment = AudioSegment.silent(round(initialDelaySeconds * 1000))
            musicSegment = AudioSegment.from_mp3(audioFileLocation)
            newSection = silenceSegment + musicSegment
            newSection.export(mapLocation + "/song.ogg", "ogg")

        # Get the map info.
        mapInfo = json.loads(mapArchive.read("Info.dat"))
        originalBpm = mapInfo["_beatsPerMinute"]

        # Change the map info.
        mapInfo["_songAuthorName"] = song.artist
        mapInfo["_songName"] = song.songName
        mapInfo["_songSubName"] = song.songSubName
        mapInfo["_levelAuthorName"] = "Beat Sage (Reprocessed)"
        mapInfo["_beatsPerMinute"] = bpm
        mapFiles = []
        for difficultySet in mapInfo["_difficultyBeatmapSets"]:
            for difficultyMap in difficultySet["_difficultyBeatmaps"]:
                if difficultyMap["_beatmapFilename"] not in mapFiles:
                    mapFiles.append(difficultyMap["_beatmapFilename"])

        # Copy the cover.
        coverExtension = os.path.basename(coverFileLocation).split(".")[1]
        shutil.copy(coverFileLocation, os.path.join(mapLocation, "cover." + coverExtension))
        mapInfo["_coverImageFilename"] = "cover." + coverExtension

        # Process the difficulty maps.
        for fileName in mapFiles:
            if not os.path.exists(mapLocation + "/" + fileName):
                mapData = json.loads(mapArchive.read(fileName))
                for note in mapData["_notes"]:
                    noteTime = (note["_time"] * (60 / originalBpm)) - 1
                    note["_time"] = (noteTime / secondsPerBeat) + initialDelayBeats
                with open(mapLocation + "/" + fileName, "w") as file:
                    file.write(json.dumps(mapData).replace(" ", ""))

        # Write the map info file.
        # This is done last since the previous checks use the Info.dat file.
        if not os.path.exists(mapLocation + "/Info.dat"):
            with open(mapLocation + "/Info.dat", "w") as file:
                file.write(json.dumps(mapInfo, indent=4))
