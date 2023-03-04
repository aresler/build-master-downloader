### WARNING

An experimental branch to test automatic installation. For now Mac only.

---
A simple script to download latest master build from TeamCity build server

### Usage

1. Copy `config.example.ini` to `config.ini` and fill the parameters.

Token can be generated in your Profile page >> Access tokens

2. Create virtual environment if necessary and install requirements.

```shell
> VENV_PATH=~/.virtualenvs
> python -m venv $VENV_PATH/venv
> source $VENV_PATH/venv/bin/activate
> pip install -r requirements.txt
```

3. Check the script usage: `python main.py -h`

```
usage: main.py [-h] -b BUILD_TYPE -f FILE_PATTERN [-t TARGET_DIR]

options:
  -h, --help            show this help message and exit
  -b BUILD_TYPE, --build-type BUILD_TYPE
                        Built configuration ID
  -f FILE_PATTERN, --file-pattern FILE_PATTERN
                        Artifact file pattern. E.g. pycharmPC-{build}-aarch64.dmg
  -t TARGET_DIR, --target-dir TARGET_DIR
                        [OPTIONAL] Download directory. Default is current workdir
```

`--build-type` -- Can be copied from specific build configuration's settings

![](https://i.imgur.com/Hq9Y8m0.png)

`--file-pattern` -- The name of the artifact to download. Replace the build number with `{build}` placeholder.

E.g. `pycharmPY-{build}-aarch64.dmg`

To download with a single command, add an alias to your shell config.

Example for `.bashrc`/`.zshrc`:

```shell
alias dlcharm="~/.virtualenvs/venv311/bin/python ~/projects/build-master-downloader/main.py \
    -b my_awesome_configuration_id \
    -f pycharmPY-{build}.dmg \
    -t ~/Downloads"
```
