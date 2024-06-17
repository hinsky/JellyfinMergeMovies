# JellyfinMergeSplit

Python script, using the Jellyfin API to merge/split mutiple versions for movies/tv episodes accross the whole library

Only tested on Debian Docker version Jellyfin 10.9.x


## You'll need python3 with requests package, sqlite3

```
sudo apt update
sudo apt install sqlite3
sudo apt install python3
sudo python3 -m pip install requests
sudo chmod +x /path/to/mergesplit.py
``` 


## Config the following with your own

api_key = "xxxxxxxxxxxxxx"  #Generate this API key from your Jellyfin backend

url = "http://127.0.0.1:8096"  #Your Jellyfin address

db = "/etc/jellyfin/config/data/library.db"  #Your Jellyfin data path


## run with arguments:

mergemov - Merge movies(with tmdb data)

mergetvimdb - Merge TV episodes with imdb data

mergetvtvdb - Merge TV episodes with tvdb data

splitmov - Split movies

splittv - Split TV episodes


## add to cron job, for example I set merge movies to run at 10:00 and 23:00 everyday.
``` 
0 10,23 * * * /root/mergesplit.py mergemov > /root/mergemov.log 2>&1
``` 
