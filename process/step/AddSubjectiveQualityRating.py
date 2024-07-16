"""
TheNexusAvenger

Adds subjective quality ratings to the level author name information.
"""

from data.MapFileSet import MapFileSet

def addSubjectiveQualityRating(mapFiles: MapFileSet) -> None:
    """Clamps the speed of maps.

    :param mapFiles: Map to process.
    """

    # Return if the rating is not provided.
    subjectiveQualityRating = mapFiles.song.subjectiveQualityRating
    if subjectiveQualityRating is None or subjectiveQualityRating == "":
        print("\t\tMap has no subjective quality rating.")
        return

    # Add the subjective quality rating.
    print("\t\tAdding subjective quality rating \"" + subjectiveQualityRating + "\".")
    mapFiles.map._levelAuthorName = "[" + subjectiveQualityRating + "] " + mapFiles.map._levelAuthorName