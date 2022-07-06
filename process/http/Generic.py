"""
TheNexusAvenger

Generic HTTP helper methods.
"""

import requests


def downloadImage(url: str, pathWithoutExtension: str) -> str:
    """Downloads an image file.

    :param url: The URL to download from.
    :param pathWithoutExtension: The path to save to without the extension.
    :return: The path the file is saved to.
    """

    response = requests.get(url)
    path = pathWithoutExtension + "." + response.headers["Content-Type"].split("/")[1]
    with open(path, "wb") as file:
        file.write(response.content)
    return path