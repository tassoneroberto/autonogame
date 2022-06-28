# aut0game

Bot for the browser game [Ogame](https://en.ogame.gameforge.com/).

This software is under development. It is capable of building `resources`, `deposits` and `facilities`. New features will be implemented in the future.

It is built on top of the Python module `pyogame` which provides the API to communicate with the game. The GitHub repository is [here](https://github.com/alaingilbert/pyogame).

## Contributing

If you are a developer and you want to contribute to this project you can clone, install and test this software on your Windows or Unix machine.

### Clone

```bash
git clone --recursive git@github.com:tassoneroberto/aut0game.git
cd aut0game
```

### Install

You can install this Python module locally on Windows or Unix.

#### Windows

```bash
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
aut0game
```

## Build Windows executable

A Windows executable `.exe` can be built by running the following command:

```bash
pyinstaller --onefile --noupx -w --windowed .\gui.py
```
