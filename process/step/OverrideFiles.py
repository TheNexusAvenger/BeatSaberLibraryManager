"""
TheNexusAvenger

Overrides map files.
"""

import json
import os
from data.Map import Map
from data.MapFileSet import MapFileSet


def overrideFiles(mapFiles: MapFileSet) -> None:
    """Adds missing mod requirements to a map.

    :param mapFiles: Map to process.
    """

    # Return if there are no overrides.
    mapDownloadFile = os.path.basename(mapFiles.song.mapDownloadPath)
    if mapDownloadFile.endswith(".zip"):
        mapDownloadFile = mapDownloadFile.replace(".zip", "")
    overridesDirectory = os.path.realpath(os.path.join(__file__, "..", "..", "..", "maps", "Overrides", mapDownloadFile))
    if not os.path.exists(overridesDirectory):
        return

    # List the files.
    fileNames = os.listdir(overridesDirectory)
    for fileName in fileNames:
        if fileName.lower() == "info.dat":
            fileNames.remove(fileName)
            fileNames.insert(0, fileName)

    # Override the files.
    for fileName in fileNames:
        if fileName.lower() == "info.dat":
            print("\t\tOverriding info.dat file.")
            with open(os.path.join(overridesDirectory, fileName), encoding="utf8") as file:
                mapFiles.map = Map(json.loads(file.read()))
        elif fileName in mapFiles.difficultyFiles.keys():
            print("\t\tOverriding difficulty file " + fileName)
            with open(os.path.join(overridesDirectory, fileName), encoding="utf8") as file:
                mapFiles.difficultyFiles[fileName] = json.loads(file.read())
        else:
            isNewMapFile = False
            for mapSet in mapFiles.map.difficultyBeatmapSets:
                for difficultyMap in mapSet.difficultyBeatmaps:
                    if fileName == difficultyMap.getBeatMapFileName():
                        isNewMapFile = True
                        break

            if isNewMapFile:
                print("\t\tAdding difficulty file " + fileName)
                with open(os.path.join(overridesDirectory, fileName), encoding="utf8") as file:
                    mapFiles.difficultyFiles[fileName] = json.loads(file.read())
            else:
                print("\t\tOverriding other file " + fileName)
                with open(os.path.join(overridesDirectory, fileName), "rb") as file:
                    mapFiles.otherFiles[fileName] = file.read()
