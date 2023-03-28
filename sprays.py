import logging
from os.path import getmtime
from pathlib import Path

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

def read_vtf(path: Path) -> VTF:
    try:
        file = path.open('rb')
    except PermissionError as e:
        logger.error(f'{path}: {e}')
        return None
    except IOError:
        logger.exception(f'{path}')
        return None
    
    try:
        vtf = VTF.read(file)
    except ValueError as e:
        logger.error(f'{path}: {e}')
        return None

    if vtf.flags & (VTFFlags.ONEBITALPHA | VTFFlags.EIGHTBITALPHA):
        if vtf.format == ImageFormats.DXT1:
            vtf.format = ImageFormats.DXT1_ONEBITALPHA
        if vtf.low_format == ImageFormats.DXT1:
            vtf.format = ImageFormats.DXT1_ONEBITALPHA
        for frame in vtf._frames.values():
            if frame._fileinfo is not None and frame._fileinfo[2] == ImageFormats.DXT1:
                frame._fileinfo = (frame._fileinfo[0], frame._fileinfo[1], ImageFormats.DXT1_ONEBITALPHA)

    vtf.load()

    try:
        file.close()
    except IOError:
        logger.exception(f'{path}')

    return vtf

def write_png(vtf: VTF, dest: Path, *, mipmap: int = 0) -> bool:
    if vtf.frame_count <= 0:
        if len(vtf) != 0:
            logger.debug(vtf._frames)
        return False
    elif vtf.frame_count == 1:
        img = vtf.get(mipmap=mipmap).to_PIL()
        img.save(
            dest,
            format='PNG',
            optimize=True,
        )
    else:
        img, *imgs = ( vtf.get(frame=index, mipmap=mipmap).to_PIL() for index in range(vtf.frame_count) ) 
        img.save(
            dest,
            format='PNG',
            optimize=True,
            append_images=imgs,
            save_all=True,
            duration=200,
            loop=0,
        )
    return True

INPUT_DIRECTORY = Path(r'/in')
OUTPUT_DIRECTORY = Path(r'/out')

count = 0

for src_path in INPUT_DIRECTORY.glob('??/????????.dat'):
    if not src_path.is_file():
        continue

    dst_path = OUTPUT_DIRECTORY / (src_path.stem + '.png')

    if dst_path.exists() and getmtime(dst_path) > getmtime(src_path):
        continue

    try:
        vtf = read_vtf(src_path)
        if not vtf:
            continue

        if not write_png(vtf, dst_path):
            continue

        if vtf.mipmap_count > 1:
            try:
                mipmap_dir = OUTPUT_DIRECTORY / 'mipmap' / src_path.stem
                mipmap_dir.mkdir(parents=True, exist_ok=True)

                for mipmap in range(1, vtf.mipmap_count):
                    mipmap_path = mipmap_dir / (str(mipmap) + '.png')
                    write_png(vtf, mipmap_path, mipmap=mipmap)
                
            except OSError:
                logger.error(f'{src_path}: {e}')

        logger.info(f'processed \'{src_path}\'')

        count += 1
    except Exception as e:
        logger.exception(f'{src_path}: {e}')

print('[INFO] total number of processed files:', count)

lock.release()
