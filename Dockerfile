FROM python:3.11-slim

ARG PUID=1000
ENV USER=spray

RUN apt-get update && \
	apt-get -y install cron sudo && \
	rm -r /var/lib/apt/lists/* && \
	useradd -u "${PUID}" -m "${USER}"

WORKDIR /app/

ADD ./requirements.txt ./
RUN pip install --no-cache-dir --use-pep517 --requirement requirements.txt

VOLUME [ "/in/", "/out/" ] 

ADD ./sprays.py ./
ADD ./crontab /etc/crontab

RUN chmod +x /etc/crontab && \
	touch .spray.lock && \
	chown spray:spray .spray.lock

CMD [ "cron", "-f" ]
