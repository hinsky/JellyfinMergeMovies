# JellyfinMergeSplit

## Python script, using the Jellyfin API to merge/split versions for movies/tv episodes accross the whole library

Only tested for Docker version Jellyfin 10.9.x on Debian


## You'll need sqlite3

apt-get install sqlite3



## Config the following with your own


api_key = "xxxxxxxxxxxxxx"  #Generate this API key from your Jellyfin backend

url = "http://127.0.0.1:8096"  #Your Jellyfin address

db = "/etc/jellyfin/config/data/library.db"  #Your Jellyfin data path

## arguments:
mergemov - Merge movies(with tmdb data)
mergetvimdb - Merge TV episodes with imdb data
mergetvtbdb - Merge TV episodes with tvdb data
splitmov - Split movies
splittv - Split TV episodes




## add to cron job, I set it to run every 20m from 5am to 23pm

crontab -e

*/20 5-23 * * * /root/mergemovies.py mergemov > /root/mergemov.log 2>&1
