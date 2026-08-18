import pygame, math, random, asyncio, platform, os, time, json
from copy import deepcopy

w = 720

pygame.init()

screen = pygame.display.set_mode((w,w))

clock = pygame.time.Clock()

pygame.display.set_caption("Gram of Grain")

DIRECTORY = os.path.join(os.path.dirname(__file__))

FONT = os.path.join(DIRECTORY, "assets/fonts/font1.ttf")

PREDRAWN = """15 111111111111111100000010000001101001010100101100000010000001101001010111101101111010100101100000010000001111111111111111100000010000001101001010100101100000010000001101111010100101101001010111101100000010000001111111111111111
15 000000000000000000000000000000000000000000000000000000000000000000000000000011100101001110001110111011100000111111111000000010111010000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000
15 000000000000000000011111111100000100000001000000100000010000001000000100000001000001000000010000001110000011111000100000000001001000000000010010000000000010100000000000101000000000000110000000000000100000000000000000000000000
15 000001111100000000111111111000001110000011100011000000000110011000000000110110001000100011110001000100011110001111100011110001000100011110001000100011011000000000110011000000000110001110000011100000111111111000000001111100000
15 000000010000000010000010000010001000010000100000100010001000000010000010000000000111000000000001111100000111101111101111000001111100000000000111000000000010000010000000100010001000001000010000100010000010000010000000010000000
15 000000000000000000000000000000001110000011100001011111110100000110000011000001000000000100010000000000010010001000100010010000000000010010000010000010001000101000100000100000001000000011111110000000000000000000000000000000000
15 000000000000000000001000100000000000101000000001110101011100011111000111110011001101100110011100111001110001111111111100000001111100000000011111110000000110111011000000111101111000000011000110000000000000000000000000000000000
15 000010000010000000001000100000000000111000000000001111100000000010111010000011011111110110000110010011000001100010001100001001010100100111000010110111001011010000100001101010101100000110010011000000011111110000001101111101100
15 000000000000000000001000001110000011100011010000001000110110000000001101100000000011011000001000110110010011101101100111001111011000010000110110000000000111100000000001111110000000011100111000000001000010000000000000000000000""".splitlines()

# testing
#PREDRAWN = """15 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000""".splitlines()

if platform.system() == "Emscripten":
    from js import window
    platform.window.onbeforeunload = None

# save load functions

def save_data(data, file):
    if platform.system() == "Emscripten":
        window.localStorage.setItem(file, data)
    else:
        # PC: Use regular file saving
        with open(os.path.join(DIRECTORY, f"data/{file}.txt"), "w") as f:
            f.write(data)

def load_data(file):
    if platform.system() == "Emscripten":
        saved_data = window.localStorage.getItem(file)
        return saved_data if saved_data else None
    else:
        # PC: Load from file
        file = os.path.join(DIRECTORY, f"data/{file}.txt")
        if os.path.exists(file):
            with open(file, "r") as f:
                return f.read()
        return None

# classes

class Text():
    def __init__(self, text: str, color, size: int, font: str = "assets/fonts/font1.ttf", 
                 x=None, y=None, centerx=None, centery=None):
        self.text = text
        self.color = color
        self.size = size
        self.font = font
        
        self.textbox = None
        self.textpos = None
        
        self.modify(text=text, color=color, size=size, font=font, x=x, y=y, centerx=centerx, centery=centery)

    def modify(self, text: str = None, color = None, size: int = None, font: str = None,
               x: int = None, y: int = None, centerx: int = None, centery: int = None):
        """Modify the text's attributes and update its surface position."""
        if text is not None:
            self.text = text
        if color is not None:
            self.color = color
        if size is not None:
            self.size = size
        if font is not None:
            self.font = font

        font_obj = pygame.font.Font(self.font, self.size)
        self.textbox = font_obj.render(self.text, True, self.color)
        
        if self.textpos is None:
            self.textpos = self.textbox.get_rect()
        else:
            old_center = self.textpos.center
            self.textpos = self.textbox.get_rect(center=old_center)

        if x is not None:
            self.textpos.x = x
        elif centerx is not None:
            self.textpos.centerx = centerx

        if y is not None:
            self.textpos.y = y
        elif centery is not None:
            self.textpos.centery = centery

    def draw(self, surface=None):
        """Draw text onto the target surface (defaults to global screen)."""
        target = surface if surface else screen
        target.blit(self.textbox, self.textpos)

class Button():
    def __init__(self, mode: str, w: int, h: int, color, 
                 border_radius=0, x=None, y=None, centerx=None, centery=None, 
                 text: Text = None, imgFile=None, ogSize=None, hoverSize=None):
        
        self.mode = mode
        self.color = color
        self.border_radius = border_radius
        self.w = w
        self.h = h

        x, y = processCenter(x, y, w, h, centerx, centery)
        self.x = int(x) if x is not None else 0
        self.y = int(y) if y is not None else 0
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        if mode == "text":
            self.text = text
            hover_s = hoverSize if hoverSize is not None else text.size
            self.hoverSize = hover_s
            
            self.hoverText = Text(self.text.text, self.text.color, hover_s, font=self.text.font)

            self.text.modify(centerx=self.rect.centerx, centery=self.rect.centery)
            self.hoverText.modify(centerx=self.rect.centerx, centery=self.rect.centery)

        elif mode == "img":
            og_size = ogSize if ogSize else w
            hover_size = hoverSize if hoverSize else w
            
            raw_img = pygame.image.load(imgFile)
            self.img = pygame.transform.scale(raw_img, (og_size, og_size))
            self.hoverImg = pygame.transform.scale(raw_img, (hover_size, hover_size))

    def draw(self, surface=None):
        """Draws the button onto the screen, checking for hover state."""
        target = surface if surface else screen
        pygame.draw.rect(target, self.color, self.rect, border_radius=self.border_radius)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.mode == "text":
                self.hoverText.draw(target)
            else:
                img_rect = self.hoverImg.get_rect(center=self.rect.center)
                target.blit(self.hoverImg, img_rect)
        else:
            if self.mode == "text":
                self.text.draw(target)
            else:
                img_rect = self.img.get_rect(center=self.rect.center)
                target.blit(self.img, img_rect)

    def get_pressed(self):
        """Checks if the left mouse button is clicked inside the button area."""
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

    def modify(self, x=None, y=None, w=None, h=None, color=None, hoverSize=None, centerx=None, centery=None):
        """Modify button dimensions, colors, and re-center text/image elements."""
        if w is not None:
            self.w = w
        if h is not None:
            self.h = h
        if color is not None:
            self.color = color

        x, y = processCenter(x if x is not None else self.x, 
                             y if y is not None else self.y, 
                             self.w, self.h, centerx, centery)
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        if self.mode == "text":
            if hoverSize is not None:
                self.hoverSize = hoverSize
                self.hoverText.modify(size=self.hoverSize)

            # Re-center text surfaces to updated button rect
            self.text.modify(centerx=self.rect.centerx, centery=self.rect.centery)
            self.hoverText.modify(centerx=self.rect.centerx, centery=self.rect.centery)

def processCenter(x, y, w, h, centerx, centery):
    """Translates center coordinates to top-left (x, y) coordinates."""
    if centerx is not None:
        x = centerx - w // 2
    if centery is not None:
        y = centery - h // 2
    return x, y
# setup functions

def setupBoards(size, cellW, gap):
    boardSolution = [] # answer
    boardSolving = [] # current solving state
    boardRects = [] # rects of each cell in the board
    for y in range(size): # sets up all lists
        boardSolution.append([])
        boardSolving.append([])
        boardRects.append([])
        for x in range(size):
            boardSolution[-1].append(0)
            boardSolving[-1].append(0)
            boardRects[-1].append(pygame.Rect(x*cellW + gap, y*cellW + gap, cellW, cellW))
    
    return boardSolution, boardSolving, boardRects

def setupPlayAnimations(cellW, size):
    crossImg = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/cross.png")), (cellW, cellW))
    cellTimers = [] # if its wrong it flashes red and then fades away as the cell timer goes by
    for y in range(size):
        cellTimers.append([])
        for x in range(size):
            cellTimers[y].append(0)
    
    return crossImg, cellTimers

def setupInfo(size, gap, cellW): # clues for nonogram
    infos = {"x": [], "y": []}
    infoDone = {"x": [], "y": []}

    yinfoRects = []
    for y in range(size):
        yinfoRects.append(pygame.Rect(0, gap+cellW*y+3, gap, cellW-6))

    xinfoRects = []
    for x in range(size):
        xinfoRects.append(pygame.Rect(gap+cellW*x+3, 0, cellW-6, gap))
    
    return infos, yinfoRects, xinfoRects, infoDone

