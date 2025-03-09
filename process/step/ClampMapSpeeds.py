"""
TheNexusAvenger

Clamps the speed of maps.
"""

from data.Configuration import getConfiguration
from data.MapFileSet import MapFileSet

CLAMPED_MAP_SPEEDS = getConfiguration("ClampedMapSpeeds", {})


def clampMapSpeeds(mapFiles: MapFileSet) -> None:
    """Clamps the speed of maps.

    :param mapFiles: Map to process.
    """

    # Iterate over the difficulties.
    for mapSet in mapFiles.map.difficultyBeatmapSets:
        for difficultyData in mapSet.difficultyBeatmaps:
            difficultyRank = difficultyData.getDifficultyRank()
            if str(difficultyRank) in CLAMPED_MAP_SPEEDS.keys():
                # Clamp the speed.
                speedConstraints = CLAMPED_MAP_SPEEDS[str(difficultyRank)]
                mapSpeed = difficultyData.getNoteJumpMovementSpeed()
                if "Minimum" in speedConstraints.keys() and mapSpeed < speedConstraints["Minimum"]:
                    print("\t\tIncreasing the Note Jump Speed of " + difficultyData.getDifficultyLabel() + " from " + str(mapSpeed) + " to " + str(speedConstraints["Minimum"]))
                    difficultyData.setNoteJumpMovementSpeed(speedConstraints["Minimum"])
                    difficultyData.addDifficultyLabelModifier("▲")
                elif "Maximum" in speedConstraints.keys() and mapSpeed > speedConstraints["Maximum"]:
                    print("\t\tDecreasing the Note Jump Speed of " + difficultyData.getDifficultyLabel() + " from " + str(mapSpeed) + " to " + str(speedConstraints["Maximum"]))
                    difficultyData.setNoteJumpMovementSpeed(speedConstraints["Maximum"])
                    difficultyData.addDifficultyLabelModifier("▼")
