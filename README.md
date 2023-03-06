# vtf2png

A spray(vtf format) converter for spray n' display plugin.

## What you need

Mount `(SRCDS Installation)/tf/downloads/` to `/in`  
ex) `-v '/tf2/installation/folder/tf/downloads/:/in/'`

Folder `/out/` is destination folder.

### Example docker-compose.yml file

    version: '3'

    services:
      vtf2apng:
        image: 'datmoyan/vtf2apng'

        volumes:
          - './srcds/tf/download/:/in/'
          - './web-server/img/:/out/'

        tty: true
        restart: 'always'

## To do

- Mipmap process for 'some' spray image.
