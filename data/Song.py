"""
TheNexusAvenger

Song entry stored in the database.
"""

from typing import Optional


class Song:
    artist: str
    songName: str
    songSubName: str
    mapSource: str
    mapDownloadPath: str
    validated: bool
    beatSaverKey: Optional[str]
    songUrl: Optional[str]
    coverUrl: Optional[str]

    def getSongName(self, fileEscaped: bool = False) -> str:
        """Returns the name of the song for the map.

        :return: The name of the song for the map.
        """

        name = self.artist + " - " + self.songName
        if self.songSubName is not None and self.songSubName != "":
            name += " " + self.songSubName
        if fileEscaped:
            name = name.replace("/", "_").replace("\\", "_").replace(":", "_")
        return name
