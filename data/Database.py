"""
TheNexusAvenger

Manages the database.
"""

import os
import sqlite3
from data import Configuration

DEFAULT_LOCATION = os.path.realpath(__file__ + "/../../database.sqlite")
DATABASE_TABLES = {
    "BeatSaverMaps": "Artist TEXT, SongName TEXT, SongSubName TEXT, Include INTEGER, Validated INTEGER, BeatSaverKey TEXT, OtherNotes Text",
    "BeatSageMaps": "Artist TEXT, SongName TEXT, SongSubName TEXT, Include INTEGER, Validated INTEGER, SongURL TEXT, CoverURL TEXT, OtherNotes Text",
}
DATABASE_TABLES_TO_SOURCE = {
    "BeatSaverMaps": "BeatSaver",
    "BeatSageMaps": "BeatSage",
}


class Database:
    def __init__(self, fileLocation=DEFAULT_LOCATION):
        """Creates the database.
        """

        self.fileLocation = fileLocation
        self.connection = sqlite3.connect(fileLocation)
        for tableName in DATABASE_TABLES.keys():
            if tableName not in DATABASE_TABLES_TO_SOURCE.keys() or Configuration.sourceEnabled(DATABASE_TABLES_TO_SOURCE[tableName]):
                self.initializeTable(tableName, DATABASE_TABLES[tableName])


    def initializeTable(self, tableName: str, tableSchema: str) -> None:
        """Initializes a table if it doesn't exist.

        :param tableName: Name of the table.
        :param tableSchema: Schema of the table.
        """

        # Get if the table exists.
        tableExists = False
        try:
            self.execute("SELECT * FROM " + tableName + ";")
            tableExists = True
        except:
            pass

        # Initialize the table.
        if not tableExists:
            print("Initializing " + tableName)
            self.execute("CREATE TABLE " + tableName + "(" + tableSchema + ");")
            self.commit()
        else:
            print("Already initialized " + tableName)


    def execute(self, query: str, parameters: list = []) -> any:
        """Executes an SQL query and returns the result.

        :param query: Query to run on the database.
        :param parameters: Parameters to use with the query.
        :return: The result of the query.
        """

        return self.connection.execute(query, parameters).fetchall()


    def commit(self) -> None:
        """Commits changes to the database.
        """

        self.connection.commit()


    def close(self) -> None:
        """Closes the database.
        """

        self.connection.close()
