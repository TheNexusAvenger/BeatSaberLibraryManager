"""
TheNexusAvenger

Replaces the song Covers.
"""

import os
from data.MapFileSet import MapFileSet

COVERS_DIRECTORY = os.path.realpath(__file__ + "/../../../maps/Covers")
KNOWN_EXTENSIONS = ["png", "jpg", "jpeg"]


def setSongCover(mapFiles: MapFileSet) -> None:
    """Replaces the song cover of a map.

    :param mapFiles: Map to process.
    """

    # Get the cover.
    songCover = None
    extension = None
    for newExtension in KNOWN_EXTENSIONS:
        newSongCover = os.path.join(COVERS_DIRECTORY, mapFiles.getSongName(True) + "." + newExtension)
        if os.path.exists(newSongCover):
            songCover = newSongCover
            extension = newExtension
            break

    # Change the cover.
    if songCover:
        # Remove the existing file.
        # A loop is done since the casing of files can be different on Windows.
        print("\t\tReplacing album cover.")
        coverImageFilename = mapFiles.map.getCoverImageFilename()
        for coverFileName in list(mapFiles.otherFiles.keys()):
            if coverFileName.lower() == coverImageFilename:
                del mapFiles.otherFiles[coverFileName]
                break

        # Set the new file.
        mapFiles.map.setCoverImageFilename("cover." + extension)
        with open(songCover, "rb") as file:
            mapFiles.otherFiles["cover." + extension] = file.read()