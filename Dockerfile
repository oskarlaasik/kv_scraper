FROM python:3
MAINTAINER Oskar Laasik <oskar.laasik@yahoo.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/kv_scraper/src
# We copy the requirements.txt file first to avoid cache invalidations
COPY requirements.txt /opt/services/kv_scraper/src/
WORKDIR /opt/services/kv_scraper/src
RUN pip install -r requirements.txt
COPY . /opt/services/kv_scraper/src
EXPOSE 5090
CMD ["python", "kv_scraper.py"]


