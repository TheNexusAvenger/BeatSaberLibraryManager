"""
TheNexusAvenger

Removes non-lightshow maps that have no notes.
"""

from data.MapFileSet import MapFileSet

LEVEL_TYPE_TO_IGNORE = ["Lightshow"]


def removeEmptyMaps(mapFiles: MapFileSet) -> None:
    """Removes non-lightshow maps that have no notes.

    :param mapFiles: Map to process.
    """

    # Iterate over the difficulty sets.
    for mapSet in mapFiles.map.difficultyBeatmapSets:
        beatmapCharacteristicName = mapSet.getBeatmapCharacteristicName()
        if beatmapCharacteristicName not in LEVEL_TYPE_TO_IGNORE:
            # Get the difficulties to remove.
            difficultiesToRemove = []
            for difficultyData in mapSet.difficultyBeatmaps:
                # Add the difficulty if the map has no notes.
                difficultyMapData = mapFiles.difficultyFiles[difficultyData.getBeatMapFileName()]
                if "colorNotes" in difficultyMapData.keys():
                    if len(difficultyMapData["colorNotes"]) == 0:
                        difficultiesToRemove.append(difficultyData)
                else:
                    if len(difficultyMapData["_notes"]) == 0:
                        difficultiesToRemove.append(difficultyData)

            # Remove the difficulties.
            for difficultyData in difficultiesToRemove:
                print("\t\tRemoving " + beatmapCharacteristicName + " difficulty " + difficultyData.getDifficulty() + " (has no notes)")
                mapSet.removeMap(difficultyData)
