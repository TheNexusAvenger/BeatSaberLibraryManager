"""
TheNexusAvenger

Downloads and processes maps.
"""

import os
import shutil

from data import Configuration
from data.Database import Database
from data.Song import Song
from process.ProcessMap import processMaps
from process.http import BeatSage
from process.http import BeatSaver
from process.http import Generic
from process.http import YouTube


# Open the database.
database = Database()
baseDownloadsPath = os.path.realpath(os.path.join(__file__, "..", "..", "..", "maps", "Downloads"))
coversDownloadsPath = os.path.join(baseDownloadsPath, "Covers")
beatSageDownloadsPath = os.path.join(baseDownloadsPath, "BeatSage")
beatSageRawDownloadsPath = os.path.join(baseDownloadsPath, "BeatSage", "Raw")
if not os.path.exists(coversDownloadsPath):
    os.makedirs(coversDownloadsPath)
if not os.path.exists(beatSageRawDownloadsPath):
    os.makedirs(beatSageRawDownloadsPath)

# Get the songs to process.
beatSaverEnabled = Configuration.sourceEnabled("BeatSaver")
beatSageEnabled = Configuration.sourceEnabled("BeatSage")
songsToProcess = []
if beatSaverEnabled:
    for songData in database.execute("SELECT Artist,SongName,SongSubName,Validated,BeatSaverKey FROM BeatSaverMaps WHERE Include = 1;"):
        # Store the base data.
        song = Song()
        song.mapSource = "BeatSaver"
        song.artist = songData[0]
        song.songName = songData[1]
        song.songSubName = songData[2]
        song.validated = (songData[3] == 1)
        song.beatSaverKey = songData[4]
        song.mapDownloadPath = os.path.join(baseDownloadsPath, "BeatSaver", song.getSongName(True) + " [BeatSaver " + song.beatSaverKey + "].zip")

        # Add the song.
        songsToProcess.append(song)
if beatSageEnabled:
    for songData in database.execute("SELECT Artist,SongName,SongSubName,Validated,SongURL,CoverURL FROM BeatSageMaps WHERE Include = 1;"):
        # Store the base data.
        song = Song()
        song.mapSource = "BeatSage"
        song.artist = songData[0]
        song.songName = songData[1]
        song.songSubName = songData[2]
        song.validated = (songData[3] == 1)
        song.songUrl = songData[4]
        song.coverUrl = songData[5]
        song.mapDownloadPath = os.path.join(baseDownloadsPath, "BeatSage", song.getSongName(True))

        # Add the song.
        songsToProcess.append(song)

# Download the missing maps from BeatSaver.
if beatSaverEnabled:
    print("Downloading missing maps from BeatSaver.")
    for song in songsToProcess:
        if song.mapSource == "BeatSaver" and not os.path.exists(song.mapDownloadPath):
            print("\tDownloading " + song.getSongName())
            BeatSaver.downloadMap(song.beatSaverKey, song.mapDownloadPath)

# Download the missing maps from Beat Sage.
if beatSageEnabled:
    print("Downloading missing maps from Beat Sage.")
    for song in songsToProcess:
        if song.mapSource == "BeatSage":
            songName = song.getSongName(True)
            mapArchivePath = os.path.join(beatSageRawDownloadsPath, songName + ".zip")
            if os.path.exists(song.mapDownloadPath) and not os.path.exists(mapArchivePath):
                # Clear the existing map if the download was deleted (rejected).
                shutil.rmtree(song.mapDownloadPath)

            if not os.path.exists(os.path.join(song.mapDownloadPath, "Info.dat")):
                # Download the cover.
                print("\tDownloading " + song.getSongName())
                coverPathWithoutExtension = os.path.join(baseDownloadsPath, "Covers", songName)
                coverPath = None
                for existingFile in os.listdir(coversDownloadsPath):
                    if existingFile.startswith(songName + "."):
                        coverPath = os.path.join(baseDownloadsPath, "Covers", existingFile)
                if coverPath is None:
                    print("\t\tDownloading the cover art.")
                    coverPath = Generic.downloadImage(song.coverUrl, coverPathWithoutExtension)

                # Download the song.
                songPath = os.path.join(baseDownloadsPath, "Songs", songName + ".mp3")
                if not os.path.exists(songPath):
                    print("\t\tDownloading the song file.")
                    YouTube.downloadMp3(song.songUrl, songPath)

                # Request the map.
                if not os.path.exists(mapArchivePath):
                    print("\t\tRequesting the map from Beat Sage.")
                    BeatSage.getBeatSageMap(songPath, coverPath, mapArchivePath)

                # Process the map.
                print("\t\tProcessing Beat Sage map.")
                BeatSage.processBeatSageMap(song, songPath, coverPath, mapArchivePath, song.mapDownloadPath)

# Process the maps.
if len(songsToProcess) == 1:
    print("Processing 1 map.")
else:
    print("Processing " + str(len(songsToProcess)) + " maps.")
processMaps(songsToProcess)

# Close the database.
database.close()