"""
TheNexusAvenger

Processes maps files with additional modifiers.
"""

import os
import shutil
from data.MapFileSet import loadMap
from data.Song import Song
from process.step.AddMissingRequirements import addMissingRequirements
from process.step.AddSimpleLightShows import addSimpleLightShows
from process.step.AddSubjectiveQualityRating import addSubjectiveQualityRating
from process.step.ClampMapSpeeds import clampMapSpeeds
from process.step.ClampReactionTimes import clampReactionTimes
from process.step.OverrideFiles import overrideFiles
from process.step.RemoveEmptyMaps import removeEmptyMaps
from process.step.SetSongCover import setSongCover
from process.step.SetSongData import setSongData
from typing import List


BEATSAVER_PROCESS_STEPS = [
    overrideFiles,
    setSongData,
    addMissingRequirements,
    removeEmptyMaps,
    addSimpleLightShows,
    setSongCover,
    addSubjectiveQualityRating,
    clampMapSpeeds,
    clampReactionTimes,
]
BEAT_SAGE_PROCESS_STEPS = [
    overrideFiles,
    setSongData,
    addMissingRequirements,
    # removeEmptyMapsExtension, # Beat Sage does not have empty maps.
    addSimpleLightShows,
    setSongCover,
    addSubjectiveQualityRating,
    clampMapSpeeds,
    clampReactionTimes,
]
BASE_PATH = os.path.realpath(os.path.join(__file__, "..", "..", "maps"))
VALIDATED_MAPS_PATH = os.path.join(BASE_PATH, "Maps")
UNVALIDATED_MAPS_PATH = os.path.join(BASE_PATH, "UnvalidatedMaps")


def processMap(song: Song, targetParentDirectory: str, processSteps: list) -> None:
    """Processes a map.

    :param song: Song entry to process.
    :param targetParentDirectory: Target parent directory to save to.
    :param processSteps: Steps to apply to the map.
    """

    mapFiles = loadMap(song, targetParentDirectory)
    print("\tProcessing " + os.path.basename(song.mapDownloadPath))
    for processStep in processSteps:
        processStep(mapFiles)
    mapFiles.write()


def processMaps(songs: List[Song]) -> None:
    """Processes a list of maps.

    :param songs: Songs to process.
    """

    # Create the directories.
    if not os.path.exists(VALIDATED_MAPS_PATH):
        os.makedirs(VALIDATED_MAPS_PATH)
    if not os.path.exists(UNVALIDATED_MAPS_PATH):
        os.makedirs(UNVALIDATED_MAPS_PATH)

    # Process the maps.
    validatedMapFiles = []
    unvalidatedMapFiles = []
    for song in songs:
        if song.validated is not True:
            targetParentDirectory = UNVALIDATED_MAPS_PATH
            unvalidatedMapFiles.append(os.path.basename(song.mapDownloadPath).replace(".zip", ""))
        else:
            targetParentDirectory = VALIDATED_MAPS_PATH
            validatedMapFiles.append(os.path.basename(song.mapDownloadPath).replace(".zip", ""))
        if song.mapSource == "BeatSaver":
            processMap(song, targetParentDirectory, BEATSAVER_PROCESS_STEPS)
        elif song.mapSource == "BeatSage":
            processMap(song, targetParentDirectory, BEAT_SAGE_PROCESS_STEPS)

    # Clear the files that no longer exist.
    for mapDirectorySet in [{"path": VALIDATED_MAPS_PATH, "maps": validatedMapFiles}, {"path": UNVALIDATED_MAPS_PATH, "maps": unvalidatedMapFiles}]:
        mapDirectoryPath = mapDirectorySet["path"]
        mapFiles = mapDirectorySet["maps"]
        for fileName in os.listdir(mapDirectoryPath):
            if fileName not in mapFiles:
                filePath = os.path.join(mapDirectoryPath, fileName)
                if os.path.isdir(filePath):
                    shutil.rmtree(filePath)
