# autonogame

Bot for the browser game [Ogame](https://en.ogame.gameforge.com/).

This software is under development. It is capable of building `resources`, `deposits` and `facilities`. New features will be implemented in the future.

It is built on top of the Python module `pyogame` which provides the API to communicate with the game. The GitHub repository is [here](https://github.com/alaingilbert/pyogame).

## Contributing

If you are a developer and you want to contribute to this project you can clone, install and test this software on your Windows or Unix machine.

### Clone

```bash
git clone --recursive git@github.com:tassoneroberto/autonogame.git
cd autonogame
```

### Install

You can install this Python module locally on Windows or Unix.

#### Windows (Powershell)

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install -e .
```

#### Unix

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -e .
```

### Run

You can run the GUI by simply executing the following command:

```bash
autonogame
```

## Build app

A Windows executable `.exe` (or MacOS application `.app`) can be built using the `pyinstaller` software (more info [here](https://pyinstaller.org/en/stable/usage.html#cmdoption-version-file)):

```bash
pyinstaller --clean --noupx -w -F -n autonogame ./src/autonogame/gui.py
```

or you can use the `Make` command:

```bash
make app
```

If you are on a Windows OS and you don't have `Make` already installed you can get it from [CHOCOLATEY](https://chocolatey.org/install):

```powershell
choco install make
```

The `./dist` folder will contain the portable executable.
