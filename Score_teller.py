import requests
import json
import schedule
import time
import sqlite3
from datetime import datetime
id='111105'
# API details
url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-overs?matchId=111105"
url_status = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard?matchId=111105"

headers = {
    "X-RapidAPI-Key": "5f066d569cmsh360924500738926p14bd11jsn70bda181c743",
    "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com"
}


db_name="score_teller.db"

def create_table():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS api_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_api_call():
    """Log the API call timestamp using the system's current date and time."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO api_logs (timestamp) VALUES (?)', (current_time,))
    conn.commit()
    conn.close()
def fetch_last_run_time():
    """Retrieve the last API run time."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp FROM api_logs ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "No previous API calls logged."
api_call_counter=0
def fetch_cricket_data():
    global api_call_counter
    try:
        # Fetch overs data
        api_call_counter +=1 
        response = requests.get(url, headers=headers)
        data = response.json()

        # Current innings details
        current_innings_details = data['miniscore']['inningsScores'][0]['inningsScore'][0]
        current_innings_runs = current_innings_details['runs']
        current_innings_wickets = current_innings_details['wickets']
        current_innings_overs = current_innings_details['overs']

        print("---------------------------------------------------Over Data-----------------------------------")
        print(f"Current score: {current_innings_runs}")
        print(f"Current wickets: {current_innings_wickets}")
        print(f"Current overs: {current_innings_overs}")

        print("---------------------------------------------------Batsman 1-----------------------------------")
        striker_data = data['miniscore'].get('batsmanStriker', {})
        print(f"{striker_data.get('name', 'N/A')}  {striker_data.get('runs', 0)} runs in {striker_data.get('balls', 0)} balls")

        print("---------------------------------------------------Batsman 2-----------------------------------")
        non_striker_data = data['miniscore'].get('batsmanNonStriker', {})
        print(f"{non_striker_data.get('name', 'N/A')}  {non_striker_data.get('runs', 0)} runs in {non_striker_data.get('balls', 0)} balls")

        # Bowler stats
        print("---------------------------------------------------Bowling-----------------------------------")
        bowler_data = data['miniscore'].get('bowlerNonStriker', {})
        bowler_wickets = bowler_data.get('wickets', 0)
        print(f"{bowler_data.get('name', 'N/A')}  {bowler_data.get('overs', '0.0')} overs  {bowler_data.get('runs', 0)} runs  {bowler_wickets} wickets")

        # Fetch match status
        response_status = requests.get(url_status, headers=headers)
        data_status = response_status.json()
        print("---------------------------------------------------Match Status-----------------------------------")
        print(data_status.get('status', 'N/A'))
        print(f"API now calling for {api_call_counter+1} times.")
    
    
        log_api_call()
    except Exception as e:
        print(f"Error fetching data: {e}")

# Schedule the function to run every 1 minute
schedule.every(1).minute.do(fetch_cricket_data)
create_table()
counter=0
print(f"counter ran{counter+1} times")
# Keep the script running to execute scheduled tasks
print("Starting scheduler... Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    
    
    
    
