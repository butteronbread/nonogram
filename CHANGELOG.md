# Changelog

## [1.3.2] - 2026-09-6
- New dictionaries initialized in global scope: `FONTSIZES` and `TEXTS`.
  - This increases performance by only initializing fonts and renders once to make up for larger screens.
  - The key for `FONTSIZES` is the exact font, and the value is the font with the key font size with the `FONT` font. This is used in the `TEXTS` dictionary and dynamic texts in the main loop (text where the words will change).
  - The key for `TEXTS` is "[font-size]-[text]", where the value is a `.render`, using the values from `FONTSIZES` as the `pygame.font.Font`. This is used in all static texts.

## [1.3.1] - 2026-09-6

### Added
- Added `self.hide` variable to `Button` class, defined in __init__. It can be set to either `"text"` or `"img"` to hide either one.
- Pop SFX to play every time the player is filling up/erasing a new cell, as well as the audio file `pop.ogg`
- `mul` divider to get the correct scale of everything when changing the screen size

### Changed
- Updated all UI tools for items in the `beach` screen to use the `Button` class
- Updated `CONTRIBUTING.md` to accomodate for the new `mul` scalar

### Fixed
- Rotations in the correct direction even when the item on the beach is flipped using calculations.

## [1.3.0] - 2026-08-20

### Added
- Added key `"sound"` to `save.txt` to keep sound state the same between sessions
- `try` and `except` for seting up the gallery to prevent cases when `gallery.txt` has been cleared but `save.txt` hasn't, so the indexes in `save.txt` are out of range for `gallery.txt`, returning an `IndexError`
- Checking in `setup` function to make sure all items that are needed are in `save.txt`

### Changed
- Sound toggle now mutes and unmutes background music instead of pausing it
- Reordered `galleryBigRects` to be created just before `gallerySmallRects` to accomodate for removal of `IndexError`

---

## [1.2.7] - 2026-08-19

### Changed
- Used a surface for the dropdown for overflowing clues
- Sliding animation for opening and closing dropdown

## [1.2.6] - 2026-08-18

### Added
- When the player first enters the game, there is a dark overlay covering everything but instructions page
  - This forces the user to look through how to play the game and nonogram mechanics
  - The player is not allowed to click anything else before going into the instructions page
  - Condition checked if `save.txt` exists
- Clue dropdown
  - If the column has more than 4 clues, there will be an openable dropdown
  - This prevents overlapping of numbers

### Changed
- More detailed instructions page to make it clearer how to play nonograms

## [1.2.5] - 2026-08-17

### Added
- `Button` class that handles drawing, clicking, hover animation, and modification of buttons, including 2 modes - image and text
- `Text` class, used in all text and the `Button` class for text mode
- `flip_page` function to handle all page flipping, used in `instructions`, `gallery`, `shop`, `add`, and `pick-beach`
- `check_info_done` function that runs every time the state on the board is changed while solving
  - Checks if that clue has been fufilled
  - If it has, the color of the number will be darker on the display

### Changed
- Swapped beach ball and shell image in shop to a better drawing
- Modified `draw_info` to accomodate darker clues if it is finished
- Drawing nonograms is mobile friendly - replaced double click to erase with click again
  - If it starts the stroke on an empty cell, the rest of that stroke will erase any filled cells. Vice versa for filled cells

## [1.2.4] — 2026-08-11

### Changed
- Reorganized project into professional directory structure
- Moved all assets into `assets/` with organized subdirectories (`audio/`, `fonts/`, `images/`)
- Moved save data files into `data/` directory
- Moved pygbag templates into `templates/` directory
- Archived all old version backups into `archive/`
- Updated all file paths in source code to match new structure
- Made font path resolution absolute using `DIRECTORY` for robustness

### Added
- `CONTRIBUTING.md` — contribution guidelines
- `requirements.txt` — Python dependency list
- `CHANGELOG.md` — this file

### Fixed
- Fixed `addInfo()` not clearing old clue data, causing corrupted puzzle hints when solving multiple puzzles in a row

## [1.2.3] — 2026-08-10

### Added
- **Auto-cross** — automatically crosses out empty cells in rows/columns that are already fully solved
- Cross-out animation (cells animate from small to full size when auto-crossed)

### Changed
- Auto-cross now checks against `math.floor()` to avoid interfering with animation states

## [1.2.2] — 2026-08-10

