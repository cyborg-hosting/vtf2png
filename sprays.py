from os.path import getmtime
from pathlib import Path
from sys import stderr
import logging

import portalocker
from srctools import VTF
from srctools.vtf import ImageFormats, VTFFlags

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lock_path = Path('/var/lock/spray.lock')
lock = portalocker.Lock(lock_path, fail_when_locked=True)
try:
    lock.acquire()
except portalocker.AlreadyLocked as e:
    logger.info(e, exc_info=True)
    exit()

INPUT_DIRECTORY = Path(r'/in/')
OUTPUT_DIRECTORY = Path(r'/out/')

count = 0

for src_path in INPUT_DIRECTORY.glob('??/????????.dat'):
    if not src_path.is_file():
        continue

    dst_path = OUTPUT_DIRECTORY / (src_path.stem + '.png')

    if not dst_path.exists():
        pass
    elif getmtime(dst_path) < getmtime(src_path):
        pass
    else:
        continue

    try:
        vtf = None
        try:
            with src_path.open('rb') as file:
                try:
                    vtf = VTF.read(file)
                except ValueError as e:
                    logger.error(f'{src_path}: {e}')
                    src_path.unlink()
                    continue
                
                if vtf.flags & (VTFFlags.ONEBITALPHA | VTFFlags.EIGHTBITALPHA):
                    if vtf.format == ImageFormats.DXT1:
                        vtf.format = ImageFormats.DXT1_ONEBITALPHA
                    if vtf.low_format == ImageFormats.DXT1:
                        vtf.format = ImageFormats.DXT1_ONEBITALPHA
                    for frame in vtf._frames.values():
                        if frame._fileinfo is not None and frame._fileinfo[2] == ImageFormats.DXT1:
                            frame._fileinfo = (frame._fileinfo[0], frame._fileinfo[1], ImageFormats.DXT1_ONEBITALPHA)

                vtf.load()
        except PermissionError as e:
            logger.error(f'{src_path}: {e}')
            continue

        if vtf.frame_count <= 0:
            if len(vtf) != 0:
                logger.debug(vtf._frames)
            continue
        elif vtf.frame_count == 1:
            img = vtf.get().to_PIL()
            img.save(
                dst_path,
                format='PNG',
                optimize=True,
            )
        else:
            img, *imgs = ( vtf.get(frame=index).to_PIL() for index in range(vtf.frame_count) ) 
            img.save(
                dst_path,
                format='PNG',
                optimize=True,
                append_images=imgs,
                save_all=True,
                duration=200,
                loop=0,
            )
        logger.info(f'processed \'{src_path}\'')

        count += 1
    except Exception as e:
        logger.exception(f'{src_path}: {e}')

print('[INFO] total number of processed files:', count)

lock.release()
