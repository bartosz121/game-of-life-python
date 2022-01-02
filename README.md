# Conway's Game of Life

Python >=3.10 implementation of [Conway's Game of Life](https://www.conwaylife.com/wiki/Main_Page) using PyQt6
 ![Demo](https://i.imgur.com/8LKTHjZ.gif)

## How to play

Clone the project

```bash
  git clone https://github.com/bartosz121/game-of-life-python
```

Go to the project directory

```bash
  cd game-of-life-python
```

Create new virtual environment

```bash
  python -m venv env
```

Activate environment

```bash
  # on Linux
  source env/bin/activate

  # on Windows
  ./env/Scripts/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Play!

```bash
  python game_of_life/run.py
```

## Demo

 - Start game with random alive cells

 ![Random cells](https://i.imgur.com/kEARdGk.gif)
 - Map editor (example of creating a [Glider](https://www.conwaylife.com/wiki/Glider))

 ![Copperhead spaceship](https://i.imgur.com/kkJc0lV.gif)
 - Load pattern from file in `.cells` or `.rle` format ([Dragon](https://www.conwaylife.com/wiki/Dragon)) you can download a pack of patterns from [here](https://www.conwaylife.com/patterns/all.zip)

 ![Loading Dragon pattern from a file](https://i.imgur.com/MGLLk6V.gif)
 - Rotate loaded pattern ([Copperhead](https://www.conwaylife.com/wiki/Copperhead))

 ![Rotating Copperhead](https://i.imgur.com/ikCECLm.gif)
 - Save pattern to a file (`.cells` or `.rle` format)

 ![Saving and loading a glider](https://i.imgur.com/LoXKpkX.gif)

## Controls
- Press `ESC` to go back or pause while playing
- While playing press `M` to enter `Map Editor`

- ### **Map Editor Controls**
  - `Left Mouse Button` makes clicked cell **alive**
  - `Right Mouse Button` makes clicked cell **dead**
  - Press `M` to exit map editor and start the game
  - When saving a pattern to a file press `Left Mouse Button` once to select starting point, then press `Left Mouse Button` again to choose the end
  - After pattern from a file is loaded press:
    - `Left Mouse Button` to place it in the grid
    - `Right Mouse Button` to transpose it
    - `Middle Mouse Button` to transpose it over the other diagonal


## Settings

You can change window size and interval timer in `run.py` file;
```python
game = GameOfLife(800, 600, timer_interval=120)
```

**All other settings (like cell width/height/color) can be changed in `settings.py` file, inside `Settings` class**

## TODO

- [ ] Implement other game of life algorithms ([hashlife](https://johnhw.github.io/hashlife/index.md.html))
- [ ] Keep settings in JSON file instead of .py
- [ ] Better error handling
- [ ] Copy-Paste feature
- [ ] Change color of the rectangle for each direction when rotating loaded pattern
- [ ] Better GUI
- [ ] Display game data (alive cells, generation)
- [ ] Better performance with large resolution
