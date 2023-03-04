import os
import shutil
import subprocess


def install_app(dmg_file, target_dir):
    p = subprocess.Popen(['hdiutil', 'attach', dmg_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    while True:
        retcode = p.poll()
        line = p.stdout.readline()
        if 'Apple_HFS' in str(line):
            _str = str(line)
        if retcode is not None:
            break
    
    start = '/Volumes/'
    end = '\\'
    name = (_str.split(start))[1].split(end)[0]
    vol = f'/Volumes/{name}'
    
    for f in os.listdir(vol):
        t = os.path.splitext(f)
        if t[1] == '.app':
            app_name = f
    
    shutil.copytree(f'{vol}/{app_name}', f'{target_dir}/{app_name}')
