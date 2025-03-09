"""
TheNexusAvenger

Data for maps for Beat Saber.
"""

DEFAULT_LABELS = {
    1: "Easy",
    3: "Normal",
    5: "Hard",
    7: "Expert",
    9: "Expert+",
}
DIFFICULTY_RANK_LOOKUP = {
    "Easy": 1,
    "Normal": 3,
    "Hard": 5,
    "Expert": 7,
    "ExpertPlus": 9,
}


class CustomDataContainer:
    def __init__(self, data: dict):
        """Initializes the custom data container.

        :param data: Data for the custom data container.
        """

        self.data = data

    def isUnderscoreFormat(self) -> bool:
        """Returns if the keys have underscores (version <=3).

        :return: Whether the keys have underscores (version <=3).
        """

        for key in self.data.keys():
            return key.startswith("_")

    def getCustomData(self, key: any) -> any:
        """Returns the value for a custom data entry.

        :param key: Key to get.
        :return: Value of the custom data.
        """

        prefix = "_" if self.isUnderscoreFormat() else ""
        if prefix + "customData" not in self.data.keys():
            return None
        customData = self.data[prefix + "customData"]
        if customData and key in customData.keys():
            return customData[key]
        return None

    def setCustomData(self, key: any, value: any) -> None:
        """Sets a custom data entry.

        :param key: Key to set.
        :param value: Value to set.
        """

        prefix = "_" if self.isUnderscoreFormat() else ""
        if prefix + "customData" not in self.data.keys():
            self.data[prefix + "customData"] = {}
        self.data[prefix + "customData"][prefix + key] = value


class BeatMap(CustomDataContainer):
    def getBeatMapFileName(self) -> str:
        """Returns the file name of the beat map.

        :return: The file name of the beat map.
        """

        if "beatmapDataFilename" in self.data.keys():
            return self.data["beatmapDataFilename"] # >=V4 format
        return self.data["_beatmapFilename"] # <=V3 format

    def getDifficulty(self) -> str:
        """Returns the difficulty of the beat map.

        :return: The difficulty of the beat map.
        """

        if "difficulty" in self.data.keys():
            return self.data["difficulty"] # >=V4 format
        return self.data["_difficulty"] # <=V3 format

    def getDifficultyLabel(self) -> str:
        """Returns the difficulty label for the beat map.

        :return: The label for the beat map.
        """

        customLabel = self.getCustomData("difficultyLabel")
        if customLabel is not None and customLabel != "":
            return customLabel
        return DEFAULT_LABELS[self.getDifficultyRank()]

    def addDifficultyLabelModifier(self, modifier: str) -> None:
        """Adds an extra label to the difficulty label.

        :param modifier: Modifier to add.
        """

        label = self.getDifficultyLabel()
        if "▲" not in label and "▼" not in label:
            self.setCustomData("difficultyLabel", label + modifier)

    def getDifficultyRank(self) -> int:
        """Returns the difficulty rank of the beat map.

        :return: The difficulty rank of the beat map.
        """

        if "difficulty" in self.data.keys():
            return DIFFICULTY_RANK_LOOKUP[self.data["difficulty"]] # >=V4 format
        return self.data["_difficultyRank"] # <=V3 format

    def getNoteJumpMovementSpeed(self) -> float:
        """Returns the note jump movement speed of the beat map.

        :return: The note jump movement speed of the beat map.
        """

        if "noteJumpMovementSpeed" in self.data.keys():
            return self.data["noteJumpMovementSpeed"] # >=V4 format
        return self.data["_noteJumpMovementSpeed"] # <=V3 format

    def setNoteJumpMovementSpeed(self, noteJumpMovementSpeed: float) -> None:
        """Sets the note jump movement speed of the beat map.

        :param noteJumpMovementSpeed: The note jump movement speed of the beat map.
        """

        if "noteJumpMovementSpeed" in self.data.keys():
            self.data["noteJumpMovementSpeed"] = noteJumpMovementSpeed # >=V4 format
        else:
            self.data["_noteJumpMovementSpeed"] = noteJumpMovementSpeed # <=V3 format

    def getNoteJumpStartBeatOffset(self) -> float:
        """Returns the note jump start beat of the beat map.

        :return: The note jump start beat of the beat map.
        """

        if "noteJumpStartBeatOffset" in self.data.keys():
            return self.data["noteJumpStartBeatOffset"] # >=V4 format
        return self.data["_noteJumpStartBeatOffset"] # <=V3 format

    def setNoteJumpStartBeatOffset(self, noteJumpStartBeatOffset: float) -> None:
        """Sets the note jump start beat of the beat map.

        :param noteJumpStartBeatOffset: The note jump start beat of the beat map.
        """

        if "noteJumpStartBeatOffset" in self.data.keys():
            self.data["noteJumpStartBeatOffset"] = noteJumpStartBeatOffset # >=V4 format
        else:
            self.data["_noteJumpStartBeatOffset"] = noteJumpStartBeatOffset # <=V3 format

