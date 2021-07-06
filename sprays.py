import os
import glob
import shutil
from PIL import Image
import time

IN_DIR = '/image-in/user_custom/'
OUT_DIR = '/image-out/'

command = 'wine ./binaries/vtf2tga.exe -i {input} -o {output}'

assert os.path.exists(IN_DIR), 'Image-in volume is not directed to tf/downloads folder.'
assert os.path.exists('./binaries/vtf2tga.exe'), '\'vtf2tga.exe\' does not exist.'
assert os.path.exists('./binaries/tier0.dll'), '\'tier0.dll\' does not exist.'
assert os.path.exists('./binaries/vstdlib.dll'), '\'vstdlib.dll\' does not exist.'
assert os.path.exists('./binaries/FileSystem_Stdio.dll'), '\'FileSystem_Stdio.dll\' does not exist.'

count = 0

for sprayFolderPath in [path for path in map(lambda dir: os.path.join(IN_DIR, dir), os.listdir(IN_DIR)) if os.path.isdir(path)]:
    for sprayFile in [spray for spray in map(lambda fileName: (fileName, os.path.join(sprayFolderPath, fileName), os.path.splitext(fileName)), os.listdir(sprayFolderPath))
                            if os.path.isfile(spray[1])
                            and spray[0].endswith('.dat')]:
        if (int(time.time()) - os.path.getmtime(sprayFile[1]) < 604800
            and (not os.path.exists(os.path.join(OUT_DIR, sprayFile[2][0] + '.png'))
                or int(time.time()) - os.path.getmtime(os.path.join(OUT_DIR, sprayFile[2][0] + '.png')) > 604800)):
            beforePath = sprayFile[1]
            afterPath = os.path.join('temp/', sprayFile[2][0] + '.vtf')
            shutil.copyfile(beforePath, afterPath)

            os.system(command.format(input=afterPath, output='temp/temp'))

            if os.path.exists('./temp/temp000.tga'):
                img, *imgs = [Image.open(f) for f in sorted(glob.glob('./temp/temp*.tga'))]
                img.save(fp=os.path.join(OUT_DIR, sprayFile[2][0] + '.png'), format='PNG', append_images=imgs, save_all=True, duration=200, loop=0)

                for file in glob.glob('./temp/temp*.tga'):
                    os.remove(file)

            elif os.path.exists('./temp/temp.tga'):
                img = Image.open('./temp/temp.tga')
                img.save(fp=os.path.join(OUT_DIR, sprayFile[2][0] + '.png'), format='PNG')

                os.remove('./temp/temp.tga')

            try:
                os.remove(afterPath)
                count += 1
                print(count)
            except FileNotFoundError:
                pass
