"""
TheNexusAvenger

Data for maps for Beat Saber.
"""

from typing import List, Optional
from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass


DEFAULT_LABELS = {
    1: "Easy",
    3: "Normal",
    5: "Hard",
    7: "Expert",
    9: "Expert+",
}


@dataclass
class CustomDataContainer:
    # _customData stored here due to _version needing to be first on Meta Quest.
    # Due to inheritance, this class's properties would appear first.

    class Meta:
        ordered = True
        unknown = EXCLUDE

    def getCustomData(self, key: any) -> any:
        """Returns the value for a custom data entry.

        :param key: Key to get.
        :return: Value of the custom data.
        """

        if self._customData and key in self._customData.keys():
            return self._customData[key]
        return None


    def setCustomData(self, key: any, value: any) -> None:
        """Sets a custom data entry.

        :param key: Key to set.
        :param value: Value to set.
        """

        if self._customData is None:
            self._customData = {}
        self._customData[key] = value


@dataclass
class BeatMap(CustomDataContainer):
    _difficulty: str
    _difficultyRank: int
    _beatmapFilename: str
    _noteJumpMovementSpeed: float
    _noteJumpStartBeatOffset: float
    _customData: Optional[dict]

    class Meta:
        ordered = True
        unknown = EXCLUDE

    def getDifficultyLabel(self) -> str:
        """Returns the difficulty label for the map.

        :return: The label for the map.
        """

        customLabel = self.getCustomData("_difficultyLabel")
        if customLabel is not None and customLabel != "":
            return customLabel
        return DEFAULT_LABELS[self._difficultyRank]


    def addDifficultyLabelModifier(self, modifier: str) -> None:
        """Adds an extra label to the difficulty label.

        :param modifier: Modifier to add.
        """

        label = self.getDifficultyLabel()
        if "▲" not in label and "▼" not in label:
            self.setCustomData("_difficultyLabel", label + modifier)


@dataclass
class BeatMapSet:
    _beatmapCharacteristicName: str
    _difficultyBeatmaps: List[BeatMap]
    _customData: Optional[dict]

    class Meta:
        ordered = True
        unknown = EXCLUDE


@dataclass
class Map(CustomDataContainer):
    _version: str
    _songName: str
    _songSubName: str
    _songAuthorName: str
    _levelAuthorName: str
    _beatsPerMinute: float
    _shuffle: int
    _shufflePeriod: float
    _previewStartTime: float
    _previewDuration: float
    _songFilename: str
    _coverImageFilename: str
    _environmentName: str
    _allDirectionsEnvironmentName: Optional[str]
    _songTimeOffset: float
    _difficultyBeatmapSets: List[BeatMapSet]
    _customData: Optional[dict]

    class Meta:
        ordered = True
        unknown = EXCLUDE