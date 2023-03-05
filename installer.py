import os
import shutil
import subprocess


def check_dir_exist(target_dir):
    if not os.path.exists(target_dir):
        choice = input(f'The path {target_dir} does not exist.\nDo you want to create it? y/n: ')
        if choice == 'y':
            os.mkdir(target_dir)
            return
        else:
            print('Aborting...')
            exit(0)


def copy_app(src, dst):
    if os.path.exists(dst):
        choice = input(f'The path {dst} already exist.\nDo you want to overwrite it? y/n: ')
        if choice == 'y':
            shutil.rmtree(dst)
        else:
            print('Aborting...')
            exit(0)
    shutil.copytree(src, dst, symlinks=True, copy_function=shutil.copy)


def install_app(dmg_file, target_dir):
    check_dir_exist(target_dir)
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

    src = f'{vol}/{app_name}'
    dst = f'{target_dir}/{app_name}'

    copy_app(src, dst)
    print('Finished.')
