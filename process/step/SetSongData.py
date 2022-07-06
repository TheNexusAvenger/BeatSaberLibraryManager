"""
TheNexusAvenger

Sets the song data of the map.
"""

from data.MapFileSet import MapFileSet


def setSongData(mapFiles: MapFileSet) -> None:
    """Sets the song data of the map.

    :param mapFiles: Map to process.
    """

    mapFiles.map._songAuthorName = mapFiles.song.artist
    mapFiles.map._songName = mapFiles.song.songName
    mapFiles.map._songSubName = mapFiles.song.songSubName