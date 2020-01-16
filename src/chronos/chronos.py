# -*- coding: utf-8 -*-

"""Main module."""

import base64
import iso8601
import json
import datetime
import pickle
import os

from flask import Flask
from flask import jsonify, url_for

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


app = Flask(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

SERVICE_ACCOUNT_FILE = "secrets/credentials.json"


def get_service():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "secrets/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    return service


def timesheet(event_name):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    hours_worked = {
        "Sunday": 0,
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Total": 0,
    }

    cal = get_service()
    if cal is None:
        return

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
            calendarId="primary",
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
        if event["summary"] == event_name:
            rawstart = event["start"].get("dateTime", event["start"].get("date"))
            rawend = event["end"].get("dateTime", event["end"].get("date"))

            start = iso8601.parse_date(rawstart)
            end = iso8601.parse_date(rawend)

            day_of_week = start.strftime("%A")

            duration = end - start
            total += duration.seconds / 3600

            hours_worked[day_of_week] += duration.seconds / 3600

    hours_worked["Total"] = total

    return hours_worked


@app.route("/")
def hello():
    return "Hello"


@app.route("/health")
def health_check():
    return "1"


@app.route("/<event>")
def event(event):

    weekly_timesheet = timesheet(event)

    print("[INFO]", weekly_timesheet)

    return jsonify(weekly_timesheet)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
