#! /usr/bin/env python3

import sqlite3
import requests
import sys


# Set with your own data
api_key = ""
url = ""
db = ""

arguments = sys.argv[1]

if len(arguments) > 0:
    if arguments == 'mergemov' or arguments == 'mergetvimdb' or arguments == 'mergetvtvdb':
        if arguments == 'mergemov':
            query = """SELECT DISTINCT SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb='), CASE WHEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb=')), '|') > 0 THEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb=')), '|') - 1 ELSE LENGTH(ProviderIds) END) AS ExtractedProviderValue, PresentationUniqueKey, Name FROM TypedBaseItems WHERE type = 'MediaBrowser.Controller.Entities.Movies.Movie' AND IsVirtualItem = '0' AND ProviderIds LIKE '%Tmdb=%' ORDER BY ExtractedProviderValue"""
        if arguments == 'mergetvimdb':
            query = """SELECT DISTINCT SUBSTR(ProviderIds, INSTR(ProviderIds, 'Imdb=') + LENGTH('Imdb='), CASE WHEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Imdb=') + LENGTH('Imdb=')), '|') > 0 THEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Imdb=') + LENGTH('Imdb=')), '|') - 1 ELSE LENGTH(ProviderIds) END) AS ExtractedProviderValue, PresentationUniqueKey, Name FROM TypedBaseItems WHERE type = 'MediaBrowser.Controller.Entities.TV.Episode' AND IsVirtualItem = '0' AND ProviderIds LIKE '%Imdb=%' ORDER BY ExtractedProviderValue"""
        if arguments == 'mergetvtvdb':
            query = """SELECT DISTINCT SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tvdb=') + LENGTH('Tvdb='), CASE WHEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tvdb=') + LENGTH('Tvdb=')), '|') > 0 THEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tvdb=') + LENGTH('Tvdb=')), '|') - 1 ELSE LENGTH(ProviderIds) END) AS ExtractedProviderValue, PresentationUniqueKey, Name FROM TypedBaseItems WHERE type = 'MediaBrowser.Controller.Entities.TV.Episode' AND IsVirtualItem = '0' AND ProviderIds LIKE '%Tvdb=%' ORDER BY ExtractedProviderValue"""
         
        # Open Jellyfin library DB  
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(query)
        video_data = cursor.fetchall()
        
        # Close DB connection
        cursor.close()
        conn.close()
        
        # check video_data，delete unique ProviderIds items(not duaplicated)
        unique_provider_ids = set([data[0] for data in video_data])
        for provider_id in unique_provider_ids:
            if sum(1 for data in video_data if data[0] == provider_id) == 1:
                video_data = [data for data in video_data if data[0] != provider_id]
                
        # Find duplicate ProviderIds row data and perform the merge operation
        for provider_id in unique_provider_ids:
            # Combine PresentationUniqueKey and name values
            if sum(1 for data in video_data if data[0] == provider_id) > 1:
                ids = ",".join([data[1] for data in video_data if data[0] == provider_id])
                names = ",".join([data[2] for data in video_data if data[0] == provider_id])
                
                # Build the curl post request
                merge_url = f"{url}/Videos/MergeVersions?api_key={api_key}&ids={ids}"

                # post request
                response = requests.post(merge_url)
                
                # Output execution result
                if response.status_code == 204:
                    print(f"Merged versions count: {len(ids.split(','))} {names}")
                else:
                    print(f"Error occurred while merging versions: {ids} {names}")
                    continue
                
    
    elif arguments == 'splitmov' or arguments == 'splittv':
        if arguments == 'splitmov':
            query = """ SELECT PresentationUniqueKey FROM TypedBaseItems WHERE type = 'MediaBrowser.Controller.Entities.Movies.Movie' GROUP BY PresentationUniqueKey HAVING COUNT(*) > 1 """
        if arguments == 'splittv':
            query = """ SELECT PresentationUniqueKey FROM TypedBaseItems WHERE type = 'MediaBrowser.Controller.Entities.TV.Episode' GROUP BY PresentationUniqueKey HAVING COUNT(*) > 1 """
        # Open Jellyfin library DB  
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(query)
        unique_keys_with_duplicates = cursor.fetchall()
        unique_keys = [key[0] for key in unique_keys_with_duplicates]
        
        # Close DB connection
        cursor.close()
        conn.close()
        
        # Split operation
        for key in unique_keys:
            split_url = f"{url}/Videos/{key}/AlternateSources?api_key={api_key}"
            response = requests.delete(split_url)
            # Output execution result
            if response.status_code == 204:
                print(f"Slipted versions for: {key}")
            else:
                print(f"Error occurred while spliting versions: {key}")
                continue

    else:
        print("Unknown arguments")
else:
    print("Please input the correct arguments")
