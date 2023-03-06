FROM python:3.11-slim

RUN apt-get update && \
	apt-get -y install cron && \
	rm -r /var/lib/apt/lists/*

WORKDIR /app/

ADD ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

VOLUME [ "/in/", "/out/" ] 

ADD ./sprays.py ./
ADD ./entrypoint.sh ./
ADD ./spray-cron /etc/cron.d/spray-cron

RUN chmod +x /etc/cron.d/spray-cron && \
	chmod +x ./entrypoint.sh

CMD [ "/app/entrypoint.sh" ]
