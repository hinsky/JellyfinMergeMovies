#! /usr/bin/env python3

import sqlite3
import requests

# Set with your own data
api_key = ""
url = ""
db = ""

# Open Jellyfin library DB
conn = sqlite3.connect(db)
cursor = conn.cursor()

# Query the movies list
cursor.execute("""
    SELECT DISTINCT
        SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb='),
            CASE
                WHEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb=')), '|') > 0
                THEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb=')), '|') - 1
                ELSE LENGTH(ProviderIds)
            END) AS ExtractedProviderValue,
        PresentationUniqueKey,
        Name
    FROM
        TypedBaseItems
    WHERE
        type = 'MediaBrowser.Controller.Entities.Movies.Movie'
        AND IsVirtualItem = '0'
        AND ProviderIds LIKE '%Tmdb=%'
    ORDER BY
        ExtractedProviderValue
""")
video_data = cursor.fetchall()

# Close DB connection
conn.close()

# check video_data，delete unique ProviderIds items(not duaplicated)
unique_provider_ids = set([data[0] for data in video_data])
for provider_id in unique_provider_ids:
    if sum(1 for data in video_data if data[0] == provider_id) == 1:
        video_data = [data for data in video_data if data[0] != provider_id]

# Find duplicate ProviderIds row data and perform the merge operation
for provider_id in unique_provider_ids:
    if sum(1 for data in video_data if data[0] == provider_id) > 1:
        # Combine PresentationUniqueKey and name values
        ids = ",".join([data[1] for data in video_data if data[0] == provider_id])
        names = ",".join([data[2] for data in video_data if data[0] == provider_id])
        # Build the curl post request
        merge_url = f"{url}/Videos/MergeVersions?api_key={api_key}&ids={ids}"
        # post request
        #print(merge_url)
        response = requests.post(merge_url)
        # Output execution result
        if response.status_code == 204:
            print(f"Merged versions count: {len(ids.split(','))} {names}")
        else:
            print(f"Error occurred while merging versions: {ids} {names}")
            continue
