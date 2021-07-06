# vtf2apng

A spray(vtf format) converter for spray n' display plugin.

## What you need:

From `(Team Fortress 2 installation)/bin/`
  - `vtf2tga.exe`
  - `vstdlib.dll`
  - `tier0.dll`
  - `FileSystem_Stdio.dll`

Mount the folder containing those to `/app/binaries/`.  
ex) `-v '/some/folder/containing/binaries/:/app/binaries/'`

Mount `(Team Fortress 2 installation/tf/downloads/)` to `/image-in`  
ex) `-v '/tf2/installation/folder/tf/downloads/:/image-in/'`

Folder `/image-out/` is destination folder.

### Example docker-compose.yml file

    version: '3'

    services:
      vtf2apng:
        image: 'datmoyan/vtf2tga'

        volumes:
          - './binaries/:/app/binaries/'
          - './srcds/tf/download/:/image-in/'
          - './web-server/img/:/image-out/'

        tty: true
        restart: 'always'

## To do:
  - Mipmap process for 'some' spray image.
