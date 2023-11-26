import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

import json

def load_json_file(file_path):
    """
    Load a JSON file and return the data as a Python data structure.

    :param file_path: Path to the JSON file.
    :return: Python data structure (dict or list) containing data from the JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
# data = load_json_file('path_to_your_file.json')


def create_dataframe_from_json(runner_data):
    # Initialize an empty list to collect data
    combined_data = []

    for data in runner_data:
        # Extracting runner's basic info
        name = data['firstname'] + ' ' + data['lastname']
        
        # Looping through each split
        for split in data['result']['splits']:
            combined_data.append({
                'Name': name,
                'Split Name': split['name'],
                'Time of Day': split['time_of_day'],
                'Pace': split['pace'],
                'Elapsed Time': split['time']
            })

    # Create a DataFrame
    return pd.DataFrame(combined_data)
mike_data = load_json_file("Stewart_fjrnp5ynts.json")
chris_data = load_json_file("Whalen_p8pehdrrpc.json")
doyle_data = load_json_file("Doyle_m7pc7tte8k.json")

runners = [doyle_data, chris_data,mike_data]
df = create_dataframe_from_json(runners)

df['Time of Day'] = pd.to_datetime(df['Time of Day'], format='%I:%M:%S%p')
df['Pace'] = pd.to_datetime(df['Pace'], format='%M:%S').dt.time
df['Elapsed Time'] = pd.to_timedelta(df['Elapsed Time'])

# Function to convert time to total seconds
def time_to_seconds(time):
    return (time.hour * 3600) + (time.minute * 60) + time.second

# Adding pace in seconds for analysis
df['Pace in Seconds'] = df['Pace'].apply(lambda x: time_to_seconds(datetime.strptime(str(x), '%H:%M:%S')))
df['Hour of Day'] = df['Time of Day'].dt.hour + df['Time of Day'].dt.minute / 60

# Function to estimate finish time based on average split pace
def estimate_finish_time(df, total_distance=26.2):
    estimated_finish = []
    for name in df['Name'].unique():
        runner_data = df[df['Name'] == name]
        last_split = runner_data.iloc[-1]
        last_split_distance = float(last_split['Split Name'].split()[0])
        distance_remaining = total_distance - last_split_distance
        average_pace_seconds = runner_data['Pace in Seconds'].mean()
        time_remaining_seconds = distance_remaining * average_pace_seconds
        estimated_elapsed_time = last_split['Elapsed Time'].total_seconds() + time_remaining_seconds
        finish_time_of_day = (datetime.combine(pd.to_datetime('today').date(), last_split['Time of Day'].time())
                              + pd.to_timedelta(time_remaining_seconds, unit='s')).time()
        estimated_finish.append({
            'Name': name,
            'Estimated Finish Time': str(pd.to_timedelta(estimated_elapsed_time, unit='s')),
            'Estimated Time of Day': finish_time_of_day
        })
    return pd.DataFrame(estimated_finish)

# Estimating finish times based on average split pace
estimated_finish_df = estimate_finish_time(df)
print(estimated_finish_df)
