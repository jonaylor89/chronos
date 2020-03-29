# -*- coding: utf-8 -*-

"""Main module."""

import base64
import iso8601
import json
import datetime
import pickle
import sys
import os

import google.auth
from googleapiclient.discovery import build

CALENDAR_ID = "jonaylor89@gmail.com"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CLIENT_SECRET_FILE = "credentials.json"


def timesheet(request):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "name" in request_json:
        name = request_json["name"]
    elif request_args and "name" in request_args:
        name = request_args["name"]
    else:
        return "No event"

    credentials, project_id = google.auth.default(scopes=SCOPES)

    cal = build("calendar", "v3", credentials=credentials)

    hours_worked = [0, 0, 0, 0, 0, 0, 0]

    if cal is None:
        return "Calendar is None"

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.date.today()
    weekday = today.weekday()
    # lower bound
    lower = today - datetime.timedelta(days=weekday)
    # upper bound
    upper = today + datetime.timedelta(days=(6 - weekday))

    iso_lower = (
        datetime.datetime.combine(lower, datetime.datetime.min.time()).isoformat() + "Z"
    )
    iso_upper = (
        datetime.datetime.combine(upper, datetime.datetime.min.time()).isoformat() + "Z"
    )

    events_result = (
        cal.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=iso_lower,
            timeMax=iso_upper,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])
    total = 0

    if not events:
        print("No upcoming events found.")
    for event in events:
        if event["summary"] == name:
            rawstart = event["start"].get("dateTime", event["start"].get("date"))
            rawend = event["end"].get("dateTime", event["end"].get("date"))

            start = iso8601.parse_date(rawstart)
            end = iso8601.parse_date(rawend)

            day_of_week = start.strftime("%w")

            duration = end - start

            hours_worked[int(day_of_week)] += duration.seconds / 3600

    return str(hours_worked)

if __name__ == "__main__":
    if len(sys.argv) > 1:

        class test(object):
            def __init__(self):
                self.args = None

            def get_json(self, silent):
                return json.loads(sys.argv[1])

        print(timesheet(test()))
