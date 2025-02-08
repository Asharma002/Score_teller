import requests
import json
import schedule
import time
import sqlite3
from datetime import datetime
from plyer import notification

# API details
match_id = '111105'
url = f"https://unofficial-cricbuzz.p.rapidapi.com/matches/get-overs?matchId={match_id}"
url_status = f"https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard?matchId={match_id}"

headers = {
    "X-RapidAPI-Key": "5f066d569cmsh360924500738926p14bd11jsn70bda181c743",
    "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com"
}

db_name = "score_teller.db"

def create_table():
    """Create database table if it doesn't exist."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS api_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_api_call():
    """Log the API call timestamp."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO api_logs (timestamp) VALUES (?)', (current_time,))
    conn.commit()
    conn.close()

def send_notification(title, message):
    """Send system notification using Plyer."""
    notification.notify(
        title=title,
        message=message,
        timeout=5  # Notification duration
    )

def fetch_cricket_data():
    """Fetch and display cricket match details while sending notifications."""
    try:
        # Fetch overs data
        response = requests.get(url, headers=headers)
        data = response.json()

        # **Check if 'miniscore' exists**
        if 'miniscore' not in data:
            print("Error: 'miniscore' key not found in API response.")
            print("Full API Response:", json.dumps(data, indent=4))  # Print full response for debugging
            return

        # Extract match details
        current_innings_details = data['miniscore']['inningsScores'][0]['inningsScore'][0]
        current_innings_runs = current_innings_details['runs']
        current_innings_wickets = current_innings_details['wickets']
        current_innings_overs = current_innings_details['overs']

        batsman1 = data['miniscore'].get('batsmanStriker', {})
        batsman2 = data['miniscore'].get('batsmanNonStriker', {})
        bowler = data['miniscore'].get('bowlerNonStriker', {})

        # Fetch match status
        response_status = requests.get(url_status, headers=headers)
        data_status = response_status.json()
        match_status = data_status.get('status', 'N/A')

        # Console Output
        print("---------------------------------------------------Over Data-----------------------------------")
        print(f"Current score: {current_innings_runs}/{current_innings_wickets} in {current_innings_overs} overs")
        print("---------------------------------------------------Batsmen-----------------------------------")
        print(f"{batsman1.get('name', 'N/A')} - {batsman1.get('runs', 0)} runs ({batsman1.get('balls', 0)} balls)")
        print(f"{batsman2.get('name', 'N/A')} - {batsman2.get('runs', 0)} runs ({batsman2.get('balls', 0)} balls)")
        print("---------------------------------------------------Bowling-----------------------------------")
        print(f"{bowler.get('name', 'N/A')} - {bowler.get('overs', '0.0')} overs, {bowler.get('runs', 0)} runs, {bowler.get('wickets', 0)} wickets")
        print("---------------------------------------------------Match Status-----------------------------------")
        print(match_status)

        # **Send Notification Immediately**
        notification_title = "Live Cricket Score Update"
        notification_message = f"{current_innings_runs}/{current_innings_wickets} in {current_innings_overs} overs\n"
        notification_message += f"Batsman: {batsman1.get('name', 'N/A')} ({batsman1.get('runs', 0)}) & {batsman2.get('name', 'N/A')} ({batsman2.get('runs', 0)})\n"
        notification_message += f"Bowler: {bowler.get('name', 'N/A')} ({bowler.get('overs', '0.0')} overs, {bowler.get('wickets', 0)} wickets)\n"
        notification_message += f"Status: {match_status}"

        send_notification(notification_title, notification_message)

        # **Log the API call after notification**
        log_api_call()

    except Exception as e:
        print(f"Error fetching data: {e}")

# Schedule the function to run every 1 minute
schedule.every(1).minute.do(fetch_cricket_data)

create_table()

print("Starting scheduler... Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)
