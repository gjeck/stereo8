# stereo8
[![Code Climate](https://codeclimate.com/github/gjeck/stereo8/badges/gpa.svg)](https://codeclimate.com/github/gjeck/stereo8)

# Getting started

## Docker
You'll need [docker](https://www.docker.com/products/docker-toolbox) installed. Launch the application by running
```
docker-compose up
```

It's often useful to enter one of the containers to debug. Do that by running:
```
docker exec <container_name> bash
// or more explicitly 
docker ps -a // lists current container ids
docker exec -it <container_id> bash
```

It will be expecting a `.keys.dockenv` file containing important passwords and configuration values. The most important are as follows:
```
# Django keys
DJANGO_PRODUCTION_KEY=some_password

# Postgres keys
POSTGRES_PASSWORD=some_password
POSTGRES_USER=postgres_user
POSTGRES_DB=some_db

# Last.fm API http://www.last.fm/api
LAST_FM_API_KEY=some_key
LAST_FM_SECRET=some_secret

# Spotify API https://developer.spotify.com/
SPOTIFY_CLIENT_ID=some_id
SPOTIFY_CLIENT_SECRET=some_secret
```

## Django
You'll need to create a super user to access the django admin panel
```
python3 manage.py createsuperuser
```

## Scrapers
To run a scraper navigate to `scrapers` and run
```
scrapy crawl <scraper_name>
```

Pass arguments to the scraper using `-a`:
```
scrapy crawl <scraper_name> -a argument1=value1
```

## Database
To connect and inspect the database run:
```
docker-compose exec db psql -U postgres -d stereo8db
```

## Hasura
This service provides the graphql api endpoint. To restore the service's metadata:
1. Click on the settings icon in the console screen
2. Choose `hasura/metadata.json`
