"""
TheNexusAvenger

Clamps the reaction time of maps.
Math from: https://github.com/zeph-yr/JDFixer/blob/BS_1.20/BeatmapUtils.cs
"""

from data.Configuration import getConfiguration
from data.MapFileSet import MapFileSet

CLAMPED_REACTION_TIMES = getConfiguration("ClampedReactionTimes", {})


def calculatePreOffsetHalfJumpDistance(bpm: float, njs: float) -> float:
    """Calculates the Half Jump Distance without the offset of a map.

    :param bpm: Beats Per Minute of the song.
    :param njs: Note Jump Speed of the map.
    :return: Half Jump Distance of the map.
    """

    halfJump = 4
    num = 60 / bpm

    while njs * num * halfJump > 17.999:
        halfJump = halfJump / 2
    return halfJump


def calculateJumpDistance(bpm: float, njs: float, offset: float) -> float:
    """Calculates the Jump Distance of a map.

    :param bpm: Beats Per Minute of the song.
    :param njs: Note Jump Speed of the map.
    :param offset: Jump distance offset of the map.
    :return: Half Jump Distance of the map.
    """

    halfJump = calculatePreOffsetHalfJumpDistance(bpm, njs)
    num = 60 / bpm

    halfJump += offset
    if halfJump < 0.25:
        halfJump = 0.25

    jumpDistance = njs * num * halfJump * 2
    return jumpDistance


def calculateReactionTime(jd: float, njs: float) -> float:
    """Calculates the reaction time for a map.

    :param jd: Jump Distance of the map.
    :param njs: Note Jump Speed of the map.
    :return: Reaction Time of the map in milliseconds.
    """

    return jd / (2 * njs) * 1000


def calculateDesiredJumpDistance(reactionTime: float, njs: float) -> float:
    """Calculates the Jump Distance for a map to get a desired Reaction Time.

    :param reactionTime: Reaction Time of the map in milliseconds.
    :param njs: Note Jump Speed of the map.
    :return: Jump Distance of the map.
    """

    return reactionTime * ((2 * njs) / 1000)


def calculateDesiredOffset(bpm: float, jd: float, njs: float) -> float:
    """Calculates the offset for a map.

    :param bpm: Beats Per Minute of the song.
    :param jd: Jump Distance of the map.
    :param njs: Note Jump Speed of the map.
    :return: Offset of the map.
    """

    halfJump = calculatePreOffsetHalfJumpDistance(bpm, njs)
    num = 60 / bpm
    return (jd / (njs * num * 2)) - halfJump


def clampReactionTimes(mapFiles: MapFileSet) -> None:
    """Clamps the reaction time of maps.

    :param mapFiles: Map to process.
    """

    # Iterate over the difficulties.
    for mapSet in mapFiles.map._difficultyBeatmapSets:
        for difficultyData in mapSet._difficultyBeatmaps:
            if str(difficultyData._difficultyRank) in CLAMPED_REACTION_TIMES.keys():
                # Clamp the reaction times.
                reactionTimeConstraints = CLAMPED_REACTION_TIMES[str(difficultyData._difficultyRank)]
                mapReactionTime = calculateReactionTime(calculateJumpDistance(mapFiles.map._beatsPerMinute, difficultyData._noteJumpMovementSpeed, difficultyData._noteJumpStartBeatOffset), difficultyData._noteJumpMovementSpeed)
                if "Minimum" in reactionTimeConstraints.keys() and mapReactionTime < reactionTimeConstraints["Minimum"]:
                    print("\t\tIncreasing the Reaction Time of " + difficultyData.getDifficultyLabel() + " from " + str(mapReactionTime) + " ms to " + str(reactionTimeConstraints["Minimum"]) + " ms")
                    difficultyData._noteJumpStartBeatOffset = calculateDesiredOffset(mapFiles.map._beatsPerMinute, calculateDesiredJumpDistance(reactionTimeConstraints["Minimum"], difficultyData._noteJumpMovementSpeed), difficultyData._noteJumpMovementSpeed)
                    difficultyData.addDifficultyLabelModifier("▼")
                elif "Maximum" in reactionTimeConstraints.keys() and mapReactionTime > reactionTimeConstraints["Maximum"]:
                    print("\t\tDecreasing the Reaction Time of " + difficultyData.getDifficultyLabel() + " from " + str(mapReactionTime) + " to " + str(reactionTimeConstraints["Maximum"]) + " ms")
                    difficultyData._noteJumpStartBeatOffset = calculateDesiredOffset(mapFiles.map._beatsPerMinute, calculateDesiredJumpDistance(reactionTimeConstraints["Maximum"], difficultyData._noteJumpMovementSpeed), difficultyData._noteJumpMovementSpeed)
                    difficultyData.addDifficultyLabelModifier("▲")
