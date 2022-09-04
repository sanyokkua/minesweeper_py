# minesweeper_py

Classic Minesweeper game on python and Qt

Implementation of the [Minesweeper Wiki](https://en.wikipedia.org/wiki/Minesweeper_(video_game)) on the Python language.

It is an education project to learn Python as a language, try python tools for UI and build desktop app.

- [The main technologies that were used in the scope of this project](#the-main-technologies-that-were-used-in-the-scope-of-this-project)
- [How this game looks like](#how-this-game-looks-like)
  - [Game Process](#game-process)
  - [Game Over](#game-over)
  - [New Game Dialog](#new-game-dialog)
- [Main functionality of the game](#main-functionality-of-the-game)
- [Technical Information](#technical-information)
  - [Structure of the repository](#structure-of-the-repository)
  - [Test Code Coverage of the Game Core API](#test-code-coverage-of-the-game-core-api)
  - [Build from sources](#build-from-sources)
    - [Prerequisites](#prerequisites)
    - [Build from sources](#build-from-sources-1)
- [TODO in the future](#todo-in-the-future)

# The main technologies that were used in the scope of this project

- Programming Language: Python 3.10.5 (All development was made on the Mac OS X)
- UI Framework: [PyQt6](https://riverbankcomputing.com/software/pyqt/intro)
- Dependency management: [Poetry](https://python-poetry.org/)
- Build tool (Binary distribution of the final APP): [pyinstaller](https://pyinstaller.org/en/stable/)

# How this game looks like

Below you can find screenshots made on Mac OS X

## Game Process

![game-process](docs/new_game_process.png)

## Game Over

![game-over](docs/game_over.png)

## New Game Dialog

![new-game](docs/new_game_dialog.png)

# Main functionality of the game

You as a user of this app (game) has ability to:

- Start New Game (via menu entry or by pressing (Windows/Linux) **ctrl+N** /(Mac OS X) **Command+N**)
- Reset Game (via menu entry or by pressing  (Windows/Linux) **ctrl+R** /(Mac OS X) **Command+R**)
- Exit Game (via menu entry, windows controls or by pressing (Windows/Linux) **ctrl+Q** /(Mac OS X) **Command+Q**))
- During the game process user can:
  - Push button Smile Button - to reset current game (start new game with the same number of mines and field size)
  - Left Mouse Button click on the cell (field button) - opens the cell
  - Right Mouse Button click on the cell (field button) - Put/Remove flag from the cell

# Technical Information

## Structure of the repository

- **docs** - folder with screenshots and should be used for keeping any documentation
- **minesweeper_core** - folder with the base code of the app and provides API to build UI around this API
- **minesweeper_ui** - folder with implementation of the QT UI for the game API
- **tests** - folder contains unittests for the **minesweeper_core**
- [**pyproject.toml**](pyproject.toml) - all the configuration of the project for the package managers and build tools
- [**poetry.lock**](poetry.lock) - lock file with all the dependencies used in the project. More information about
  poetry can be found on their [website](https://python-poetry.org/)
- **minesweeper.spec** - specification for the building application executable

## Test Code Coverage of the Game Core API

![test-coverage](docs/test_coverage.png)

## Build from sources

### Prerequisites

- You should have installed Python to you PC. Python installers and instructions can be found on the official [**Python
  Page**](https://www.python.org/)
- You also should have to install Poetry package manager. Instruction can be found on the official [**Poetry
  page**](https://python-poetry.org/docs/#installation)
- If you want to clone this repository, then probably you also need a [**GIT**](https://git-scm.com/) preinstalled.

### Build from sources

1. Open Terminal on your OS
2. Navigate to the folder with this app

```shell
cd /path/to/the/root/of/minesweeper_py
```

3. Create virtual environment for Python if you want to have all the dependencies preinstalled inside app directory.
   Poetry will automatically create virtual environment, but if you create one inside app folder - poetry will use this
   instead its default.

```shell
python3 -m venv .venv 
```

4. Install dependencies by poetry

```shell
poetry install
```

5. After installation, you should now have ability to start application via entry points created in the scope of
   installation script

```shell
poetry run minesweeper
```

6. To build **PACKAGE** for using in the other projects or to push to cloud package repositories run:

```shell
poetry build
```

It will build **tar.gz** and **.whl** packages

7. To build EXECUTABLES to have game as one executable file for Mac OS or Windows, or any supported OS try this command

```shell
poetry run pyinstaller minesweeper.spec
```

After this command execution in:

- folder **build/minesweeper** you will find build intermediate files
- folder **dist** you will find executable app for your OS where you run the build command (
  Minesweeper.exe/Minesweeper.app)

8. Now you can use a built executable to run the app/game

# TODO in the future

In this project there are plans to add:

- other languages to UI
