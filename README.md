# Grids and Grains

**Collect sand dollars. Solve puzzles. Build your dream beach.**

Grids and Grains is a creative blend of logic puzzles and customization—solve nonograms to earn sand dollars, then spend them on decorations to personalize your very own beach paradise.

---

## Game Features

### Puzzle System
- **Nonograms** - An option to solve your own **custom** nonograms or pre-drawn ones
- **Pre-drawn nonograms** - A library of **pre-drawn** nonograms to solve
- **Self-drawn nonograms** – Create and publish your own puzzles to solve
- **Rewards** – Earn **100× sand dollars** for every pre-drawn nonogram solved, and **10 sand dollars** for custom ones
- **Automated Crosses** - When a row/column is fufilled, crosses are **automatically** added to all empty pixels in that row/column for convenience 
- **Mobile Friendly** - A toggle to swap between **cross** and **fill** mode as opposed to single and double clicks

### Beach Customization
- **Inventory** – Manage items you own but aren't currently displaying
- **3 Beach Backgrounds** – Choose from different scenic backdrops
- **Blue Box** - Each item complete with a blue box that shows the barrier of collision with edges of the screen
- **Move Tool** - Drag your mouse on the blue box to rearange placed items
- **Rotate and Scale** - Easy-to-use scaling and rotating tools to fully customize your beach
- **Flip** - Allows flipping images on the beach horizontally
- **Remove Tool** – Easily remove placed items, will be stored in inventory upon removal

### Other Features
- **Shop** – Spend sand dollars on decorations and items for your beach
- **Gallery** – View your complete history of created nonograms
- **Sound** - Toggle your background music on and off
- **Information** - Information page to describe how to play, the controls, and a detailed description of how to solve a nonogram

---

## Project Structure

```
nonogram/
├── main.py           # Main game entry point
├── assets/               # All game assets
│   ├── audio/            # Background music and sound effects
│   ├── fonts/            # Custom fonts
│   └── images/           # All image assets
│       ├── backgrounds/  # Beach background images
│       ├── icons/        # UI icons and buttons
│       ├── infos/        # Information/tutorial page images
│       └── shop/         # Shop item images
├── data/                 # Runtime save data (generated)
│   ├── save.txt          # Player progress and settings
│   └── gallery.txt       # Created nonogram history
├── templates/            # Pygbag web build templates
│   ├── index.tmpl
│   └── default.tmpl
├── CONTRIBUTING.md       # Contribution guidelines
├── requirements.txt      # Python dependencies
├── LICENSE               # Project license
└── README.md             # This file
```

---

## Development Setup

### Prerequisites
Make sure you have Python installed on your system.

### Installation
```bash
pip install -r requirements.txt
```

### Running Locally
*Navigate to the project root*

#### Run with Pygame
```bash
python main.py
```

#### Run with Pygbag
```bash
pygbag --template templates/index.tmpl ../nonogram
```

### Build the Website with Pygbag
```bash
pygbag --build --archive ../nonogram
```

After running this command, ensure `title.png` and `favicon.png` (currently in root directory) is placed into all `/web` folders created, including the zipped folder if you wish to run it from there.  
To add it to the zipped folder, you must first unzip it, add it, and then zip it.  
After having built the website once, you may find some files have not been removed. This is expected and you do not need to replace those files with the same file, but you must make sure all files are there.