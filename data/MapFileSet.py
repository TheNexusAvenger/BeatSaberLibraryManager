"""
TheNexusAvenger

Set of files that make up a map.
"""

import json
import os
from data.Map import Map
from data.Song import Song
from typing import Dict, Optional, Union
from zipfile import ZipFile


def removeNullValues(dictionary: Union[dict, list]) -> None:
    """Removes null values from a given dictionary.
    This is done recursively.

    :param dictionary: Dictionary to remove null values from.
    """

    if type(dictionary) is dict:
        for key in list(dictionary.keys()):
            if dictionary[key] is None:
                del dictionary[key]
            elif type(dictionary[key]) is dict or type(dictionary[key]) is list:
                removeNullValues(dictionary[key])
    elif type(dictionary) is list:
        for entry in list(dictionary):
            removeNullValues(entry)


class MapFileSet:
    targetDirectory: str
    map: Map
    song: Song
    difficultyFiles: Dict[str, dict]
    otherFiles: Dict[str, bytes]


    def __init__(self):
        """Creates the map file set.
        """

        self.targetParentDirectory = None
        self.difficultyFiles = {}
        self.otherFiles = {}


    def getMapName(self) -> str:
        """Returns the map name for the map.

        :return: The map name for the map.
        """

        return os.path.basename(self.targetParentDirectory)


    def getSongName(self, fileEscaped: bool = False) -> str:
        """Returns the name of the song for the map.

        :return: The name of the song for the map.
        """

        return self.song.getSongName(fileEscaped)


    def loadFiles(self) -> None:
        """Loads the files from the otherFiles.
        """

        # Determine the info file.
        # The caps can vary.
        infoFileName = None
        for fileName in self.otherFiles.keys():
            if fileName.lower() == "info.dat":
                infoFileName = fileName
                break
        if infoFileName is None:
            raise AssertionError("Info.dat file not found.")

        # Read the info file.
        self.map = Map.Schema().loads(self.otherFiles[infoFileName].decode("utf8"))
        del self.otherFiles[infoFileName]

        # Read the difficulty maps.
        for mapSet in self.map._difficultyBeatmapSets:
            for difficultyMap in mapSet._difficultyBeatmaps:
                difficultyFileName = difficultyMap._beatmapFilename
                if difficultyFileName in self.otherFiles.keys():
                    self.difficultyFiles[difficultyFileName] = json.loads(self.otherFiles[difficultyFileName])
                    del self.otherFiles[difficultyFileName]


    def write(self) -> None:
        """Writes the map to the file system.
        """

        # Write the info file.
        self.writeJsonFile("Info.dat", Map.Schema().dump(self.map), indent=4)

        # Write the difficulty files.
        # Spaces are removed due to difficulties with loading maps in unmodded versions.
        for fileName in self.difficultyFiles.keys():
            self.writeJsonFile(fileName, self.difficultyFiles[fileName], separators=(",", ":"))

        # Write the other files.
        for fileName in self.otherFiles.keys():
            self.writeFile(fileName, self.otherFiles[fileName])


    def writeJsonFile(self, fileName: str, data: Union[dict, list], indent=None, separators: Optional[tuple] = None) -> None:
        """Writes a JSON file for the map.
        JSON files require a special case since the serialization order is random.

        :param fileName: File name to write.
        :param data: Data to write to the file.
        :param separators: Separators to use when serializing JSON.
        :param indent: Indenting to use with the JSON.
        """

        # Create the parent directory.
        if not os.path.exists(self.targetParentDirectory):
            os.makedirs(self.targetParentDirectory)

        # Return if the file contents are the same.
        # For syncing files between systems, this prevents constantly overwriting files that don't change.
        removeNullValues(data)
        filePath = os.path.join(self.targetParentDirectory, fileName)
        if os.path.exists(filePath):
            with open(filePath, "rb") as file:
                if json.loads(file.read()) == data:
                    return

        # Write the file.
        with open(filePath, "w", encoding="utf8") as file:
            file.write(json.dumps(data, indent=indent, separators=separators, ensure_ascii=False))


    def writeFile(self, fileName: str, data: bytes) -> None:
        """Writes a file for the map.

        :param fileName: File name to write.
        :param data: Data to write to the file.
        """

        # Create the parent directory.
        if not os.path.exists(self.targetParentDirectory):
            os.makedirs(self.targetParentDirectory)

        # Return if the file contents are the same.
        # For syncing files between systems, this prevents constantly overwriting files that don't change.
        filePath = os.path.join(self.targetParentDirectory, fileName)
        if os.path.exists(filePath):
            with open(filePath, "rb") as file:
                if file.read() == data:
                    return

        # Write the file.
        with open(filePath, "wb") as file:
            file.write(data)


def loadMapFromDirectory(song: Song, targetParentDirectory: str) -> MapFileSet:
    """Loads a map file from a directory.

    :param song: Song entry to process.
    :param targetParentDirectory: Parent directory to save the map to.
    """

    fileSet = MapFileSet()
    fileSet.song = song
    for fileName in os.listdir(song.mapDownloadPath):
        with open(os.path.join(song.mapDownloadPath, fileName), "rb") as file:
            fileSet.otherFiles[fileName] = file.read()
    fileSet.loadFiles()
    fileSet.targetParentDirectory = os.path.join(targetParentDirectory, os.path.basename(song.mapDownloadPath).replace(".zip", ""))
    return fileSet


def loadMapFromZip(song: Song, targetParentDirectory: str) -> MapFileSet:
    """Loads a map file from a ZIP file.

    :param song: Song entry to process.
    :param targetParentDirectory: Parent directory to save the map to.
    """

    with ZipFile(song.mapDownloadPath) as file:
        fileSet = MapFileSet()
        fileSet.song = song
        for fileName in file.namelist():
            fileSet.otherFiles[fileName] = file.read(fileName)
        fileSet.loadFiles()
        fileSet.targetParentDirectory = os.path.join(targetParentDirectory, os.path.basename(song.mapDownloadPath).replace(".zip", ""))
        return fileSet


def loadMap(song: Song, targetParentDirectory: str) -> MapFileSet:
    """Loads a map file or directory.

    :param song: Song entry to process.
    :param targetParentDirectory: Parent directory to save the map to.
    """

    if os.path.isdir(song.mapDownloadPath):
        return loadMapFromDirectory(song, targetParentDirectory)
    elif song.mapDownloadPath.endswith(".zip"):
        return loadMapFromZip(song, targetParentDirectory)
    else:
        raise AssertionError("Supplied source path is not a directory or a ZIP file.")
