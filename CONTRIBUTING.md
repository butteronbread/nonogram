# Contributing Guidelines

To contribute to **Grids and Grains**, please ensure your contributions adhere to the following standards to maintain code quality, performance, and readability across the project.

---

## Code Style Guidelines

### 1. Code Reusability (DRY Principle)

Keep the codebase **DRY** (*Don't Repeat Yourself*):

* **Extract Functions:** If a block of code (3+ lines) is repeated in multiple places, refactor it into a dedicated function and replace all duplicate instances with function calls.
* **Use Data Structures for Repeated Logic:** If you find yourself running identical operations on multiple variables (e.g., `x` and `y`), store them in a `list` or `dictionary` and iterate over them using a loop instead.

### 2. Generalization

* Write modular, general-purpose functions wherever possible.
* Avoid hardcoding values or tightly coupling functions to single specific use cases if they can be designed to handle broader scenarios.
* When creating classes, they must be generalized to fit most things the class is used for (e.g. if the class is for buttons, it can and will be used in most buttons)

### Dynamic Screen Scaling (`w` & `h` Variables)

* **Use Relative Coordinates:** Calculate object positions and layout sizes using fractions/multipliers of the screen width (`w`) and height (`h`) rather than hardcoding explicit pixel coordinates (e.g., `w * 0.5` or `h * 0.25`).
* **Styling Exceptions:** Small UI styling properties—such as font sizes, border radii, line thicknesses, and minor padding—may use hardcoded integer values where relative scaling is unnecessary.

### 3. Asset Management & Pygame Performance

* **Single-Pass Asset Loading:** **NEVER** load images, audio, or fonts inside the main game loop. All assets must be loaded **once** inside the `setup` functions and stored for future use.
* **Conditional Transformations:** Avoid calling `pygame.transform` functions (scaling, rotating, flipping) every frame. Image transformations should be pre-rendered during setup or executed strictly behind conditional checks.
* **Rect Instantiation:** Static `pygame.Rect` objects should be created once in `setup` functions. Avoid recreating identical static `Rect` instances multiple times. *(Creating new, dynamic rects during gameplay is allowed).*

### 4. Code Structure & Organization

* **Section Grouping:** Functions are grouped logically by feature/module using comments. Place any new function into its corresponding section.
* **New Sections:** If you add 2 or more related functions that don't fit into existing groups, create a new labeled section header.

### 5. Naming Conventions & Code Style

* **Descriptive Naming:** Use clear, self-explanatory names for variables, functions, and classes that explicitly reflect their purpose.
* **Documenting Ambiguous Names:** If a variable name could be misleading or non-standard due to specific constraints, document its exact role in a comment at the start of the `main` function.
* **Line Length Limit:** Keep code lines under **100 characters** whenever possible to maintain readability.

### 6. Commenting Standards

* **Explain the "Why":** Comment on complex or non-obvious logic. Focus comments on *why* a particular approach was taken, rather than stating what the Python syntax is already doing.

---

## Code Output and Placeholder Guidelines

### 1. Screens
* For this project, there must only be **one** pygame screen - `main.py` - for pygbag and delay time purposes.

### 2. Terminal Usage
* The terminal is for debuging purposes only. All `print` statements must be removed before contributing. Any information meant for the player must be displayed on the `pygame` window instead.

### 3. Comments
* All placeholder comments used to temporarily remove a part of the script must be removed before contributing.

---

## Do Not Change

### 1. File System
* `main.py`, `index.tmpl`, `favicon.png` and `title.png` must stay in `root` directory. This is required in order to run pygbag.

---

## Quality Assurance & Pre-Submission

### 1. Thorough Testing
* **Complete Game Check:** Test all features and edge cases thoroughly before submitting your changes to ensure no new bugs or regressions are introduced.
* **Investigate Intermittent Bugs:** Do not ignore bugs that occurred earlier during testing and seemingly disappeared. They rarely fix themselves—you are likely just testing under slightly different conditions. Trace and resolve the root cause.

### 2. Pygbag Compatibility
* **Web Build Verification:** Always build and test the **Pygbag** version alongside the native Pygame version to ensure visuals, performance, and inputs match seamlessly across both platforms.
* **Debug Tools:** After running Pygbag, open <http://localhost:8000/?-i> instead to have a full overview of everything happening, including `errors` and `print` statements.
* **Local Storage Issues:** If there is an issue regarding storage, go into the website inspector tool and remove or alter the data.