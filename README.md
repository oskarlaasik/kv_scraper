# kv_scraper


This is a containerized Flask application to scrape kv.ee

Build the image:
```
$ docker-compose build
```

Once the image is built, run the container:
```
$ docker-compose up -d
```

Navigate to http://localhost:8080/api to view the api documentation.

Scraper can be activated
```
docker exec [parent_folder_name]_kv_scraper_1 python kv_scraper.py
```
