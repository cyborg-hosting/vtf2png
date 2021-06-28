import os
import glob
import shutil
from PIL import Image
import time

IN_DIR = '/image-in/user_custom/'
OUT_DIR = '/image-out/'

command = 'wine vtf2tga.exe -i {input} -o {output}'

for dir in os.listdir(IN_DIR):
    
    dir = os.path.join(IN_DIR, dir)
    
    if os.path.isdir(dir):
        for dat in os.listdir(dir):
            if dat.endswith('.dat') and int(time.time()) - os.path.getmtime(os.path.join(dir, dat)) < 604800:
                beforePath = os.path.join(dir, dat)
                afterPath = os.path.join('./temp/', os.path.splitext(dat)[0] + '.vtf')
                shutil.copyfile(beforePath, afterPath)

                os.system(command.format(input='temp/' + os.path.splitext(dat)[0] + '.vtf', output='temp/temp'))

                if os.path.exists('./temp/temp000.tga'):
                    img, *imgs = [Image.open(f) for f in sorted(glob.glob('./temp/temp*.tga'))]
                    img.save(fp=os.path.join(OUT_DIR, os.path.splitext(dat)[0] + '.png'), format='PNG', append_images=imgs, save_all=True, duration=200, loop=0)

                    for file in glob.glob('./temp/temp*.tga'):
                        try:
                            os.remove(file)
                        except OSError:
                            pass
                elif os.path.exists('./temp/temp.tga'):
                    img = Image.open('./temp/temp.tga')
                    img.save(fp=os.path.join(OUT_DIR, os.path.splitext(dat)[0] + '.png'), format='PNG')

                    try:
                        os.remove('./temp/temp.tga')
                    except OSError:
                        pass

                if os.path.exists(afterPath):
                    try:
                        os.remove(afterPath)
                    except OSError:
                        pass
                            

                
                




