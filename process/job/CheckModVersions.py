"""
TheNexusAvenger

Determines if the mods for the current Beat Saber version exist.
"""

import re
import requests

# Host for the mods.
BEATMODS_HOST = "https://beatmods.com"

# Non-default mods required for the current suite of maps.
REQUIRED_MODS = [
    "MappingExtensions",
    "NoodleExtensions",
    "Chroma",
]


# Get the script that contains the versions.
print("Determining versions.")
page = requests.get(BEATMODS_HOST).text
scriptLocations = re.findall(r"src=\"(\/js\/[^\"]+)\"", page)

if len(scriptLocations) == 0:
    print("Failed to find script containing versions. Exiting.")
    exit(-1)
elif len(scriptLocations) > 1:
    print("Failed to find single script containing versions (found multiple). Exiting.")
    exit(-1)

# Get the list of versions.
pageScript = requests.get(BEATMODS_HOST + scriptLocations[0]).text
gameVersions = re.findall(r"gameVersions:\[([^\]]+)\]", pageScript)

if len(gameVersions) == 0:
    print("Failed to find versions in the page script. Exiting.")
    exit(-1)

# Parse the list of versions.
versions = re.findall(r"([\d\.]+)", gameVersions[0])
if len(versions) == 0:
    print("No versions found. Exiting.")
    exit(-1)
print("Game versions: " + ", ".join(versions))
latestVersion = versions[0]
print("\tAssuming latest version: " + latestVersion)

# Fetch the mods.
mods = requests.get(BEATMODS_HOST + "/api/v1/mod?search=&status=approved&gameVersion=" + latestVersion + "&sort=&sortDirection=1").json()
modsList = []
for mod in mods:
    modsList.append(mod["name"])
print("Mods for version " + latestVersion + ": " + ", ".join(modsList))

# Check for the required mods existing.
missingMods = 0
print("Checking mods.")
for requiredMod in REQUIRED_MODS:
    if requiredMod in modsList:
        print("\tMod " + requiredMod + " found for the current version.")
    else:
        print("\tMod " + requiredMod + " NOT found for the current version.")
        missingMods += 1

# Exit with a code -1 if mods are missing.
if missingMods > 0:
    print("Mods are missing. Exiting.")
    exit(-1)