class BeatMapSet(CustomDataContainer):
    def __init__(self, data: dict):
        """Initializes the beat map set.

        :param data: Data for the beat map set.
        """

        super().__init__(data)

        # Load the difficulty maps.
        self.difficultyBeatmaps = []
        if "_difficultyBeatmaps" in self.data.keys():
            for beatmap in self.data["_difficultyBeatmaps"]:
                self.difficultyBeatmaps.append(BeatMap(beatmap))

    def getBeatmapCharacteristicName(self) -> None:
        """Returns the characteristic name of the map set.

        :return: The characteristic name of the map set.
        """

        if "characteristic" in self.data.keys():
            return self.data["characteristic"] # >=V4 format
        return self.data["_beatmapCharacteristicName"] # <=V3 format

    def removeMap(self, beatmap: BeatMap) -> None:
        """Removes a map from the map set.

        :param map: Map to remove.
        """

        self.difficultyBeatmaps.remove(beatmap)
        self.data["_difficultyBeatmaps"].remove(beatmap.data)


class Map(CustomDataContainer):
    def __init__(self, data: dict):
        """Initializes the map.

        :param data: Data for the map.
        """

        super().__init__(data)

        # Load the difficulty sets.
        self.difficultyBeatmapSets = []
        if "_difficultyBeatmapSets" in self.data.keys():
            # <=V3 format
            for mapSet in self.data["_difficultyBeatmapSets"]:
                self.difficultyBeatmapSets.append(BeatMapSet(mapSet))
        else:
            # >=V4 format
            mapSets = {}
            for beatmap in self.data["difficultyBeatmaps"]:
                characteristic = beatmap["characteristic"]
                if characteristic not in mapSets.keys():
                    mapSets[characteristic] = BeatMapSet(beatmap)
                    self.difficultyBeatmapSets.append(mapSets[characteristic])
                mapSets[characteristic].difficultyBeatmaps.append(BeatMap(beatmap))

    def getBeatsPerMinute(self) -> float:
        """Returns the beats per minute of the map.

        :return: The beats per minute of the map.
        """

        if "audio" in self.data.keys():
            return self.data["audio"]["bpm"] # >=V4 format
        return self.data["_beatsPerMinute"] # <=V3 format

    def getCoverImageFilename(self) -> str:
        """Returns the cover image filename.

        :return: The cover image filename.
        """

        if "coverImageFilename" in self.data.keys():
            return self.data["coverImageFilename"] # >=V4 format
        return self.data["_coverImageFilename"] # <=V3 format

    def setCoverImageFilename(self, coverImageFilename: str) -> None:
        """Sets the cover image filename.

        :param coverImageFilename: Name of the cover image filename.
        """

        if "coverImageFilename" in self.data.keys():
            self.data["coverImageFilename"] = coverImageFilename # >=V4 format
        else:
            self.data["_coverImageFilename"] = coverImageFilename # <=V3 format

    def prefixLevelAuthorName(self, levelAuthorNamePrefix: str) -> None:
        """Prefixes the level author name.

        :param levelAuthorNamePrefix: Prefix of the leve author name to add.
        """

        if "difficultyBeatmaps" in self.data.keys():
            # >=V4 format
            for difficultyBeatmap in self.data["difficultyBeatmaps"]:
                difficultyBeatmap["beatmapAuthors"]["mappers"][0] = levelAuthorNamePrefix + difficultyBeatmap["beatmapAuthors"]["mappers"][0]
        else:
            self.data["_levelAuthorName"] = levelAuthorNamePrefix + self.data["_levelAuthorName"] # <=V3 format

    def setSongAuthorName(self, songAuthorName: str) -> None:
        """Sets the name of the song author.

        :param songAuthorName: Name of the song author.
        """

        if "song" in self.data.keys():
            self.data["song"]["author"] = songAuthorName # >=V4 format
        else:
            self.data["_songAuthorName"] = songAuthorName # <=V3 format

    def setSongName(self, songName: str) -> None:
        """Sets the name of the song name.

        :param songName: Name of the song.
        """

        if "song" in self.data.keys():
            self.data["song"]["title"] = songName # >=V4 format
        else:
            self.data["_songName"] = songName # <=V3 format

    def setSongSubName(self, songSubName: str) -> None:
        """Sets the name of the song sub name.

        :param songSubName: Sub name of the song.
        """

        if "song" in self.data.keys():
            self.data["song"]["subTitle"] = songSubName # >=V4 format
        else:
            self.data["_songSubName"] = songSubName # <=V3 format
