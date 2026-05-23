# Sand Grounds v1.1

**Collect sand dollars. Solve puzzles. Build your dream beach.**

Sand Grounds is a creative blend of logic puzzles and customization—solve nonograms to earn sand dollars, then spend them on decorations to personalize your very own beach paradise.

---

## New Aditions (v1.0 -> v1.1)
- **Rotate and Scale** - Easy-to-use scaling and rotating tools to fully customize your beach

---

## Game Features

### Puzzle System
- **Self-drawn nonograms** – Create and publish your own puzzles for others to solve
- **Puzzle Collection** – A library of nonograms to challenge yourself with
- **Gallery** – View your complete history of created nonograms
- **Rewards** – Earn **100× sand dollars** for every puzzle solved

### Beach Customization
- **Shop** – Spend sand dollars on decorations and items for your beach
- **Inventory** – Manage items you own but aren't currently displaying
- **3 Beach Backgrounds** – Choose from different scenic backdrops
- **Blue Box** - Each item complete with a blue box that shows the barrier of collision with edges of the screen
- **Move Tool** - Drag your mouse on the blue box to rearange placed items
- **Rotate and Scale** - Easy-to-use scaling and rotating tools to fully customize your beach
- **Remove Tool** – Easily remove placed items, will be stored in inventory removal

---

## File System

### Pygame Files
**Versions used for saving backup code**: v[update-number].[mini-update-number].[backup-version].py  
**Most recent version**: main.py  
**Game save files**: save.txt, gallery.txt

### Website Files
**Zip file**: build/web.zip  
**Website file**: build/web/index.html

---

## Development Setup

### Prerequisites
Make sure you have Python installed on your system.

### Installation
```bash
pip install pygame
pip install pygbag
```

### Running Locally
#### Run with Pygame
```bash
python main.py
```

#### Run with Pygbag
```bash
pygbag <folder>
```

### Publish with Pygbag
```bash
pygbag --build --archive <folder>
```
