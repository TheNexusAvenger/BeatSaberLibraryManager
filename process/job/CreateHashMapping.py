"""
TheNexusAvenger

Creates a mapping between custom map hashes and BeatSaver map hashes.
"""

import hashlib
import json
import os
from zipfile import ZipFile


def getMapFiles(filePath: str) -> dict[str, bytes]:
    """Reads a directory or zip file map.

    :param filePath: Path of the file to read (directory or zip file).
    :return: Dictionary of the data files with their contents.
    """

    # Read the .dat files.
    fileData = {}
    if os.path.isdir(filePath):
        # Read the map files for a folder map.
        for fileName in os.listdir(filePath):
            if not fileName.endswith(".dat"):
                continue
            with open(os.path.join(filePath, fileName), "rb") as file:
                fileData[fileName.lower()] = file.read()
    else:
        # Read the map files for a ZIP file.
        with ZipFile(filePath) as file:
            for fileName in file.namelist():
                if not fileName.endswith(".dat"):
                    continue
                fileData[fileName.lower()] = file.read(fileName)

    # Return the files.
    return fileData


def calculateMapHash(filePath: str) -> str:
    """Calculates the hash of a directory or zip map.

    :param filePath: Path of the map.
    :return: Hash of the map.
    """

    # Read the info file.
    mapFiles = getMapFiles(filePath)
    mapInfo = json.loads(mapFiles["info.dat"].decode("utf8"))

    # Hash the info file.
    sha1 = hashlib.sha1()
    sha1.update(mapFiles["info.dat"])

    # Hash the difficulty maps.
    if "_difficultyBeatmapSets" in mapInfo.keys():
        # Handle V3 and older maps.
        for difficultyBeatmapSets in mapInfo["_difficultyBeatmapSets"]:
            for difficultyBeatmap in difficultyBeatmapSets["_difficultyBeatmaps"]:
                sha1.update(mapFiles[difficultyBeatmap["_beatmapFilename"].lower()])
    else:
        # Handle V4 and newer maps.
        if "audioDataFilename" in mapInfo["audio"].keys():
            sha1.update(mapFiles[mapInfo["audio"]["audioDataFilename"].lower()])
        for difficultyBeatmap in mapInfo["difficultyBeatmaps"]:
            if "beatmapDataFilename" in difficultyBeatmap.keys():
                sha1.update(mapFiles[difficultyBeatmap["beatmapDataFilename"].lower()])
            if "lightshowDataFilename" in difficultyBeatmap.keys():
                sha1.update(mapFiles[difficultyBeatmap["lightshowDataFilename"].lower()])

    # Hash the map files.
    return sha1.hexdigest()


# Create the hash mapping.
mapHashes = {}
mapsPath = os.path.realpath(os.path.join(__file__, "..", "..", "..", "maps"))
for mapDirectoryName in ["Maps", "UnvalidatedMaps"]:
    mapDirectory = os.path.join(mapsPath, mapDirectoryName)
    if not os.path.exists(mapDirectory):
        continue

    # Add the hashes for the maps.
    print("Generating hashes for " + mapDirectoryName)
    for mapName in os.listdir(mapDirectory):
        mapFilePath = os.path.join(mapDirectory, mapName)
        mapDownloadFilePath = os.path.join(mapsPath, "Downloads", "BeatSaver", mapName + ".zip")
        if not os.path.exists(mapDownloadFilePath):
            continue
        mapHashes[calculateMapHash(mapFilePath)] = calculateMapHash(mapDownloadFilePath)

# Store the hashes.
with open(os.path.join(mapsPath, "Maps", "hashes.json"), "w") as file:
    file.write(json.dumps(mapHashes, indent=4))
