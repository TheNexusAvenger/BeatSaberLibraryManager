"""
TheNexusAvenger

Sets the song data of the map.
"""

from data.MapFileSet import MapFileSet


def setSongData(mapFiles: MapFileSet) -> None:
    """Sets the song data of the map.

    :param mapFiles: Map to process.
    """

    mapFiles.map.setSongAuthorName(mapFiles.song.artist)
    mapFiles.map.setSongName(mapFiles.song.songName)
    mapFiles.map.setSongSubName(mapFiles.song.songSubName)
