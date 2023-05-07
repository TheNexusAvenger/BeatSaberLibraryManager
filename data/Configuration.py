"""
TheNexusAvenger

Loads the configuration from the file system.
"""

import json
import os

CONFIGURATION_LOCATION = os.path.realpath(os.path.join(__file__, "..", "..", "configuration.json"))
DEFAULT_CONFIGURATION = {
    "ClampedMapSpeeds": {
        "5": {
            "Minimum": 17,
            "Maximum": 19,
        },
        "7": {
            "Minimum": 17,
            "Maximum": 19,
        },
        "9": {
            "Minimum": 18,
            "Maximum": 20,
        },
    },
    "ClampedReactionTimes": {
        "5": {
            "Minimum": 600,
            "Maximum": 750,
        },
        "7": {
            "Minimum": 600,
            "Maximum": 700,
        },
        "9": {
            "Minimum": 600,
            "Maximum": 700,
        },
    },
    "EnabledSources": [
        "BeatSaver",
        "BeatSage"
    ]
}


# Load the configuration.
if not os.path.exists(CONFIGURATION_LOCATION):
    with open(CONFIGURATION_LOCATION, "w") as file:
        file.write(json.dumps(DEFAULT_CONFIGURATION, indent=4))
with open(CONFIGURATION_LOCATION) as file:
    configuration = json.loads(file.read())


def getConfiguration(key: str, default: any) -> any:
    """Gets a value in the configuration.

    :param key: Key of the configuration to get.
    :param default: Default value to return if the key is undefined.
    :return: The value for the configuration entry.
    """

    if key not in configuration.keys():
        return default
    return configuration[key]


def sourceEnabled(source: str) -> bool:
    """Returns if a map source is enabled.

    :param source: Source of the maps.
    :return: If the source is enabled.
    """

    if "EnabledSources" not in configuration.keys():
        return True
    return source in configuration["EnabledSources"]
