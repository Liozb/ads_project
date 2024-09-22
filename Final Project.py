import numpy as np
import pandas as pd
import seaborn as sns
import re
from datetime import datetime


def extract_weaponry(description, keywords):
    # Check if any weapon keyword is found in the description
    for keyword in keywords:
        if keyword in description.lower():
            return keyword
    return "unknown"


def extract_binary(description, keywords):
    # Check if any weapon keyword is found in the description
    for keyword in keywords:
        if keyword in description:
            return 1
    return 0


def file_process(input_file, output_file1, output_file2):
    # Read the text document
    with open(input_file, 'r') as file:
        text_data = file.read()
    locations_count = text_data.count("location=".lower())
    desc = text_data.count("description=".lower())

    # trouble shooting
    print("num of loc: ", locations_count)
    print("num of descr: ", desc)

    # Regular expressions to capture location, date, and description
    pattern = r"location='(.*?)'\s*description='(.*?)'"
    matches = re.findall(pattern, text_data, re.DOTALL)

    # Extract locations and descriptions
    locations = [match[0] for match in matches]
    descriptions = [match[1].replace('"', '').replace("\\'", "'").strip() for match in matches]
    date_pattern = r'(\d{1,2} \w+ \d{4})'  # Matches dates like "22 March 2024"

    # trouble shooting
    print("extracted loc: ", np.size(locations))
    print("extractd descr: ", np.size(descriptions))

    # Extract dates from descriptions
    for desc in descriptions:
      if re.search(date_pattern, desc) == None:
        print(desc)
    
    dates = [re.search(date_pattern, desc).group(1) for desc in descriptions]
    numeric_dates = [datetime.strptime(date, "%d %B %Y").strftime("%d-%m-%Y") for date in dates]

    # Create a DataFrame
    df = pd.DataFrame({
        'Location': locations,
        'Date': numeric_dates,
        'Description': descriptions
    })

    # keywords for new columns
    weapon_keys = ["rockets", "drone", "missiles", "anti-tank", "mortar", "projectile", "aerial target", "UAV",
                   "airstrike", "airstrike", "shells", "flare bombs", "machine gunfire", "shelling"]
    interception_keys = ["Interception", "intercepted"]
    killed_injured_keys = ["killed", "were injured", "injuring"]
    shot_down_keys = ["shot down"]

    # creating new fetures
    df['Weaponry'] = df['Description'].apply(lambda desc: extract_weaponry(desc, weapon_keys))
    df['Interception'] = df['Description'].apply(lambda desc: extract_binary(desc, interception_keys))
    df['Casulties'] = df['Description'].apply(lambda desc: extract_binary(desc, killed_injured_keys))

    # adjusting for israeli strikes
    if (df['Weaponry'] == 'airstrike').any():
        df['Shot Down'] = df['Description'].apply(lambda desc: extract_binary(desc, shot_down_keys))
        df = df.drop(columns=['Interception'])

    # counting strikes per location
    location_counts = df['Location'].value_counts()
    location_counts_df = location_counts.reset_index()
    location_counts_df.columns = ['Location', 'number of strikes']

    # Save to a CSV file
    df.to_csv(output_file1, index=False)
    location_counts_df.to_csv(output_file2, index=False)
    return df


df_0 = file_process("attacks_0.txt", "attacks_0.csv", "location_counts_0.csv")
df_1 = file_process("attacks_1.txt", "attacks_1.csv", "location_counts_1.csv")


