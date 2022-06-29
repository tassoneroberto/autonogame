# autonogame

Bot for the browser game OGame.

<https://en.ogame.gameforge.com/>

This software is under development. It is capable of building `resources`, `deposits` and `facilities`. New features will be implemented in the future.

It is built on top of the Python module `pyogame` which provides the API to communicate with the game. The GitHub repository is [here](https://github.com/alaingilbert/pyogame).

## Installing

You can install this software as a `pip` package and run it from a terminal.

```bash
pip install autonogame
autonogame
```

In alternative you can download and execute the pre-built app (Windows only) by visiting the [Releases](https://github.com/tassoneroberto/autonogame/releases) page.

## Contributing

If you are a developer and you want to contribute to this project you can clone, install and test this software on your Windows or Unix machine.

```bash
git clone git@github.com:tassoneroberto/autonogame.git
cd autonogame
```

You can install this Python module locally on Windows or Unix.

### Windows

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install -e .
```

### Unix

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

A Windows executable `.exe` (or MacOS application `.app`) can be built using the `pyinstaller` software (more info [here](https://pyinstaller.org/en/stable/usage.html#cmdoption-version-file)). The command can be execute using `Make`:

```bash
make build-app
```

If you are on a Windows OS and you don't have `Make` already installed you can get it from [CHOCOLATEY](https://chocolatey.org/install):

```powershell
choco install make
```

The `./app` folder will contain the portable executable.
