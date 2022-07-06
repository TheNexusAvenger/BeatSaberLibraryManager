"""
TheNexusAvenger

Adds simple light shows if there is no events.
"""

from data.MapFileSet import MapFileSet


def addSimpleLightShows(mapFiles: MapFileSet) -> None:
    """Clamps the speed of maps.

    :param mapFiles: Map to process.
    """

    for mapDataName in mapFiles.difficultyFiles.keys():
        # Return if V3 maps are detected.
        mapData = mapFiles.difficultyFiles[mapDataName]
        if "colorNotes" in mapData:
            print("\t\tVersion 3 map format detected for " + mapDataName + ", which is unsupported by AddSimpleLightShows.")
            continue

        # Return if there are events already.
        if len(mapData["_events"]) != 0:
            continue

        # Process the notes.
        print("\t\tAdding a simple light show to " + mapDataName)
        processedNotes = []
        lastMainLightsRed = False
        eventGroups = []
        for note in mapData["_notes"]:
            # Ignore the note if it was processed.
            if note in processedNotes or not (note["_type"] == 0 or note["_type"] == 1):
                continue

            # Determine the notes at the time.
            notesAtTime = []
            for otherNote in mapData["_notes"]:
                if note["_time"] == otherNote["_time"] and (otherNote["_type"] == 0 or otherNote["_type"] == 1):
                    notesAtTime.append(otherNote)

            # Determine the types for each column.
            totalTypes = []
            typesPerColumn = [[], [], [], []]
            for noteAtTime in notesAtTime:
                column = typesPerColumn[noteAtTime["_lineIndex"]]
                if noteAtTime["_type"] not in column:
                    column.append(noteAtTime["_type"])
                if noteAtTime["_type"] not in totalTypes:
                    totalTypes.append(noteAtTime["_type"])

            # Determine the first column with notes.
            firstColumn = 0
            columnsWithNotes = []
            for i in range(0, len(typesPerColumn)):
                if len(typesPerColumn[i]) != 0:
                    firstColumn = i
                    break
            for column in typesPerColumn:
                if len(column) != 0:
                    columnsWithNotes.append(column)

            # Add the lights.
            timeEvents = []
            eventGroups.append(timeEvents)
            eventTime = note["_time"]
            if len(totalTypes) == 1:
                noteType = totalTypes[0] == 0 and 7 or 3
                if len(columnsWithNotes) == 1:
                    if firstColumn == 0 or firstColumn == 1:
                        timeEvents.append({
                            "_time": eventTime,
                            "_type": 2,
                            "_value": noteType,
                        })
                    else:
                        timeEvents.append({
                            "_time": eventTime,
                            "_type": 3,
                            "_value": noteType,
                        })
                else:
                    timeEvents.append({
                        "_time": eventTime,
                        "_type": 0,
                        "_value": noteType,
                    })
                    timeEvents.append({
                        "_time": eventTime,
                        "_type": 1,
                        "_value": noteType,
                    })
                    timeEvents.append({
                        "_time": eventTime,
                        "_type": 2,
                        "_value": noteType,
                    })
                    timeEvents.append({
                        "_time": eventTime,
                        "_type": 3,
                        "_value": noteType,
                    })
                    lastMainLightsRed = (totalTypes[0] == 0)
            else:
                # Get the values of the notes.
                backLaserValue = (lastMainLightsRed and 7 or 3)
                lastMainLightsRed = not lastMainLightsRed
                leftValue = 0
                rightValue = 0
                if len(columnsWithNotes) == 1:
                    leftValue = (lastMainLightsRed and 7 or 3)
                    rightValue = (lastMainLightsRed and 3 or 7)
                else:
                    if 0 in columnsWithNotes[0] and 1 in columnsWithNotes[len(columnsWithNotes) - 1]:
                        leftValue = 7
                        rightValue = 3
                    elif 1 in columnsWithNotes[0] and 0 in columnsWithNotes[len(columnsWithNotes) - 1]:
                        leftValue = 3
                        rightValue = 7

                # Get the events.
                timeEvents.append({
                    "_time": eventTime,
                    "_type": 0,
                    "_value": backLaserValue,
                })
                timeEvents.append({
                    "_time": eventTime,
                    "_type": 1,
                    "_value": backLaserValue,
                })
                timeEvents.append({
                    "_time": eventTime,
                    "_type": 2,
                    "_value": leftValue,
                })
                timeEvents.append({
                    "_time": eventTime,
                    "_type": 3,
                    "_value": rightValue,
                })

        # Add the laser speed events.
        events = []
        currentLaserSpeed = 0
        for eventGroup in eventGroups:
            # Get the total events that are near.
            eventTime = eventGroup[0]["_time"]
            totalNearEvents = 0
            for otherEventGroup in eventGroups:
                otherEventTime = otherEventGroup[0]["_time"]
                eventTimeDifference = otherEventTime - eventTime
                if eventTimeDifference >= -2 and eventTimeDifference <= 2:
                    totalNearEvents += 1

            # Set the laser speeed.
            newLaserSpeed = max(1, min(round(totalNearEvents), 8))
            if currentLaserSpeed != newLaserSpeed:
                currentLaserSpeed = newLaserSpeed
                events.append({
                    "_time": eventTime,
                    "_type": 12,
                    "_value": currentLaserSpeed,
                })
                events.append({
                    "_time": eventTime,
                    "_type": 13,
                    "_value": currentLaserSpeed,
                })
            for event in eventGroup:
                events.append(event)

        # Save the events.
        mapData["_events"] = events