### Changed
- Introduced `DIRECTORY` constant using `os.path.dirname(__file__)` for reliable path resolution
- All asset paths now use `os.path.join(DIRECTORY, ...)` instead of relative strings
- Updated pre-drawn nonogram puzzle set (9 puzzles)

## [1.2.1] — 2026-08-08

### Changed
- Refactored info/clue system to use a unified `infos` dictionary with `"x"` and `"y"` keys
- Combined `xinfo`/`yinfo` lists into a single `infos` dict for cleaner code
- Refactored `addInfo()` to iterate over both axes with a single loop

## [1.2.0] — 2026-08-08

### Changed
- Extracted `addInfo()` into a standalone function for generating row/column clues
- Code cleanup and improved function separation

---

## [1.1.5] — 2026-08-08

### Added
- **Mobile-friendly toggle (XO mode)** — swap between cross ("X") and fill ("O") mode for touch-friendly gameplay
- Heart icon toggle button with `heartO.png` and `heartX.png` indicator images
- Cross-out cell animation (smooth scaling effect when cells are crossed)

### Changed
- Refactored board drawing into `drawBoard()` function with docstring
- Refactored info setup into `setupInfo()` function
- Added comments and docstrings throughout the codebase
- Formatted code for consistent spacing

## [1.1.4] — 2026-08-06

### Changed
- Migrated save system from plain text to **JSON format** (`save.txt` now stores JSON)
- Added `json` and `os` imports
- Save data now uses structured keys: `sanddollar`, `gallery`, `beach_bg`, `inv`, `beach_items`
- Updated all save/load calls throughout the codebase

### Fixed
- Fixed beach item selection requiring mouse-down state check to prevent accidental selection

## [1.1.3] — 2026-08-06

### Added
- **Information page** — tutorial/help page with game instructions and nonogram-solving guide
- Info button on home screen with `info.png` icon
- Multi-page instruction viewer with `infoPage.png` and `infoPageBold.png` backgrounds
- 3 instruction page images (`imgs/infos/0.png`, `1.png`, `2.png`)

### Changed
- Renamed game from "Sand Grounds" to **"Gram of Grain"**
- Extracted `setupOthers()` and `setupHome()` as dedicated setup functions for cleaner initialization

## [1.1.2] — 2026-08-06

### Added
- **Pre-drawn nonogram library** — 9 built-in puzzles encoded as binary strings
- **Choose solve mode** — new screen to pick between pre-drawn and custom nonograms
- `setupChooseSolve()` function with UI for the selection screen

## [1.1.1] — 2026-08-06

### Added
- **Sound toggle** — on/off button on home screen with `on.png` and `off.png` icons
- **Flip tool** — horizontally flip placed beach items
- Flip button with `flip.png` icon on the beach item UI

## [1.1.0] — 2026-08-06

### Added
- **Rotate tool** — rotate placed beach items by dragging
- Rotation tracking with `ogRotation` state variable

### Fixed
- Fixed rotation direction (was rotating the wrong way)
- Fixed type conversion issue in beach data processing

---

## [1.0.4] — 2026-05-18

### Changed
- Code cleanup
- Minor bug fixes and adjustments
- Major beach customization system rework

## [1.0.3] — 2026-05-18

### Added
- **Scale tool** — scale placed beach items by dragging
- Scale and rotate UI buttons displayed on selected beach items
- `display_selected_UI()` function for beach item control overlay

## [1.0.2] — 2026-05-18

### Added
- **Shop purchase animation** — sand dollar deduction animation when buying items
- `shopSDAnimate` and `shopSDAnimateTxt` for animated price display
- Sand dollar counter visible in shop view

## [1.0.1] — 2026-05-18

### Added
- **Cross mark rendering** — cells can now display cross marks to indicate "definitely empty"
- Cross animation when marking cells

### Changed
- Moved all images into `imgs/` subdirectory (organized from root-level files)
- Updated all image paths to use the new directory structure

## [1.0.0] — 2026-03-30

### Added
- Initial release
- Core nonogram puzzle gameplay (15×15 grid)
- Drawing mode to create custom nonograms
- Beach customization scene with background selection
- Shop system with 14 decorative items
- Sand dollar currency with earning and spending
- Gallery to view created nonogram history
- Move tool for placing and repositioning beach items
- Trash tool to remove items (returns to inventory)
- Background music and click/flip sound effects
- Pygbag web build support
