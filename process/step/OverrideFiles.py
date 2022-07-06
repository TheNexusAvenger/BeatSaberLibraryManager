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
    overridesDirectory = os.path.realpath(os.path.join(__file__, "..", "..", "..", "maps", "Overrides", os.path.basename(mapFiles.song.mapDownloadPath).split(".")[0]))
    if not os.path.exists(overridesDirectory):
        return

    # Override the files.
    for fileName in os.listdir(overridesDirectory):
        if fileName.lower() == "info.dat":
            print("\t\tOverriding info.dat file.")
            with open(os.path.join(overridesDirectory, fileName), encoding="utf8") as file:
                mapFiles.map = Map.Schema().loads(file.read())
        elif fileName in mapFiles.difficultyFiles.keys():
            print("\t\tOverriding difficulty file " + fileName)
            with open(os.path.join(overridesDirectory, fileName), encoding="utf8") as file:
                mapFiles.difficultyFiles[fileName] = json.loads(file.read())
        else:
            print("\t\tOverriding other file " + fileName)
            with open(os.path.join(overridesDirectory, fileName), "rb") as file:
                mapFiles.otherFiles[fileName] = file.read()
