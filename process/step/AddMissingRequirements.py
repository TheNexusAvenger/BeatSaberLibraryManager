"""
TheNexusAvenger

Adds mod requirements to maps if they are detected as missing.
C418 - Aria Math (Protostar Remix) is an example that is missing extension definitions.

Does not support V3.0.0 or newer map formats.
"""

from data.MapFileSet import MapFileSet


def addMissingRequirements(mapFiles: MapFileSet) -> None:
    """Adds missing mod requirements to a map.

    :param mapFiles: Map to process.
    """

    # Iterate over the difficulties.
    for mapSet in mapFiles.map._difficultyBeatmapSets:
        for difficultyData in mapSet._difficultyBeatmaps:
            # Read the map data.
            difficultyMapData = mapFiles.difficultyFiles[difficultyData._beatmapFilename]

            # Add Noodle Extensions and Chroma
            if "_customData" in difficultyMapData.keys() and "_pointDefinitions" in difficultyMapData["_customData"].keys():
                # Prepare the requirements.
                requirements = difficultyData.getCustomData("_requirements")
                if requirements is None:
                    requirements = {}

                # Add the requirements.
                if "Noodle Extensions" not in requirements:
                    print("\t\tAdding \"Noodle Extensions\" requirement.")
                    requirements.append("Noodle Extensions")
                    difficultyData.setCustomData("_requirements", requirements)
                if "Chroma" not in requirements:
                    print("\t\tAdding \"Chroma\" requirement.")
                    requirements.append("Chroma")
                    difficultyData.setCustomData("_requirements", requirements)