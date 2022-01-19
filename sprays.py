import os
import glob
import shutil
from PIL import Image

IN_DIR = '/image-in/user_custom/'
OUT_DIR = '/image-out/'

command = 'wine ./binaries/vtf2tga.exe -i {input} -o {output}'

assert os.path.exists(IN_DIR), 'Image-in volume is not directed to tf/downloads folder.'
assert os.path.exists('./binaries/vtf2tga.exe'), '\'vtf2tga.exe\' does not exist.'
assert os.path.exists('./binaries/tier0.dll'), '\'tier0.dll\' does not exist.'
assert os.path.exists('./binaries/vstdlib.dll'), '\'vstdlib.dll\' does not exist.'
assert os.path.exists('./binaries/FileSystem_Stdio.dll'), '\'FileSystem_Stdio.dll\' does not exist.'

count = 0

globStr = os.path.join(IN_DIR, '??/????????.dat')

for sprayFile in glob.iglob(globStr):
    if not os.path.isfile(sprayFile):
        continue

    path, name = os.path.split(sprayFile)
    file, extension = os.path.splitext(name)

    destPath = os.path.join(OUT_DIR, file + '.png')
    
    if not os.path.exists(destPath):
        pass
    elif os.path.getmtime(sprayFile) > os.path.getmtime(destPath):
        pass
    else:
        continue

    print('[INFO] IMAGE BEING PROCESSED NOW:', sprayFile)
    
    tempPath = os.path.join('temp', file + '.vtf')
    shutil.copyfile(sprayFile, tempPath)

    os.system(command.format(input=tempPath, output='temp/temp'))

    if os.path.exists('temp/temp000.tga'):
        img, *imgs = [Image.open(f) for f in sorted(glob.glob('temp/temp*.tga'))]
        img.save(fp=destPath,
                 format='PNG',
                 append_images=imgs,
                 save_all=True,
                 duration=200,
                 loop=0)
        count += 1
    
    elif os.path.exists('temp/temp.tga'):
        img = Image.open('temp/temp.tga')
        img.save(fp=destPath, format='PNG')
        count += 1
    
    for tgaFile in glob.iglob('temp/temp*.tga'):
        os.remove(tgaFile)

    try:
        os.remove(tempPath)
        print('[INFO] PROCESSED IMAGES COUNT:', count)
        print()
    except FileNotFoundError:
        pass