def setupHome():
    playButton = Button("text", w*0.4, w*0.15, "#426334", 
              border_radius=20, centerx=w/2, centery=w*0.35, 
              text=Text("Play", "#abcc9d", 64), hoverSize=72)

    drawButton = Button("text", w*0.3, w*0.12, "#abcc9d", 
                  border_radius=20, centerx=w/2, centery=w*0.55, 
                  text=Text("Draw", "#426334", 48), hoverSize=53)

    playBubble = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/upbubble.png")), (w*0.6, w*0.2))
    drawBubble = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/downbubble.png")), (w*0.6, w*0.2))

    sanddollarRect = pygame.Rect(w*0.63, w*0.02, w*0.35, w*0.1)
    sanddollarImg = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/sanddollar.png")), (w*0.07, w*0.07))

    shopButton = Button("img", w*0.12, w*0.12, "#f8faf7", 20, x=w*0.02, y=w*0.02, 
                        imgFile=os.path.join(DIRECTORY, "assets/images/icons/shop.png"),
                        ogSize=w*0.08, hoverSize=w*0.09)

    galleryButton = Button("img", w*0.12, w*0.12, "#f8faf7", 20, x=w*0.16, y=w*0.02, 
                           imgFile=os.path.join(DIRECTORY, "assets/images/icons/gallery.png"),
                           ogSize=w*0.08, hoverSize=w*0.09)

    beachButton = Button("img", w*0.12, w*0.12, "#f8faf7", 20, x=w*0.02, y=w*0.86, 
                         imgFile=os.path.join(DIRECTORY, "assets/images/icons/beach.png"),
                         ogSize=w*0.08, hoverSize=w*0.09)

    soundButtonRect = pygame.Rect(w*0.86, w*0.86, w*0.12, w*0.12)
    ogSoundImgs = [pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/off.png")), 
                   pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/on.png"))]
    soundImgs = [pygame.transform.scale(ogSoundImgs[1], (w*0.08, w*0.08)), 
                 pygame.transform.scale(ogSoundImgs[0], (w*0.08, w*0.08))]
    soundOn = True

    infoButton = Button("img", w*0.12, w*0.12, "#f8faf7", 20, x=w*0.72, y=w*0.86, 
                             imgFile=os.path.join(DIRECTORY, "assets/images/icons/info.png"),
                             ogSize=w*0.08, hoverSize=w*0.09)

    return playButton, drawButton, playBubble, drawBubble,\
        sanddollarRect, sanddollarImg,\
        shopButton, galleryButton, beachButton,\
        soundButtonRect, ogSoundImgs, soundImgs, soundOn,\
        infoButton

def setupChooseSolve():
    choosePredrawnButton = Button("text", w*0.5, w*0.15, "#426334", 
                          border_radius=20, centerx=w/2, centery=w*0.35, 
                          text=Text("Pre-drawn", "#abcc9d", 64), hoverSize=72)

    chooseCustomRect = pygame.Rect(0,0,w*0.4,w*0.14)
    chooseCustomRect.centerx = w/2
    chooseCustomRect.centery = w*0.55

    return choosePredrawnButton, chooseCustomRect

def setupDarkFade():
    darken = pygame.Surface((w,w), pygame.SRCALPHA)
    darken.fill((0, 0, 0, 0))
    opacity = 0

    fade = pygame.Surface((w,w), pygame.SRCALPHA)
    fade.fill((0, 0, 0, 127))
    fadeo = 127

    return darken, opacity, fade, fadeo

def setupEndScreen():
    yesButton = Button("text", w*0.3, w*0.1, "#9ebd73", 
                       border_radius=20, centerx=w*0.3, centery=w*0.7, 
                       text=Text("Yes", "#344024", 48), hoverSize=56)

    noButton = Button("text", w*0.3, w*0.1, "#bd7573", 
                      border_radius=20, centerx=w*0.7, centery=w*0.7, 
                      text=Text("No", "#402424", 48), hoverSize=56)

    claimSanddollarButton = Button("text", w*0.75, w*0.1, "#9ebd73", 
                                 border_radius=20, centerx=w*0.5, centery=w*0.6, 
                                 text=Text("Yes", "#344024", 48), hoverSize=56)

    return yesButton, noButton, claimSanddollarButton

def setupGallery():
    galleryBg = pygame.Rect(0,0,w*0.9,w*0.9)
    galleryBg.center = (w/2,w/2)
    popupExitRect = pygame.Rect(w*0.83, w*0.07, w*0.1, w*0.1)

    galleryData = []
    galleryBigRects = []
    gallerySmallRects = []
    galleryColors = []

    solveNext = 0

    galleryPage = 0

    flipLeftButton = Button("text", w*0.1, w*0.15, "#5b6b4f", 
                            border_radius=20, centerx=w*0.125, centery=w*0.5, 
                            text=Text("<", "#ffffff", 64), hoverSize=96)

    flipRightButton = Button("text", w*0.1, w*0.15, "#5b6b4f", 
                            border_radius=20, centerx=w*0.875, centery=w*0.5, 
                            text=Text(">", "#ffffff", 64), hoverSize=96)

    return galleryBg, popupExitRect, galleryData,\
        galleryBigRects, gallerySmallRects, galleryColors,\
            solveNext, galleryPage, flipLeftButton, flipRightButton

def setupBeach():
    beachBgImgs = [pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/backgrounds/1.png")), (w,w)),
                   pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/backgrounds/2.png")), (w,w)),
                   pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/backgrounds/3.png")), (w,w))]

    beachConfirmButtonRect = pygame.Rect(w*0.45,w*0.88,w*0.1,w*0.1)
    beachConfirmButtonImg = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/check.png")), (w*0.1,w*0.1))

    mainExitRect = pygame.Rect(w*0.88, w*0.02, w*0.1, w*0.1)

    addButtonRect = pygame.Rect(w*0.02, w*0.88, w*0.1, w*0.1)
    trashButtonRect = pygame.Rect(w*0.14, w*0.88, w*0.1, w*0.1)

    scaleImg = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/scale.png")), (w*0.05,w*0.05))
    scaleRect = pygame.Rect(0, 0, w*0.06, w*0.06)

    rotateImg = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/rotate.png")), (w*0.05,w*0.05))
    rotateRect = pygame.Rect(0, 0, w*0.06, w*0.06)

    flipImg = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/flip.png")), (w*0.05,w*0.05))
    flipRect = pygame.Rect(0, 0, w*0.06, w*0.06)

    trashImgs = [pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/close.png")), (w*0.08, w*0.08)), 
                 pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/open.png")), (w*0.08, w*0.08))]

    addBg = pygame.Rect(0,0,w*0.9,w*0.9)
    addBg.center = (w/2,w/2)

    posOffset = (0,0)

    return beachBgImgs, beachConfirmButtonRect, beachConfirmButtonImg,\
        mainExitRect, addButtonRect,\
        trashButtonRect, trashImgs,\
        addBg, posOffset,\
        rotateImg, scaleImg,\
        rotateRect, scaleRect,\
        flipImg, flipRect

def setupShop():
    shopBg = pygame.Rect(0,0,w*0.9,w*0.9)
    shopBg.center = (w/2,w/2)

    shopPage = 0

    shopItemRects = []
    for i in range(14):
        shopItemRects.append(pygame.Rect(w*0.2+((i%4)%2 * w*0.35), w*0.15+((i%4)//2 * w*0.4), w*0.25, w*0.35))

    shopItemImgs = []
    ogShopItemImgs = []
    for i in range(14):
        shopItemImgs.append(pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, f"assets/images/shop/{i}.png")), 
                                                   (w*0.18, w*0.18)))
        ogShopItemImgs.append(pygame.image.load(os.path.join(DIRECTORY, f"assets/images/shop/{i}.png")))

    shopItemPrice = [300, 100, 500, 300, 1200, 1000, 1000, 200, 200, 300, 300, 200, 500, 200]

    return shopBg, shopPage, shopItemRects, shopItemImgs, ogShopItemImgs, shopItemPrice

def setup():
    tutorial = False
    if load_data("save") == None:
        save_data('{"sanddollar": 0, "gallery": "", "beach_bg": "", "inv": "", "beach_items": ""}', "save") # default save value
        tutorial = True
    if load_data("gallery") == None:
        save_data(" ", "gallery")

    # general purpose
    size = 15 # pixels for the drawing width and height
    
    gap = w*0.122
    cellW = math.floor((w-gap)/size) # gap of 3 on top and left for numbers

    hp = 100

    offset = -500
    acceleration = 1

    down = False
    solveDown = False

    colors = ((185, 191, 153), # not filled
                (75, 83, 32)) # filled and not filled nonogram colors

    crossImg, cellTimers = setupPlayAnimations(cellW, size)

    boardSolution, boardSolving, boardRects = setupBoards(size, cellW, gap)

    infos, yinfoRects, xinfoRects, infoDone = setupInfo(size, gap, cellW)

    darken, opacity, fade, fadeo = setupDarkFade()

    # home screen stuff
    playButton, drawButton,\
        playBubble, drawBubble,\
        sanddollarRect, sanddollarImg,\
        shopButton, galleryButton, beachButton,\
        soundButtonRect, ogSoundImgs, soundImgs, soundOn,\
        infoButton = setupHome()

    # publish image yes no buttons
    yesButton, noButton, claimSanddollarButton = setupEndScreen()

    # gallery stuff
    galleryBg, popupExitRect, galleryData,\
        galleryBigRects, gallerySmallRects,\
        galleryColors, solveNext, galleryPage,\
        flipLeftButton, flipRightButton = setupGallery()

    # beach stuff
    beachBgImgs, beachConfirmButtonRect, beachConfirmButtonImg,\
        mainExitRect, addButtonRect, trashButtonRect, trashImgs,\
        addBg, posOffset,\
        rotateImg, scaleImg,\
        rotateRect, scaleRect,\
        flipImg, flipRect = setupBeach()

    # shop stuff
    shopBg, shopPage,\
        shopItemRects, shopItemImgs, ogShopItemImgs,\
        shopItemPrice = setupShop()

    stage = "home" # index
    r = json.loads(load_data("save"))
    sanddollar = int(r["sanddollar"])

    selecting, clickBg = -1, False

    shopSDAnimate, shopSDAnimateTxt,\
        scaling, rotating, ogRotation = 0, "", False, False, 0

    choosePredrawnButton, chooseCustomRect = setupChooseSolve()

    infoPageBg = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/infoPage.png")), 
                                        (w*0.9,w*0.9))
    infoPageBgBold = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/infoPageBold.png")), 
                                            (w*0.9,w*0.9))
    infoRect = pygame.Rect(166, 236, 160, 30)

    instructionPages = []
    for i in range(7):
        instructionPages.append(pygame.transform.scale(pygame.image.load(
            os.path.join(DIRECTORY, f"assets/images/infos/{i}.png")), (w*0.9,w*0.9)))
    instructionPageNo = 0

    XO = "O"
    heartXOimg = {"O": pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/heartO.png")), (gap, gap)), 
                  "X": pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/heartX.png")), (gap, gap))}
    heartRect = pygame.Rect(0,0,gap,gap)

    checkButtonRect = pygame.Rect(gap*0.1, gap*0.1, gap*0.8, gap*0.8)
    checkButtonImg = pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/check.png")), 
                                            (gap*0.8, gap*0.8))

    drawMode = 1

    clueArrows = {"down": pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/arrowDown.png")), ((cellW-6)*0.9, ((cellW-6)*0.9) * 0.6)),
                  "up": pygame.transform.scale(pygame.image.load(os.path.join(DIRECTORY, "assets/images/icons/arrowUp.png")), ((cellW-6)*0.9, ((cellW-6)*0.9) * 0.6))}

    clueSelected = None

    return size, gap, cellW, hp, drawMode,\
        offset, acceleration, down, solveDown, colors, solveNext,\
        checkButtonRect, checkButtonImg, crossImg,\
        cellTimers, boardSolution, boardSolving, boardRects,\
        infos, yinfoRects, xinfoRects, infoDone, clueArrows, clueSelected,\
        darken, opacity, fade, fadeo,\
        choosePredrawnButton, chooseCustomRect,\
        playButton, drawButton, playBubble, drawBubble,\
        sanddollarRect, sanddollarImg,\
        shopButton, galleryButton, beachButton,\
        yesButton, noButton, claimSanddollarButton,\
        popupExitRect, galleryBg, galleryData,\
        galleryBigRects, gallerySmallRects,\
        galleryColors, galleryPage, flipLeftButton, flipRightButton,\
        beachBgImgs, beachConfirmButtonRect, beachConfirmButtonImg,\
        mainExitRect, addButtonRect, trashButtonRect, trashImgs,\
        addBg, posOffset, shopBg, shopPage,\
        shopItemRects, shopItemImgs, ogShopItemImgs,\
        shopItemPrice, stage, sanddollar,\
        selecting, clickBg,\
        rotateImg, rotateRect, scaleImg, scaleRect, flipImg, flipRect,\
        shopSDAnimate, shopSDAnimateTxt,\
        scaling, rotating, ogRotation,\
        soundButtonRect, ogSoundImgs, soundImgs, soundOn,\
        infoButton, infoPageBg, infoPageBgBold, infoRect,\
        instructionPages, instructionPageNo,\
        XO, heartXOimg, heartRect,\
        tutorial

# other functions

# nonogram functions

def drawBoard(size, screen, colors, board, gap, w, cellW, boardRects, crossImg, cellTimers):
    """Draw the nonogram board, including filled cells, empty cells, crossed out cells, and wrong cells with animations."""
    # 0 = empty, 1 = filled, 2 = crossed out, 2 < x < 3 = animation for crossed out, 3 = wrong

    for y in range(size):
        for x in range(size):
            if board[y][x] == 3: # wrong
                pygame.draw.rect(screen, colors[0], boardRects[y][x])
                surf = pygame.Surface((cellW, cellW), pygame.SRCALPHA)
                surf.fill((252, 93, 93, 4.25*cellTimers[y][x]))
                screen.blit(surf, (boardRects[y][x].x, boardRects[y][x].y))
                cellTimers[y][x] -= 1

                if cellTimers[y][x] <= 0:
                    cellTimers[y][x] = 0
                    board[y][x] = 0

            elif 3 > board[y][x] > 2: # animation for crossed out (range = 2.9 -> 2.1)
                pygame.draw.rect(screen, colors[0], boardRects[y][x])
                newW = (3 - board[y][x]) * cellW
                screen.blit(pygame.transform.scale(crossImg, (newW, newW)), (boardRects[y][x].x + (cellW - newW)/2, boardRects[y][x].y + (cellW - newW)/2))
                board[y][x] -= 0.1

                if board[y][x] < 2.1:
                    board[y][x] = 2

            elif board[y][x] == 2: # crossed out
                pygame.draw.rect(screen, colors[0], boardRects[y][x])
                screen.blit(crossImg, (boardRects[y][x].x, boardRects[y][x].y))

            else: # filled in or empty
                pygame.draw.rect(screen, colors[board[y][x]], boardRects[y][x])

    # the lines
    # thin lines
    for y in range(1,size):
        lineStart = (gap, gap + cellW*y)
        lineEnd = (w, gap + cellW*y)
        pygame.draw.line(screen, (36,51,5), lineStart, lineEnd, 2)

    for x in range(1,size):
        lineStart = (gap + cellW*x, gap)
        lineEnd = (gap + cellW*x, w)
        pygame.draw.line(screen, (36,51,5), lineStart, lineEnd, 2)

    # thick lines
    for y in range(0, size+5, 5):
        lineStart = (gap, gap + cellW*y)
        lineEnd = (w, gap + cellW*y)
        pygame.draw.line(screen, (36,51,5), lineStart, lineEnd, 4)

    for x in range(0, size+5, 5):
        lineStart = (gap + cellW*x, gap)
        lineEnd = (gap + cellW*x, w)
        pygame.draw.line(screen, (36,51,5), lineStart, lineEnd, 4)

def addInfo(size, infos, boardSolution, boardSolving, infoDone):
    # info stuff checking stuff

    for xy in ["x", "y"]:
        for n in range(size): # n is each row/column
            infos[xy].append("")
            infoDone[xy].append([])
            if xy == "x":
                for y in range(size):
                    if boardSolution[y][n] == 0:
                        infos[xy][n] += " "
                    else:
                        infos[xy][n] += "#"
            else:
                for x in range(size):
                    if boardSolution[n][x] == 0:
                        infos[xy][n] += " "
                    else:
                        infos[xy][n] += "#"

            infos[xy][n] = infos[xy][n].split()
            for i in range(len(infos[xy][n])):
                infos[xy][n][i] = str(len(infos[xy][n][i]))
                infoDone[xy][n].append(False)

    return infos, boardSolving, infoDone

def drawInfo(yinfoRects, xinfoRects, size, infos, infoDone, clueArrows, clueSelected, down):
    # check which one selected
    for i, info in enumerate(xinfoRects):
        if info.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not down:
            if clueSelected == i:
                clueSelected = None
            else:
                clueSelected = i
            break

    # draw background for info
    for y in yinfoRects:
        pygame.draw.rect(screen, (52, 74, 36), y, border_top_left_radius=10, border_bottom_left_radius=10)
    
    for x in xinfoRects:
        pygame.draw.rect(screen, (52, 74, 36), x, border_top_left_radius=10, border_top_right_radius=10)

    # y: infos for rows (y stays same, x changes)
    # x: infos for columns (x stays same, y changes)
    for xy in ["y", "x"]:
        for n in range(size):
            if (len(infos[xy][n]) < 5 and xy == "x") or xy == "y":
                for i in range(len(infos[xy][n])):
                    if infoDone[xy][n][i]:
                        text = pygame.font.Font(FONT, 24).render((infos[xy][n][i]), True, "#80917a")
                    else:
                        text = pygame.font.Font(FONT, 24).render((infos[xy][n][i]), True, "#ffffff")

                    # position of rect + width * multiplier depending on which one it is
                    if xy == "y":
                        textpos = text.get_rect(centerx = yinfoRects[n].x + yinfoRects[n].w * (i+0.5) / len(infos[xy][n]), 
                                                centery = yinfoRects[n].centery)
                    else:
                        textpos = text.get_rect(centerx = xinfoRects[n].centerx, 
                                                centery = xinfoRects[n].y + xinfoRects[n].h * (i+0.5) / len(infos[xy][n]))
                    screen.blit(text, textpos)

            else:
                for i in range(3):
                    if infoDone[xy][n][i]:
                        text = pygame.font.Font(FONT, 24).render((infos[xy][n][i]), True, "#80917a")
                    else:
                        text = pygame.font.Font(FONT, 24).render((infos[xy][n][i]), True, "#ffffff")

                    textpos = text.get_rect(centerx = xinfoRects[n].centerx, 
                                            centery = xinfoRects[n].y + xinfoRects[n].h * (i+0.5) / 4)

                    screen.blit(text, textpos)

                if clueSelected == n:
                    pygame.draw.rect(screen, (52, 74, 36), 
                                     ( xinfoRects[n].x, xinfoRects[n].y + xinfoRects[n].h - 10, # y: bottom edge - border radius
                                       xinfoRects[n].w, xinfoRects[n].h * (len(infos[xy][n])-3) / 4 + 10 ),
                                     border_top_left_radius=10, border_bottom_left_radius=10)

                    for i in range(len(infos[xy][n])-3):
                        if infoDone[xy][n][i]:
                            text = pygame.font.Font(FONT, 24).render((infos[xy][n][i+3]), True, "#80917a")
                        else:
                            text = pygame.font.Font(FONT, 24).render((infos[xy][n][i+3]), True, "#ffffff")
    
                        textpos = text.get_rect(centerx = xinfoRects[n].centerx, 
                                                centery = xinfoRects[n].y + xinfoRects[n].h * (i+3.5) / 4)
    
                        screen.blit(text, textpos)

                    screen.blit(clueArrows["up"], (xinfoRects[n].centerx - clueArrows["down"].get_width()/2,
                                                   xinfoRects[n].y + xinfoRects[n].h * len(infos[xy][n]) / 4))
                else:
                    screen.blit(clueArrows["down"], (xinfoRects[n].centerx - clueArrows["down"].get_width()/2,
                                                     xinfoRects[n].y + xinfoRects[n].h * 3 / 4))

    return clueSelected

def textAnimations(offset, acceleration):
    """Animation for moving the text across the screen"""
    offset += acceleration
    
    if w/2+offset < w/8:
        acceleration += 0.2
    elif w/2+offset < w/4*3:
        if acceleration > 5:
            acceleration /= 1.02
    else:
        acceleration += 0.2

    return offset, acceleration

def autoCross(boardSolving, boardSolution, size):
    """Automatically crosses out empty cells in rows/columns that already fit all requirements"""
    for y in range(size): # rows
        same = True
        for x in range(size):
            if boardSolving[y][x] != boardSolution[y][x] and math.floor(boardSolving[y][x]) != 2:
                same = False

        if same:
            for x in range(size):
                if boardSolving[y][x] == 0:
                    boardSolving[y][x] = 2.9

    for x in range(size):
        same = True
        for y in range(size):
            if boardSolving[y][x] != boardSolution[y][x] and math.floor(boardSolving[y][x]) != 2:
                same = False

        if same:
            for y in range(size):
                if boardSolving[y][x] == 0:
                    boardSolving[y][x] = 2.9

    return boardSolving

def check_info_done(infoDone, boardSolving, boardSolution, infos):
    size = len(boardSolution)

    solving = deepcopy(boardSolving)
    # processing data
    # 0 = empty, 1 = filled, 2 = crossed out, 2 < x < 3 = animation for crossed out, 3 = wrong
    for y in range(size):
        for x in range(size):
            if solving[y][x] >= 2: # make format match boardSolution
                solving[y][x] = 0

    # rows
    # getting data
    markers = {"x": [], "y": []} # 1d: every row, 2d: every run, 3d: start, end pos
    start = None
    end = None
    for xy in ["x", "y"]:
        for a1 in range(size): # axis 1 (x or y)
            markers[xy].append([])
            for a2 in range(size): # axis 2
                if xy == "y":
                    # a1 = row (y), a2 = col (x)
                    if boardSolution[a1][a2] == 1 and (a2 == 0 or boardSolution[a1][a2-1] == 0):
                        start = a2
                    if boardSolution[a1][a2] == 1 and (a2 == size-1 or boardSolution[a1][a2+1] == 0):
                        end = a2
                else:
                    # a1 = col (x), a2 = row (y)
                    if boardSolution[a2][a1] == 1 and (a2 == 0 or boardSolution[a2-1][a1] == 0):
                        start = a2
                    if boardSolution[a2][a1] == 1 and (a2 == size-1 or boardSolution[a2+1][a1] == 0):
                        end = a2

                if start is not None and end is not None:
                    markers[xy][a1].append([start, end])
                    start, end = None, None

    # applying data
    for xy in ["y", "x"]:
        for a1 in range(size):
            for run in range(len(markers[xy][a1])):
                done = True
                for a2 in range(markers[xy][a1][run][0], markers[xy][a1][run][1] + 1):
                    # "y": a1 is row (y) and a2 is col (x)
                    # "x": a1 is col (x) and a2 is row (y)
                    row, col = (a1, a2) if xy == "y" else (a2, a1)
                    
                    if boardSolving[row][col] == 0:
                        done = False

                infoDone[xy][a1][run] = done
    
    return infoDone

# beach functions

def beach_setup(shopItemImgs, ogShopItemImgs, stage):
    """Loads the beach data every time something has changed"""

    r = json.loads(load_data("save"))
    beachBgNo = 0
    beachData = ""

    beachBgNo = r["beach_bg"]
    beachData = r["beach_items"]

    if beachBgNo == '': # if user didnt pick a beach yet
        stage = "pick-beach"
        beachBgNo = 0
    else:
        beachBgNo = int(beachBgNo)

    # process beach data into list: [imgNo, [x, y, scale, rotation, flip (true/false)]]
    beachItemRects = []
    
    beachData = beachData.split()
    for i in range(len(beachData)):
        beachData[i] = beachData[i].split("/")
        beachData[i][0] = int(beachData[i][0])

        beachData[i][1] = beachData[i][1].split("-")

        # convert to datatypes
        beachData[i][1][0] = int(beachData[i][1][0]) # x
        beachData[i][1][1] = int(beachData[i][1][1]) # y
        beachData[i][1][2] = float(beachData[i][1][2]) # scale
        beachData[i][1][3] = int(beachData[i][1][3]) # rotation
        beachData[i][1][4] = int(beachData[i][1][4]) # flip

        # transform image
        shopItemImgs[beachData[i][0]] = \
            pygame.transform.rotate(
                pygame.transform.scale(
                    ogShopItemImgs[beachData[i][0]], # the image
                    (w*0.2 * beachData[i][1][2],  w*0.2*beachData[i][1][2])), # default size (w*0.2) * multiplier scale
                    beachData[i][1][3]) # rotation

        # processed data in rects for collision detection
        beachItemRects.append(pygame.Rect(beachData[i][1][0], 
                                          beachData[i][1][1], 
                                          w*0.2 * beachData[i][1][2],  
                                          w*0.2*beachData[i][1][2]))
    
    if stage != "pick-beach":
        stage = "beach"

    moveItem = [] # what item is being moved. the last item is layered on the top on the screen, so it will be moved

    return beachBgNo, beachData, beachItemRects, moveItem, stage

def display_selected_UI(beachItemRects, selecting, scaleRect, scaleImg, rotateRect, rotateImg, flipRect, flipImg, scaling, rotating, beachData, ogRotation, down):
    """Display the scale, rotate and flip button for the beach item currently selected"""

    # draw the UI rects
    pygame.draw.rect(screen, (100,100,255), beachItemRects[selecting], 5)

    pygame.draw.rect(screen, "#768F74", scaleRect, border_radius=10)
    screen.blit(scaleImg, (scaleRect.x+w*0.005, scaleRect.y+w*0.005))

    pygame.draw.rect(screen, "#A3BF9F", rotateRect, border_radius=10)
    screen.blit(rotateImg, (rotateRect.x+w*0.005, rotateRect.y+w*0.005))

    pygame.draw.rect(screen, "#8CB48A", flipRect, border_radius=10)
    screen.blit(flipImg, (flipRect.x+w*0.005, flipRect.y+w*0.005))

    # check if the buttons are pressed and set variables
    if scaleRect.collidepoint(pygame.mouse.get_pos())\
        and pygame.mouse.get_pressed()[0]\
            and not rotating and not scaling:
        scaling = True

    if rotateRect.collidepoint(pygame.mouse.get_pos())\
        and pygame.mouse.get_pressed()[0]\
            and not scaling and not rotating:
        rotating = True
        ogRotation = beachData[selecting][1][3]

    # flip button
    if flipRect.collidepoint(pygame.mouse.get_pos())\
        and pygame.mouse.get_pressed()[0]\
            and not scaling and not rotating and not down: # prevent accidentally press
        
        beachData[selecting][1][4] = (str((beachData[selecting][1][4] + 1) % 2)) # if its 0, set to 1, vice versa
        
        r = json.loads(load_data("save"))

        r["beach_items"] = r["beach_items"].split()

        r["beach_items"][selecting] = r["beach_items"][selecting].split("-") # process data into list
        r["beach_items"][selecting][4] = str(beachData[selecting][1][4]) # change data
        r["beach_items"][selecting] = "-".join(r["beach_items"][selecting])

        r["beach_items"] = " ".join(r["beach_items"])

        save_data(json.dumps(r), "save")
    
    return scaling, rotating, ogRotation

def scale_beach_img(beachData, selecting, beachItemRects, shopItemImgs, ogShopItemImgs, rotateRect, scaleRect, flipRect, moveItem):
    """Scales the selected beach item based on mouse position and updates the rect and image accordingly, as well as the UI."""
    # take the diff between mouse and rect. divide by default size to get multiplier
    beachData[selecting][1][2] = (pygame.mouse.get_pos()[0] - beachItemRects[selecting].x) / (w*0.2)

    # scale image to new size
    shopItemImgs[beachData[selecting][0]] = \
        pygame.transform.scale(ogShopItemImgs[beachData[selecting][0]],
                               (w*0.2 * beachData[selecting][1][2],  
                                w*0.2 * beachData[selecting][1][2]))

    # scale rect to new size
    beachItemRects[selecting] = \
        pygame.Rect(beachData[selecting][1][0], 
                    beachData[selecting][1][1], 
                    w*0.2 * beachData[selecting][1][2],  
                    w*0.2 * beachData[selecting][1][2])

    # reposition UI
    scaleRect.centerx = beachItemRects[moveItem[-1]].x + beachItemRects[moveItem[-1]].w
    scaleRect.centery = beachItemRects[moveItem[-1]].y + beachItemRects[moveItem[-1]].h

    rotateRect.centerx = beachItemRects[moveItem[-1]].x
    rotateRect.centery = beachItemRects[moveItem[-1]].y + beachItemRects[moveItem[-1]].h

    flipRect.centerx = beachItemRects[moveItem[-1]].x + beachItemRects[moveItem[-1]].h
    flipRect.centery = beachItemRects[moveItem[-1]].y

    # save the data
    r = json.loads(load_data("save"))
    
    r["beach_items"] = r["beach_items"].split()
    r["beach_items"][moveItem[-1]] = f"{beachData[moveItem[-1]][0]}/{beachData[moveItem[-1]][1][0]}-{beachData[moveItem[-1]][1][1]}-{beachData[moveItem[-1]][1][2]}-{beachData[moveItem[-1]][1][3]}-{beachData[moveItem[-1]][1][4]}"
    
    r["beach_items"] = " ".join(r["beach_items"])

    save_data(json.dumps(r), "save")

    return scaleRect, rotateRect, flipRect, beachItemRects

def move_beach_item(moveItem, beachData, posOffset, beachItemRects, scaleRect, rotateRect, flipRect):
    """Moves the selected beach item based on mouse position and updates the rect accordingly, as well as the UI."""

    selecting = moveItem[-1] # takes the last item in the list, which is the image layered on top in the screen

    # gets new position
    beachData[moveItem[-1]][1][0] = pygame.mouse.get_pos()[0] - posOffset[0]
    beachData[moveItem[-1]][1][1] = pygame.mouse.get_pos()[1] - posOffset[1]

    # checks if new position is out of bounds
    if beachData[moveItem[-1]][1][0] < 0: # left bound
        beachData[moveItem[-1]][1][0] = 0

    if beachData[moveItem[-1]][1][1] < 0: # top bound
        beachData[moveItem[-1]][1][1] = 0

    if beachData[moveItem[-1]][1][0] + beachData[moveItem[-1]][1][2] * w*0.2 > w: # right bound
        beachData[moveItem[-1]][1][0] = int(w - beachData[moveItem[-1]][1][2] * w*0.2)

    if beachData[moveItem[-1]][1][1] + beachData[moveItem[-1]][1][2] * w*0.2 > w: # bottom bound
        beachData[moveItem[-1]][1][1] = int(w - beachData[moveItem[-1]][1][2] * w*0.2)

    # save data
    r = json.loads(load_data("save"))
    
    r["beach_items"] = r["beach_items"].split()
    r["beach_items"][moveItem[-1]] = f"{beachData[moveItem[-1]][0]}/{beachData[moveItem[-1]][1][0]}-{beachData[moveItem[-1]][1][1]}-{beachData[moveItem[-1]][1][2]}-{beachData[moveItem[-1]][1][3]}-{beachData[moveItem[-1]][1][4]}"
    
    r["beach_items"] = " ".join(r["beach_items"])

    save_data(json.dumps(r), "save")

    # update rects
    beachItemRects[moveItem[-1]].x = beachData[moveItem[-1]][1][0]
    beachItemRects[moveItem[-1]].y = beachData[moveItem[-1]][1][1]

    # update UI
    scaleRect.centerx = beachItemRects[moveItem[-1]].x + beachItemRects[moveItem[-1]].w
    scaleRect.centery = beachItemRects[moveItem[-1]].y + beachItemRects[moveItem[-1]].h

    rotateRect.centerx = beachItemRects[moveItem[-1]].x
    rotateRect.centery = beachItemRects[moveItem[-1]].y + beachItemRects[moveItem[-1]].h

    flipRect.centerx = beachItemRects[moveItem[-1]].x + beachItemRects[moveItem[-1]].w
    flipRect.centery = beachItemRects[moveItem[-1]].y

    return selecting, scaleRect, rotateRect, flipRect

def beach_trash_button(moveItem, beachData, trashButtonRect, trashImgs, selecting, stage):
    """When beach item is added to trash, remove it from the beach and add it to the inventory, then save the data."""

    pygame.draw.rect(screen, (173, 78, 78), trashButtonRect, border_radius=20)

    if trashButtonRect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(trashImgs[1], (trashButtonRect.x+w*0.01, trashButtonRect.y+w*0.01))

        if moveItem != [] and not pygame.mouse.get_pressed()[0]:
            stage = "beach setup"

            # save data - remove from beach items and add to inv
            r = json.loads(load_data("save"))

            r["beach_items"] = r["beach_items"].split()
            r["beach_items"].pop(moveItem[-1])
            r["beach_items"] = " ".join(r["beach_items"])

            r["inv"] = r["inv"].split()
            r["inv"].append(str(beachData[moveItem[-1]][0]))
            r["inv"] = " ".join(r["inv"])

            save_data(json.dumps(r), "save")

            selecting = -1

    else:
        screen.blit(trashImgs[0], (trashButtonRect.x+w*0.01, trashButtonRect.y+w*0.01))
    
    return selecting, stage

def beach_add_button(addButtonRect, stage, clickSFX, down):
    """If add button is pressed, go to add setup stage to add an item to the beach."""
    pygame.draw.rect(screen, (126, 166, 119), addButtonRect, border_radius=20)

    if addButtonRect.collidepoint(pygame.mouse.get_pos()) and not down:
        text = pygame.font.Font(FONT, 96).render("+", True, (255,255,255))
        textpos = text.get_rect(centerx=addButtonRect.centerx, centery=addButtonRect.centery-w*0.01)
        screen.blit(text, textpos)
        
        if pygame.mouse.get_pressed()[0]:
            stage = "add setup"
            clickSFX.play()

    else:
        text = pygame.font.Font(FONT, 64).render("+", True, (255,255,255))
        textpos = text.get_rect(centerx=addButtonRect.centerx, centery=addButtonRect.centery-w*0.01)
        screen.blit(text, textpos)
    
    return stage

# general purpose

def exit_button(exitRect, clickSFX, stage, down, target):
    """An exit button that changes the stage to the target stage when clicked."""
    pygame.draw.rect(screen, (222, 130, 126), exitRect, border_radius=20) # draw button

    if exitRect.collidepoint(pygame.mouse.get_pos()) and not down: # on hover
        text = pygame.font.Font(FONT, 64).render("X", True, (255,255,255))
        textpos = text.get_rect(centerx=exitRect.centerx, centery=exitRect.centery)
        screen.blit(text, textpos)
        
        if pygame.mouse.get_pressed()[0]: # clicked
            clickSFX.play()
            stage = target # change stage

    else: # not hovered
        text = pygame.font.Font(FONT, 48).render("X", True, (255,255,255))
        textpos = text.get_rect(centerx=exitRect.centerx, centery=exitRect.centery)
        screen.blit(text, textpos)
    
    return stage

def flip_page(changePage, maxPages, flipRightButton, flipLeftButton, sfx, down, show=False):
    if changePage > 0 or show:
        flipLeftButton.draw()

        if flipLeftButton.get_pressed() and not down:
            changePage -= 1
            sfx.play()

    if changePage < maxPages or show:
        flipRightButton.draw()

        if flipRightButton.get_pressed() and not down:
            changePage += 1
            sfx.play()

    return changePage

# pages

async def main():
    # acceleration: the acceleration of the animation before solving
    # galleryColors: holds data of the images in the gallery (which one is 0 or 1)
    # clickBg: if the background is selected to unselect items on the beach

    size, gap, cellW, hp, drawMode,\
        offset, acceleration, down, solveDown, colors, solveNext,\
        checkButtonRect, checkButtonImg, crossImg,\
        cellTimers, boardSolution, boardSolving, boardRects,\
        infos, yinfoRects, xinfoRects, infoDone, clueArrows, clueSelected,\
        darken, opacity, fade, fadeo,\
        choosePredrawnButton, chooseCustomRect,\
        playButton, drawButton, playBubble, drawBubble,\
        sanddollarRect, sanddollarImg,\
        shopButton, galleryButton, beachButton,\
        yesButton, noButton, claimSanddollarButton,\
        popupExitRect, galleryBg, galleryData,\
        galleryBigRects, gallerySmallRects,\
        galleryColors, galleryPage, flipLeftButton, flipRightButton,\
        beachBgImgs, beachConfirmButtonRect, beachConfirmButtonImg,\
        mainExitRect, addButtonRect, trashButtonRect, trashImgs,\
        addBg, posOffset, shopBg, shopPage,\
        shopItemRects, shopItemImgs, ogShopItemImgs,\
        shopItemPrice, stage, sanddollar,\
        selecting, clickBg,\
        rotateImg, rotateRect, scaleImg, scaleRect, flipImg, flipRect,\
        shopSDAnimate, shopSDAnimateTxt,\
        scaling, rotating, ogRotation,\
        soundButtonRect, ogSoundImgs, soundImgs, soundOn,\
        infoButton, infoPageBg, infoPageBgBold, infoRect,\
        instructionPages, instructionPageNo,\
        XO, heartXOimg, heartRect,\
        tutorial = setup()

    # load music and sfx
    pygame.mixer.music.load(os.path.join(DIRECTORY, "assets/audio/bgm.ogg"))
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play(-1)

    clickSFX = pygame.mixer.Sound(os.path.join(DIRECTORY, "assets/audio/click.ogg"))
    clickSFX.set_volume(0.2)
    flipSFX = pygame.mixer.Sound(os.path.join(DIRECTORY, "assets/audio/flip.ogg"))
    flipSFX.set_volume(0.3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        
        screen.fill((224, 232, 218))

        if stage == "home": # home page
            # money
            sanddollarRect = pygame.Rect(w*0.63, w*0.02, w*0.35, w*0.1)

            pygame.draw.rect(screen, (248, 250, 247), sanddollarRect, border_radius=20)
            screen.blit(sanddollarImg, (sanddollarRect.x+w*0.02, sanddollarRect.centery-w*0.035))

            sdShowTxt = str(sanddollar)
            if len(sdShowTxt) > 9:
                sdShowTxt = str(int(sanddollar/1000000))+"M"
            elif len(sdShowTxt) > 5:
                sdShowTxt = str(int(sanddollar/1000))+"K"

            text = pygame.font.Font(FONT, 48).render(sdShowTxt, True, (66, 99, 52))
            textpos = text.get_rect(x=sanddollarRect.x+w*0.12, centery=sanddollarRect.centery-w*0.003)
            screen.blit(text, textpos)

            # shop
            shopButton.draw()

            if shopButton.get_pressed():
                stage = "shop"
                clickSFX.play()
            
            # gallery
            galleryButton.draw()
            
            if galleryButton.get_pressed():
                stage = "gallery setup"
                clickSFX.play()
            
            # beach
            beachButton.draw()
                        
            if beachButton.get_pressed():
                stage = "beach setup"
                clickSFX.play()
        
            # sound
            pygame.draw.rect(screen, (248, 250, 247), soundButtonRect, border_radius=20)

            if soundButtonRect.collidepoint(pygame.mouse.get_pos()):
                soundImgs = pygame.transform.scale(ogSoundImgs[soundOn], (w*0.09, w*0.09))

                if pygame.mouse.get_pressed()[0] and not down:
                    soundOn = not soundOn

                    if not soundOn:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

            else:
                soundImgs = pygame.transform.scale(ogSoundImgs[soundOn], (w*0.08, w*0.08))
            
            screen.blit(soundImgs, (soundButtonRect.centerx - soundImgs.get_size()[0]/2,
                                    soundButtonRect.centery-soundImgs.get_size()[1]/2))

            # info button
            infoButton.draw()
                        
            if infoButton.get_pressed():
                stage = "info"
                clickSFX.play()

            # play button
            playButton.draw()

            if playButton.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(playBubble, (w*0.2, playButton.y - w*0.2))

                text = pygame.font.Font(FONT, 24).render("Solve a nonogram", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=playButton.y - w*0.15)
                screen.blit(text, textpos)

                text = pygame.font.Font(FONT, 24).render("Earn sand dollars", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=playButton.y - w*0.1)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    stage = "choose-solve"
                    clickSFX.play()

            # draw button
            drawButton.draw()
            
            if drawButton.rect.collidepoint(pygame.mouse.get_pos()):

                screen.blit(drawBubble, (w*0.2, drawButton.y + w*0.12))

                text = pygame.font.Font(FONT, 24).render("Draw and solve your own nonogram", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=drawButton.y + w*0.21)
                screen.blit(text, textpos)

                text = pygame.font.Font(FONT, 24).render("Doesn't earn sand dollars", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=drawButton.y + w*0.26)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    stage = "animation-for-draw"
                    clickSFX.play()

            if tutorial:
                stage = "home"
                fade.fill((0,0,0,100))
                screen.blit(fade)

                infoButton.draw()
                                        
                if infoButton.get_pressed():
                    stage = "info"
                    clickSFX.play()
                    tutorial = False

        elif stage == "info": # info page
            pygame.draw.rect(screen, (241, 245, 237), galleryBg, border_radius=10)
            
            screen.blit(infoPageBg, (w*0.05,w*0.05))

            if infoRect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(infoPageBgBold, (w*0.05,w*0.05))

                if pygame.mouse.get_pressed()[0] and not down:
                    stage = "instructions"
                    clickSFX.play()
            
            stage = exit_button(popupExitRect, clickSFX, stage, down, "home")

        elif stage == "instructions": # instructions page
            pygame.draw.rect(screen, (241, 245, 237), galleryBg, border_radius=10)
            
            screen.blit(instructionPages[instructionPageNo], (w*0.05,w*0.05))

            instructionPageNo = flip_page(instructionPageNo, len(instructionPages)-1, 
                                          flipRightButton, flipLeftButton, flipSFX, down)

            stage = exit_button(popupExitRect, clickSFX, stage, down, "info")

        elif stage.split()[0] == "gallery": # view solved nonograms in gallery
            pygame.draw.rect(screen, (241, 245, 237), galleryBg, border_radius=10)

            if len(stage.split()) > 1 and stage.split()[1] == "setup":
                # gallery data and rects
                galleryData = []
                galleryBigRects = [] # rects holding the whole nonogram puzzle
                gallerySmallRects = [] # individual rects inside the big rects representing each cell of the nonogram
                galleryColors = []

                saveR = json.loads(load_data("save")) # save file read
                galleryR = load_data("gallery").strip().splitlines() # gallery file read
                
                galleryData = saveR["gallery"].split("-")

                # if there is IndexError here, check the save.txt
                if galleryData != [""]:
                    data = ""
                    for i in range(len(galleryData)):
                        # w*0.2 = left margin, i%4 because 2*2 = 4, and 4 is the nonogram per page
                        # %2 because 2 columns, //2 because 2 rows
                        galleryBigRects.append(pygame.Rect(w*0.2+((i%4)%2 * w*0.35),
                                                           w*0.2+((i%4)//2 * w*0.35), 
                                                           w*0.25, # size
                                                           w*0.25))

                        if galleryData[i][0] == "p": # where to get the data from
                            galleryData[i] = galleryData[i][1:]
                            data = PREDRAWN[int(galleryData[i])].split(" ")
                        else:
                            data = galleryR[int(galleryData[i])].split(" ")
                        datasize = int(data[0]) # SMTH WRONG HERE HELPPPPP
                        data = data[1]

                        dataW = (galleryBigRects[-1].w - w*0.02)/datasize

                        gallerySmallRects.append([])
                        for y in range(datasize):
                            for x in range(datasize):
                                gallerySmallRects[-1].append(
                                    pygame.Rect( # w*0.01 = margin
                                        galleryBigRects[-1].x + w*0.01 + dataW*x,
                                        galleryBigRects[-1].y + w*0.01 + dataW*y,
                                        dataW, 
                                        dataW))
                        
                        galleryColors.append(list(data))

                    stage = "gallery"
                    galleryPage = 0

            # display the gallery
            for y in range(galleryPage*4,galleryPage*4+4):
                if len(galleryBigRects) > y:
                    pygame.draw.rect(screen, (60, 64, 57), galleryBigRects[y], border_radius=10)

                    for x in range(len(gallerySmallRects[y])):
                        if x == 0:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], 
                                             gallerySmallRects[y][x], border_top_left_radius=10)
                        elif x == datasize-1:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], 
                                             gallerySmallRects[y][x], border_top_right_radius=10)
                        elif x == datasize**2-datasize:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], 
                                             gallerySmallRects[y][x], border_bottom_left_radius=10)
                        elif x == datasize**2-1:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], 
                                             gallerySmallRects[y][x], border_bottom_right_radius=10)
                        else:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], 
                                             gallerySmallRects[y][x])

            galleryPage = flip_page(galleryPage, (len(galleryBigRects)-1)//4, 
                                    flipRightButton, flipLeftButton, flipSFX, down)

            stage = exit_button(popupExitRect, clickSFX, stage, down, "home")

        elif stage == "shop": # buy items for beach
            pygame.draw.rect(screen, (249, 250, 242), shopBg, border_radius=10)

            for i in range(shopPage*4,shopPage*4+4):
                if len(shopItemRects) > i:
                    pygame.draw.rect(screen, (204, 209, 171), 
                                     shopItemRects[i], border_radius=10)

                    if shopItemRects[i].collidepoint(pygame.mouse.get_pos()):
                        shopItemImgs[i] = pygame.transform.scale(ogShopItemImgs[i], (w*0.2, w*0.2))
                        screen.blit(shopItemImgs[i], (shopItemRects[i].centerx - w*0.1, 
                                                      shopItemRects[i].centery - w*0.15))

                        if pygame.mouse.get_pressed()[0] and not down:
                            if sanddollar >= shopItemPrice[i]:
                                # animation start + sfxs
                                shopSDAnimateTxt = str(shopItemPrice[i])
                                shopSDAnimate = 20
                                clickSFX.play()

                                r = json.loads(load_data("save"))

                                # adding item to inventory
                                r["inv"] = r["inv"].split(" ")
                                r["inv"].append(str(i))

                                r["inv"] = " ".join(r["inv"])
                                r["inv"] = r["inv"].strip(" ")

                                # minus money
                                sanddollar -= shopItemPrice[i]
                                r["sanddollar"] = str(sanddollar)

                                save_data(json.dumps(r), "save")
                    
                    else:
                        shopItemImgs[i] = pygame.transform.scale(ogShopItemImgs[i], (w*0.18, w*0.18))
                        screen.blit(shopItemImgs[i], (shopItemRects[i].centerx - w*0.09, 
                                                      shopItemRects[i].centery - w*0.14))

                    text = pygame.font.Font(FONT, 48).render("$"+str(shopItemPrice[i]), 
                                                             True, (80, 82, 66))
                    textpos = text.get_rect(centerx=shopItemRects[i].centerx, 
                                            centery=shopItemRects[i].centery + w*0.1)
                    screen.blit(text, textpos)

            shopPage = flip_page(shopPage, (len(shopItemRects)-1)//4, 
                                 flipRightButton, flipLeftButton, flipSFX, down)

            # display sand dollars
            sanddollarRect = pygame.Rect(w*0.04, w*0.02, w*0.35, w*0.1)

            pygame.draw.rect(screen, "#CAD4C5", sanddollarRect, border_radius=20)
            screen.blit(sanddollarImg, (sanddollarRect.x+w*0.02, 
                                        sanddollarRect.centery-w*0.035))

            # if go over then change to K or M for thousand and million
            sdShowTxt = str(sanddollar)
            if len(sdShowTxt) > 9:
                sdShowTxt = str(int(sanddollar/1000000))+"M"
            elif len(sdShowTxt) > 5:
                sdShowTxt = str(int(sanddollar/1000))+"K"

            # display text
            text = pygame.font.Font(FONT, 48).render(sdShowTxt, True, (66, 99, 52))
            textpos = text.get_rect(x=sanddollarRect.x+w*0.12, 
                                    centery=sanddollarRect.centery-w*0.003)
            screen.blit(text, textpos)

            # animations for when sand dollars are spent
            if shopSDAnimate > 0:
                text = pygame.font.Font(FONT, int((20-shopSDAnimate)*1.5)).render(f"-{shopSDAnimateTxt}", True, (66, 99, 52))
                text.set_alpha(255*shopSDAnimate/20)
                textpos = text.get_rect(centerx=sanddollarRect.x + sanddollarRect.w + w*0.05, 
                                        centery=sanddollarRect.y + sanddollarRect.h - w*0.05 + w*0.1*shopSDAnimate/20)
                screen.blit(text, textpos)

                shopSDAnimate -= 1

            stage = exit_button(popupExitRect, clickSFX, stage, down, "home")

        elif stage == "pick-beach": # startup screen to pick what beach background you want
            screen.blit(beachBgImgs[beachBgNo], (0,0))

            beachBgNo = flip_page(beachBgNo, 3, 
                                flipRightButton, flipLeftButton, flipSFX, down, show=True)
            
            beachBgNo = beachBgNo % 3

            screen.blit(beachConfirmButtonImg, (w*0.45,w*0.88))

            if beachConfirmButtonRect.collidepoint(pygame.mouse.get_pos())\
                and pygame.mouse.get_pressed()[0] and not down:
                clickSFX.play()
                stage = "beach setup"

                # save data
                r = json.loads(load_data("save"))

                r["beach_bg"] = str(beachBgNo)

                save_data(json.dumps(r), "save")

        elif stage.split()[0] == "beach": # beach main screen
            if len(stage.split()) > 1 and stage.split()[1] == "setup":
                beachBgNo, beachData, beachItemRects, moveItem, stage = beach_setup(shopItemImgs, ogShopItemImgs, stage)

            screen.blit(beachBgImgs[beachBgNo], (0,0))

            clickBg = True

            if not down:
                moveItem = []

            for i in range(len(beachData)):
                scaled_img = pygame.transform.scale(ogShopItemImgs[beachData[i][0]], 
                                                    (int(beachData[i][1][2]*w*0.2), 
                                                     int(beachData[i][1][2]*w*0.2)))
                center = (beachData[i][1][0] + scaled_img.get_width() // 2, 
                          beachData[i][1][1] + scaled_img.get_height() // 2)
                img = pygame.transform.flip(pygame.transform.rotate(
                    scaled_img, int(beachData[i][1][3])), 
                    int(beachData[i][1][4]), False)
                rect = img.get_rect(center=center)
                screen.blit(img, rect)

                if beachItemRects[i].collidepoint(pygame.mouse.get_pos())\
                    and pygame.mouse.get_pressed()[0] and not down:
                    moveItem.append(i)

                    posOffset = (pygame.mouse.get_pos()[0]-beachData[moveItem[-1]][1][0], 
                                 pygame.mouse.get_pos()[1]-beachData[moveItem[-1]][1][1])
                    clickBg = False
            
            if pygame.mouse.get_pressed()[0] and clickBg and moveItem == []: # reset selecting if bg is clicked
                selecting = -1
            
            # do things to selected object (blit stuff)
            if selecting != -1:
                scaling, rotating, ogRotation = display_selected_UI(beachItemRects, selecting, scaleRect, scaleImg, rotateRect, rotateImg, flipRect, flipImg, scaling, rotating, beachData, ogRotation, down)
            
            if rotating:
                # find the distance between center of the image and mouse pos and then use trig to find angle to rotate
                try:
                    center = (beachItemRects[selecting].centerx, beachItemRects[selecting].centery) # find center of image
                    mouse = pygame.mouse.get_pos() # get mouse pos
                    diff = (mouse[0] - center[0], center[1] - mouse[1]) # calc difference between mouse and image center
                    angle = int(math.atan2(diff[1], diff[0]) * 180 / math.pi) # calc angle that needs to be rotated

                    beachData[selecting][1][3] = (ogRotation + angle + 135) % 360 # idk
                    
                    r = json.loads(load_data("save"))

                    r["beach_items"] = r["beach_items"].split()
                    r["beach_items"][selecting] = f"{beachData[selecting][0]}/{beachData[selecting][1][0]}-{beachData[selecting][1][1]}-{beachData[selecting][1][2]}-{beachData[selecting][1][3]}-{beachData[selecting][1][4]}"
                    r["beach_items"] = " ".join(r["beach_items"])

                    save_data(json.dumps(r), "save")

                except: pass
                
            if scaling:
                if (pygame.mouse.get_pos()[0] - beachItemRects[selecting].x) / (w*0.2) > 0.3:
                    scaleRect, rotateRect, flipRect, beachItemRects = scale_beach_img(beachData, selecting, beachItemRects, shopItemImgs, ogShopItemImgs, rotateRect, scaleRect, flipRect, moveItem)

            if moveItem != []\
                and not scaleRect.collidepoint(pygame.mouse.get_pos()) and not scaling\
                and not rotateRect.collidepoint(pygame.mouse.get_pos()) and not rotating:
                selecting, scaleRect, rotateRect, flipRect = move_beach_item(moveItem, beachData, posOffset, beachItemRects, scaleRect, rotateRect, flipRect)
            
            if not pygame.mouse.get_pressed()[0] and down:
                scaling = False
                rotating = False
                stage = "beach setup"
            
            stage = beach_add_button(addButtonRect, stage, clickSFX, down)
            
            selecting, stage = beach_trash_button(moveItem, beachData, trashButtonRect, trashImgs, selecting, stage)

            stage = exit_button(mainExitRect, clickSFX, stage, down, "home")

        elif stage.split()[0] == "add": # screen to chose what to add to beach
            pygame.draw.rect(screen, (241, 245, 237), addBg, border_radius=10)

            if len(stage.split()) > 1 and stage.split()[1] == "setup":
                stage = "add"
                addPage = 0

                # get data
                r = json.loads(load_data("save"))

                addData = r["inv"]
                addData = addData.split()

                for i in range(len(addData)):
                    addData[i] = int(addData[i])

                # create rects for items
                addItemRects = []
                for i in range(len(addData)):
                    addItemRects.append(pygame.Rect(w*0.18+((i%9)%3 * w*0.22), 
                                                    w*0.18+((i%9)//3 * w*0.22), 
                                                    w*0.2, 
                                                    w*0.2))

            for i in range(addPage*9, addPage*9+9):
                if len(addItemRects) > i:
                    pygame.draw.rect(screen, (149, 163, 135), addItemRects[i], border_radius=20)
                    
                    if addItemRects[i].collidepoint(pygame.mouse.get_pos()):
                        shopItemImgs[addData[i]] = pygame.transform.scale(ogShopItemImgs[addData[i]], (w*0.17, w*0.17))
                        screen.blit(shopItemImgs[addData[i]], (addItemRects[i].centerx-w*0.085, addItemRects[i].centery-w*0.085))

                        if pygame.mouse.get_pressed()[0]:
                            stage = "beach setup"

                            # save data
                            r = json.loads(load_data("save"))

                            r["beach_items"] = r["beach_items"].split()
                            r["inv"] = r["inv"].split()

                            r["inv"].remove(str(addData[i]))
                            r["beach_items"].append(f"{str(addData[i])}/{int(random.randint(int(w/4), int(w/4)*3))}-{int(random.randint(int(w/4), int(w/4)*3))}-1-0-0")
                            r["beach_items"] = " ".join(r["beach_items"])
                            r["inv"] = " ".join(r["inv"])

                            save_data(json.dumps(r), "save")
                    
                    else:
                        shopItemImgs[addData[i]] = pygame.transform.scale(ogShopItemImgs[addData[i]], 
                                                                          (w*0.15, w*0.15))
                        screen.blit(shopItemImgs[addData[i]], 
                                    (addItemRects[i].centerx-w*0.075, 
                                     addItemRects[i].centery-w*0.075))

            addPage = flip_page(addPage, (len(addData)-1)//9, 
                                flipRightButton, flipLeftButton, flipSFX, down)

            if key[pygame.K_LEFT] and addPage > 0 and not down:
                addPage -= 1
            if key[pygame.K_RIGHT] and addPage < (len(shopItemRects)-1)//9 and not down:
                addPage += 1

            stage = exit_button(popupExitRect, clickSFX, stage, down, "beach")

        elif stage == "animation-for-draw": # text animation for drawing new custom
            drawBoard(size, screen, colors, boardSolution, gap, w, cellW, boardRects, crossImg, cellTimers)
            
            screen.blit(checkButtonImg, (gap*0.1,gap*0.1))

            screen.blit(fade, (0,0))

            text = pygame.font.Font(FONT, 96).render("Draw your Nonogram!", True, (255,255,255))
            textpos = text.get_rect(centerx=w/2-offset, centery=w*0.4)
            screen.blit(text, textpos)

            text = pygame.font.Font(FONT, 48).render("Have a friend draw it for a challenge", True, (255,255,255))
            textpos = text.get_rect(centerx=w/2-offset, centery=w*0.6)
            screen.blit(text, textpos)

            # animation for text moving across the screen
            offset, acceleration = textAnimations(offset, acceleration)

            if offset >= 700:
                stage = "fade-for-draw"
                acceleration = 1
                offset = -500
        
        elif stage == "fade-for-draw": # fade from text animation to drawing new custom
            drawBoard(size, screen, colors, boardSolution, gap, w, cellW, boardRects, crossImg, cellTimers)
            
            screen.blit(checkButtonImg, (gap*0.1,gap*0.1))

            fade.fill((0, 0, 0, fadeo))
            screen.blit(fade, (0,0))
            fadeo -= acceleration
            acceleration += 0.5

            if fadeo <= 0:
                stage = "draw"
                fadeo = 127
                acceleration = 1
                fade.fill((0, 0, 0, 127))
        
        elif stage == "draw": # draw for making a new custom
            # draw the board
            drawBoard(size, screen, colors, boardSolution, gap, w, cellW, boardRects, crossImg, cellTimers)
            
            screen.blit(checkButtonImg, (gap*0.1,gap*0.1))
            
            # player start to draw
            for y in range(size):
                for x in range(size):
                    if boardRects[y][x].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                        if not down:
                            drawMode = int(not boardSolution[y][x])

                        boardSolution[y][x] = drawMode
            
            # done
            if checkButtonRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                stage = "animation-for-solve"

                infos, boardSolving, infoDone = addInfo(size, infos, boardSolution, boardSolving, infoDone)
        
        elif stage == "choose-solve": # screen to chose to play custom drawn or pre-drawn
            # pre-drawn button
            choosePredrawnButton.draw()

            if choosePredrawnButton.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(playBubble, (w*0.2, choosePredrawnButton.y - w*0.2))

                text = pygame.font.Font(FONT, 24).render("Solve a pre-drawn nonogram", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=choosePredrawnButton.y - w*0.15)
                screen.blit(text, textpos)

                text = pygame.font.Font(FONT, 24).render("Earn sand dollars", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=choosePredrawnButton.y - w*0.1)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    stage = "animation-for-solve get-from-gallery pre-drawn"
                    clickSFX.play()

            # custom button
            pygame.draw.rect(screen, (171, 204, 157), chooseCustomRect, border_radius=20)

            if chooseCustomRect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(drawBubble, (w*0.2, chooseCustomRect.y + chooseCustomRect.h))

                if load_data("gallery") != " ":
                    text = pygame.font.Font(FONT, 24).render("Solve a nonogram you drew before", True, (51, 66, 44))
                    textpos = text.get_rect(centerx=w/2, centery=chooseCustomRect.y + w*0.23)
                    screen.blit(text, textpos)

                    text = pygame.font.Font(FONT, 24).render("Doesn't earn sand dollars", True, (51, 66, 44))
                    textpos = text.get_rect(centerx=w/2, centery=chooseCustomRect.y + w*0.28)
                    screen.blit(text, textpos)

                    text = pygame.font.Font(FONT, 72).render("Custom", True, (66, 99, 52))

                else:
                    text = pygame.font.Font(FONT, 24).render("No nonogram available", True, (51, 66, 44))
                    textpos = text.get_rect(centerx=w/2, centery=chooseCustomRect.y + w*0.23)
                    screen.blit(text, textpos)

                    text = pygame.font.Font(FONT, 24).render("Draw one before solving", True, (51, 66, 44))
                    textpos = text.get_rect(centerx=w/2, centery=chooseCustomRect.y + w*0.28)
                    screen.blit(text, textpos)

                    text = pygame.font.Font(FONT, 64).render("Custom", True, (66, 99, 52))

                if pygame.mouse.get_pressed()[0] and not down and load_data("gallery") != " ":
                    stage = "animation-for-solve get-from-gallery custom"
                    clickSFX.play()
            
            else:
                text = pygame.font.Font(FONT, 64).render("Custom", True, (66, 99, 52))
            
            textpos = text.get_rect(centerx=chooseCustomRect.centerx, centery=chooseCustomRect.centery)
            screen.blit(text, textpos)

            stage = exit_button(mainExitRect, clickSFX, stage, down, "home")

        elif stage.split()[0] == "animation-for-solve": # text animation for starting to solve
            if len(stage.split()) > 1 and stage.split()[1] == "get-from-gallery":
                if len(stage.split()) > 2 and stage.split()[2] == "custom":
                    r = load_data("gallery").strip().splitlines()
                    solveNext = random.randint(0,len(r)-1)
                    r = r[solveNext]
                    
                elif len(stage.split()) > 2 and stage.split()[2] == "pre-drawn":
                    r = load_data("gallery").strip().splitlines()
                    random.seed(time.time_ns()) # makes sure it is random because when running with pygbag its always 2
                    solveNext = random.randint(0,len(PREDRAWN)-1)

                    r = PREDRAWN[solveNext]

                    solveNext = f"p{solveNext}"

                size = int(r.split(" ")[0])
                r = r.split(" ")[1]
                for y in range(size):
                    for x in range(size):
                        boardSolution[y][x] = int(r[y*size+x])
                
                infos, boardSolving, infoDone = addInfo(size, infos, boardSolution, boardSolving, infoDone)

                stage = stage.split()
                stage[1] = "earn-sanddollar"
                stage = " ".join(stage)

            drawBoard(size, screen, colors, boardSolving, gap, w, cellW, boardRects, crossImg, cellTimers)

            screen.blit(heartXOimg[XO], (0,0))

            text = pygame.font.Font(FONT, 32).render(str(hp)+"%", True, (247, 225, 237))
            textpos = text.get_rect(centerx=gap/2, centery=gap/5*4)
            screen.blit(text, textpos)

            clueSelected = drawInfo(yinfoRects, xinfoRects, size, infos, infoDone, clueArrows, clueSelected, down)

            screen.blit(fade, (0,0))

            text = pygame.font.Font(FONT, 96).render("Solve!", True, (255,255,255))
            textpos = text.get_rect(centerx=w/2+offset, centery=w/2)
            screen.blit(text, textpos)

            offset, acceleration = textAnimations(offset, acceleration)

            if offset >= 700:
                stage = stage.split()
                stage[0] = "fade-for-solve"
                stage = " ".join(stage)
                acceleration = 1
        
        elif stage.split()[0] == "fade-for-solve": # fade from text animation to solving
            drawBoard(size, screen, colors, boardSolving, gap, w, cellW, boardRects, crossImg, cellTimers)

            screen.blit(heartXOimg[XO], (0,0))

            text = pygame.font.Font(FONT, 32).render(str(hp)+"%", True, (247, 225, 237))
            textpos = text.get_rect(centerx=gap/2, centery=gap/5*4)
            screen.blit(text, textpos)

            clueSelected = drawInfo(yinfoRects, xinfoRects, size, infos, infoDone, clueArrows, clueSelected, down)

            fade.fill((0, 0, 0, fadeo))
            screen.blit(fade, (0,0))
            fadeo -= acceleration
            acceleration += 0.5

            if fadeo <= 0:
                stage = stage.split()
                stage[0] = "solve"
                stage = " ".join(stage)
        
        elif stage.split()[0] == "solve": # solve the nonogram
            boardSolving = autoCross(boardSolving, boardSolution, size)

            drawBoard(size, screen, colors, boardSolving, gap, w, cellW, boardRects, crossImg, cellTimers)

            screen.blit(heartXOimg[XO], heartRect)
            if pygame.mouse.get_pressed()[0] and heartRect.collidepoint(pygame.mouse.get_pos()) and not down:
                if XO == "X":
                    XO = "O"
                else:
                    XO = "X"
                clickSFX.play()

            clueSelected = drawInfo(yinfoRects, xinfoRects, size, infos, infoDone, clueArrows, clueSelected, down)
            
            # check for fill
            for y in range(size):
                for x in range(size):
                    if boardRects[y][x].collidepoint(pygame.mouse.get_pos())\
                        and pygame.mouse.get_pressed()[0] and not solveDown:
                            
                            if (boardSolving[y][x] == 0 or boardSolving[y][x] == 3) and XO == "O":
                                if boardSolution[y][x] == 1:
                                    boardSolving[y][x] = 1
                                else:
                                    boardSolving[y][x] = 3
                                    cellTimers[y][x] = 60
                                    hp -= 8
                                    solveDown = True

                            if (boardSolving[y][x] == 0 or boardSolving[y][x] == 3) and XO == "X":
                                if boardSolution[y][x] == 0:
                                    boardSolving[y][x] = 2.9
                                else:
                                    boardSolving[y][x] = 3
                                    cellTimers[y][x] = 60
                                    hp -= 8
                                    solveDown = True

                            infoDone = check_info_done(infoDone, boardSolving, boardSolution, infos)

            text = pygame.font.Font(FONT, 32).render(str(hp)+"%", True, (247, 225, 237))
            textpos = text.get_rect(centerx=gap/2, centery=gap/5*4)
            screen.blit(text, textpos)

            # check if won
            won = True
            for y in range(size):
                for x in range(size):
                    if not (boardSolving[y][x] == boardSolution[y][x]\
                            or (boardSolving[y][x] == 2 and boardSolution[y][x] == 0)):
                        won = False
            
            if won:
                stage = stage.split()
                stage[0] = "win"
                stage = " ".join(stage)
            
            if hp <= 0:
                stage = stage.split()
                stage[0] = "lose"
                stage = " ".join(stage)
        
        elif stage.split()[0] == "win" or stage.split()[0] == "lose": # win or lose screen
            for y in range(size):
                for x in range(size):
                    boardRects[y][x].x = x*w/size
                    boardRects[y][x].y = y*w/size
                    boardRects[y][x].w = w/size
                    boardRects[y][x].h = w/size

            for y in range(size):
                for x in range(size):
                    pygame.draw.rect(screen, colors[boardSolution[y][x]], boardRects[y][x])
            
            if opacity < 127:
                opacity += 1

            darken.fill((0, 0, 0, opacity))
            screen.blit(darken, (0,0))

            if stage.split()[0] == "win":
                text = pygame.font.Font(FONT, 128).render("YOU WIN!", True, (211, 232, 179))
                if "pre-drawn" in stage:
                    earndollar = 100
                else:
                    earndollar = 10
            elif stage.split()[0] == "lose":
                text = pygame.font.Font(FONT, 128).render("YOU LOSE!", True, (232, 195, 195))
                earndollar = 0
            text.set_alpha(opacity*2)

            if len(stage.split()) > 1 and stage.split()[1] == "earn-sanddollar":
                textpos = text.get_rect(centerx=w/2, centery=w/3)
            else:
                textpos = text.get_rect(centerx=w/2, centery=w/4)
            screen.blit(text, textpos)

            if opacity >= 127:
                if len(stage.split()) > 1 and stage.split()[1] == "earn-sanddollar":
                    claimSanddollarButton.text.modify(text=f"Claim sand dollar {earndollar}x")
                    claimSanddollarButton.hoverText.modify(text=f"Claim sand dollar {earndollar}x")
                    claimSanddollarButton.draw()

                    if claimSanddollarButton.get_pressed():
                        clickSFX.play()
                        sanddollar += earndollar

                        if stage.split()[0] == "win":
                            # save data
                            r = json.loads(load_data("save"))

                            r["sanddollar"] = str(sanddollar)
                            r["gallery"] = r["gallery"].split("-")
                            r["gallery"].append(str(solveNext))
                            r["gallery"] = "-".join(r["gallery"])
                            r["gallery"] = r["gallery"].strip("-")

                            save_data(json.dumps(r), "save")

                        stage = "reset"

                else:
                    text = pygame.font.Font(FONT, 64).render("Publish image?", True, (157, 166, 144))
                    textpos = text.get_rect(centerx=w/2, centery=w*0.55)
                    screen.blit(text, textpos)

                    yesButton.draw()

                    if yesButton.get_pressed():
                        clickSFX.play()
                        r = load_data("gallery").strip()

                        r += "\n" + str(size)+" "
                        for y in boardSolution: # go through and get binary map of nonogram
                            for x in y:
                                r += str(x)

                        solveNext = len(r.splitlines()) - 1 # find last one because it was just appended for the gallery

                        # save data
                        save_data(r, "gallery")

                        r = json.loads(load_data("save"))

                        r["gallery"] = r["gallery"].split("-")
                        r["gallery"].append(str(solveNext))
                        r["gallery"] = "-".join(r["gallery"])
                        r["gallery"] = r["gallery"].strip("-")

                        save_data(json.dumps(r), "save")

                        solveNext = -1

                        stage = "reset"

                    noButton.draw()
                    
                    if noButton.get_pressed():
                        clickSFX.play()
                        stage = "reset"

        elif stage == "reset": # reset everything after solving a nonogram
            boardSolution, boardSolving, boardRects = setupBoards(size, cellW, gap)

            checkButtonRect = pygame.Rect(gap*0.1, gap*0.1, gap*0.8, gap*0.8)

            # info for the sides
            infos, yinfoRects, xinfoRects, infoDone = setupInfo(size, gap, cellW)

            # for win and loose and animation word screen
            darken = pygame.Surface((w,w), pygame.SRCALPHA)
            darken.fill((0, 0, 0, 0))
            opacity = 0

            # for fade in and out of the darken
            fade = pygame.Surface((w,w), pygame.SRCALPHA)
            fade.fill((0, 0, 0, 127))
            fadeo = 127

            solveNext = 0

            hp = 100

            offset = -500
            acceleration = 1

            stage = "home"

        key = pygame.key.get_pressed()

        if not pygame.mouse.get_pressed()[0] and not pygame.mouse.get_pressed()[2] and not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            down = False
            solveDown = False
        else:
            down = True

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)

asyncio.run(main())