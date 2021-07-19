# vtf2apng

A spray(vtf format) converter for spray n' display plugin.

## What you need

Grab those files from `(Source Engine Game Windows Installation)/bin/`

- `vtf2tga.exe`
- `vstdlib.dll`
- `tier0.dll`
- `FileSystem_Stdio.dll`

Mount the folder containing those to `/app/binaries/`.  
ex) `-v '/some/folder/containing/binaries/:/app/binaries/'`

Mount `(SRCDS Installation)/tf/downloads/` to `/image-in`  
ex) `-v '/tf2/installation/folder/tf/downloads/:/image-in/'`

Folder `/image-out/` is destination folder.

### Example docker-compose.yml file

    version: '3'

    services:
      vtf2apng:
        image: 'datmoyan/vtf2apng'

        volumes:
          - './binaries/:/app/binaries/'
          - './srcds/tf/download/:/image-in/'
          - './web-server/img/:/image-out/'

        tty: true
        restart: 'always'

## To do

- Mipmap process for 'some' spray image.
