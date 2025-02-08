## Cricket Score Tracker

## Overview

This Python project fetches live cricket match data using the Unofficial Cricbuzz API and logs API call timestamps into an SQLite database. The data includes live scores, batsmen statistics, bowler performance, and match status. The script runs periodically using the schedule library.

## Features

Fetches live match data (score, wickets, overs, batsmen, and bowler stats).

Logs API call timestamps in an SQLite database.

Runs every minute to fetch updated match data.

## Prerequisites

Make sure you have the following dependencies installed:

pip install requests schedule sqlite3

## Setup & Usage

Clone this repository:

git clone https://github.com/Score_teller/cricket-score-tracker.git

Navigate to the project folder:

cd cricket-score-tracker

Run the script:

python score_tracker.py

Project Structure

cricket-score-tracker/
│── score_tracker.py  # Main script
│── README.md         # Documentation
│── score_teller.db   # SQLite database (created automatically)

## API Details

Endpoint 1 (Overs Data):

https://unofficial-cricbuzz.p.rapidapi.com/matches/get-overs?matchId=111105

Endpoint 2 (Match Status):

https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard?matchId=111105

Authentication is done using X-RapidAPI-Key in the request headers.

## Database Logging

The script logs each API call timestamp in an SQLite database (score_teller.db).

The table api_logs stores the timestamps of API calls.

You can fetch the last API call timestamp using:

SELECT timestamp FROM api_logs ORDER BY id DESC LIMIT 1;

## Scheduler

The script uses the schedule library to call the API every 1 minute.

## Troubleshooting

If API calls fail, ensure your RapidAPI Key is valid.

Ensure your internet connection is active.

If database errors occur, try deleting score_teller.db and re-running the script.

Author

Anshuman Sharma
