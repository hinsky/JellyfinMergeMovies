# JellyfinMergeSplit

Python script, using the Jellyfin API to merge/split mutiple versions for movies/tv episodes accross the whole library

Only tested on Debian Docker version Jellyfin 10.9.x


## You'll need sqlite3

apt-get install sqlite3



## Config the following with your own


api_key = "xxxxxxxxxxxxxx"  #Generate this API key from your Jellyfin backend

url = "http://127.0.0.1:8096"  #Your Jellyfin address

db = "/etc/jellyfin/config/data/library.db"  #Your Jellyfin data path

## run with arguments:
mergemov - Merge movies(with tmdb data)

mergetvimdb - Merge TV episodes with imdb data

mergetvtbdb - Merge TV episodes with tvdb data

splitmov - Split movies

splittv - Split TV episodes




## add to cron job, for example I set merge movie to run at 10:00 and 23:00 everyday.

0 10,23 * * * /root/mergemovies.py mergemov > /root/mergemov.log 2>&1
