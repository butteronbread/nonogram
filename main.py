import pygame, math, random, asyncio, platform, os, time

w = 720

FONT = "font1.ttf"

pygame.init()

screen = pygame.display.set_mode((w,w))

clock = pygame.time.Clock()

pygame.display.set_caption("Gram of Grain")

PREDRAWN = """15 000000000000000000000000000000011100011111000010010100000100010001000001010010001000000010010010100000100011100011111000000000000000000000111000100000000100010100000000111000111000000100010101000000100010101000000000000000000
15 000000000000000000000000000000000111001111110001100000000010011000000000100010000000001000010000000001000011111000010000011001100010000010000100100000011001100100000001111001000000000000000000000000000000000000000000000000000
15 111111111111111100000010000001101001010100101100000010000001101001010111101101111010100101100000010000001111111111111111100000010000001101001010100101100000010000001101111010100101101001010111101100000010000001111111111111111
15 100011000110001010100101001010001000010000100010100101001010100011000110001011100111000000100011000100000100011000100000100011000100000011100111000000100010000001110010100000010001001000000010001010100000010001100010000001110
15 000000000000000000000000000000000000000000000000000000000000000000000000000011100101001110001110111011100000111111111000000010111010000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000
15 000000000000000000011111111100000100000001000000100000010000001000000100000001000001000000010000001110000011111000100000000001001000000000010010000000000010100000000000101000000000000110000000000000100000000000000000000000000
15 000001111100000000111111111000001110000011100011000000000110011000000000110110001000100011110001000100011110001111100011110001000100011110001000100011011000000000110011000000000110001110000011100000111111111000000001111100000
15 000000010000000010000010000010001000010000100000100010001000000010000010000000000111000000000001111100000111101111101111000001111100000000000111000000000010000010000000100010001000001000010000100010000010000010000000010000000
15 000000000000000000000000000000001110000011100001011111110100000110000011000001000000000100010000000000010010001000100010010000000000010010000010000010001000101000100000100000001000000011111110000000000000000000000000000000000""".splitlines()

if platform.system() == "Emscripten":
    from js import window
    platform.window.onbeforeunload = None

# save load functions

def save_data(data, file):
    if platform.system() == "Emscripten":
        window.localStorage.setItem(file, data)
    else:
        # PC: Use regular file saving
        with open(f"{file}.txt", "w") as f:
            f.write(data)

def load_data(file):
    if platform.system() == "Emscripten":
        saved_data = window.localStorage.getItem(file)
        return saved_data if saved_data else None
    else:
        # PC: Load from file
        file = f"{file}.txt"
        if os.path.exists(file):
            with open(file, "r") as f:
                return f.read()
        return None

# setup functions

def setupBoards(size, cellW, gap):
    boardSolution = [] # answer
    boardSolving = [] # current solving state
    boardRects = [] # rects of each cell in the board
    for y in range(size):
        boardSolution.append([])
        boardSolving.append([])
        boardRects.append([])
        for x in range(size):
            boardSolution[-1].append(0)
            boardSolving[-1].append(0)
            boardRects[-1].append(pygame.Rect(x*cellW + gap, y*cellW + gap, cellW, cellW))
    
    return boardSolution, boardSolving, boardRects

def setupPlayAnimations(cellW, size):
    crossImg = pygame.transform.scale(pygame.image.load("imgs/cross.png"), (cellW, cellW))
    cellTimers = []
    for y in range(size):
        cellTimers.append([])
        for x in range(size):
            cellTimers[y].append(0)
    
    return crossImg, cellTimers

def setupInfo(size, gap, cellW):
    yinfo = []
    xinfo = []

    yinfoRects = []
    for y in range(size):
        yinfoRects.append(pygame.Rect(0, gap+cellW*y+3, gap, cellW-6))

    xinfoRects = []
    for x in range(size):
        xinfoRects.append(pygame.Rect(gap+cellW*x+3, 0, cellW-6, gap))
    
    return yinfo, xinfo, yinfoRects, xinfoRects

def setupHome():
    playRect = pygame.Rect(0,0,w*0.4,w*0.15) # play button: Solve a pre-drawn nonogram. Earn coins according to puzzle difficulty
    playRect.centerx = w/2
    playRect.centery = w*0.35

    drawRect = pygame.Rect(0,0,w*0.3,w*0.12) # draw button: Draw and solve your own nonogram design. This will not increase coins
    drawRect.centerx = w/2
    drawRect.centery = w*0.55

    playBubble = pygame.transform.scale(pygame.image.load("imgs/upbubble.png"), (w*0.6, w*0.2))
    drawBubble = pygame.transform.scale(pygame.image.load("imgs/downbubble.png"), (w*0.6, w*0.2))

    sanddollarRect = pygame.Rect(w*0.63, w*0.02, w*0.35, w*0.1)
    sanddollarImg = pygame.transform.scale(pygame.image.load("imgs/sanddollar.png"), (w*0.07, w*0.07))

    shopButtonRect = pygame.Rect(w*0.02, w*0.02, w*0.12, w*0.12)
    ogShopImg = pygame.image.load("imgs/shop.png")
    shopImg = pygame.transform.scale(ogShopImg, (w*0.08, w*0.08))

    galleryButtonRect = pygame.Rect(w*0.16, w*0.02, w*0.12, w*0.12)
    ogGalleryImg = pygame.image.load("imgs/gallery.png")
    galleryImg = pygame.transform.scale(ogGalleryImg, (w*0.08, w*0.08))

    beachButtonRect = pygame.Rect(w*0.02, w*0.86, w*0.12, w*0.12)
    ogBeachImg = pygame.image.load("imgs/beach.png")
    beachImg = pygame.transform.scale(ogBeachImg, (w*0.08, w*0.08))

    soundButtonRect = pygame.Rect(w*0.86, w*0.86, w*0.12, w*0.12)
    ogSoundImgs = [pygame.image.load("imgs/off.png"), pygame.image.load("imgs/on.png")]
    soundImgs = [pygame.transform.scale(ogSoundImgs[1], (w*0.08, w*0.08)), pygame.transform.scale(ogSoundImgs[0], (w*0.08, w*0.08))]
    soundOn = True

    infoButtonRect = pygame.Rect(w*0.72, w*0.86, w*0.12, w*0.12)
    ogInfoImg = pygame.image.load("imgs/info.png")
    infoImg = pygame.transform.scale(ogInfoImg, (w*0.08, w*0.08))

    return playRect, drawRect, playBubble, drawBubble, sanddollarRect, sanddollarImg, shopButtonRect, ogShopImg, shopImg, galleryButtonRect, ogGalleryImg, galleryImg, beachButtonRect, ogBeachImg, beachImg, soundButtonRect, ogSoundImgs, soundImgs, soundOn, infoButtonRect, ogInfoImg, infoImg

def setupChooseSolve():
    choosePredrawnRect = pygame.Rect(0,0,w*0.5,w*0.15)
    choosePredrawnRect.centerx = w/2
    choosePredrawnRect.centery = w*0.35

    chooseCustomRect = pygame.Rect(0,0,w*0.4,w*0.14)
    chooseCustomRect.centerx = w/2
    chooseCustomRect.centery = w*0.55

    return choosePredrawnRect, chooseCustomRect

def setupDarkFade():
    darken = pygame.Surface((w,w), pygame.SRCALPHA)
    darken.fill((0, 0, 0, 0))
    opacity = 0

    fade = pygame.Surface((w,w), pygame.SRCALPHA)
    fade.fill((0, 0, 0, 127))
    fadeo = 127

    return darken, opacity, fade, fadeo

def setupEndScreen():
    yesRect = pygame.Rect(0,0,w*0.3,w*0.1)
    yesRect.centerx = w*0.3
    yesRect.centery = w*0.7

    noRect = pygame.Rect(0,0,w*0.3,w*0.1)
    noRect.centerx = w*0.7
    noRect.centery = w*0.7

    claimSanddollarRect = pygame.Rect(0,0,w*0.75,w*0.1)
    claimSanddollarRect.centerx = w/2
    claimSanddollarRect.centery = w*0.6

    return yesRect, noRect, claimSanddollarRect

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

    FlipLeftRect = pygame.Rect(0,0,w*0.1,w*0.15)
    FlipLeftRect.centerx = w*0.125
    FlipLeftRect.centery = w*0.5

    FlipRightRect = pygame.Rect(0,0,w*0.1,w*0.15)
    FlipRightRect.centerx = w*0.875
    FlipRightRect.centery = w*0.5

    return galleryBg, popupExitRect, galleryData, galleryBigRects, gallerySmallRects, galleryColors, solveNext, galleryPage, FlipLeftRect, FlipRightRect

def setupBeach():
    beachBgImgs = [pygame.transform.scale(pygame.image.load("beachBg/1.png"), (w,w)), pygame.transform.scale(pygame.image.load("beachBg/2.png"), (w,w)), pygame.transform.scale(pygame.image.load("beachBg/3.png"), (w,w))]

    beachConfirmButtonRect = pygame.Rect(w*0.45,w*0.88,w*0.1,w*0.1)
    beachConfirmButtonImg = pygame.transform.scale(pygame.image.load("imgs/check.png"), (w*0.1,w*0.1))

    mainExitRect = pygame.Rect(w*0.88, w*0.02, w*0.1, w*0.1)

    addButtonRect = pygame.Rect(w*0.02, w*0.88, w*0.1, w*0.1)
    trashButtonRect = pygame.Rect(w*0.14, w*0.88, w*0.1, w*0.1)

    scaleImg = pygame.transform.scale(pygame.image.load("imgs/scale.png"), (w*0.05,w*0.05))
    scaleRect = pygame.Rect(0, 0, w*0.06, w*0.06)

    rotateImg = pygame.transform.scale(pygame.image.load("imgs/rotate.png"), (w*0.05,w*0.05))
    rotateRect = pygame.Rect(0, 0, w*0.06, w*0.06)

    flipImg = pygame.transform.scale(pygame.image.load("imgs/flip.png"), (w*0.05,w*0.05))
    flipRect = pygame.Rect(0, 0, w*0.06, w*0.06)

    trashImgs = [pygame.transform.scale(pygame.image.load("imgs/close.png"), (w*0.08, w*0.08)), pygame.transform.scale(pygame.image.load("imgs/open.png"), (w*0.08, w*0.08))]

    addBg = pygame.Rect(0,0,w*0.9,w*0.9)
    addBg.center = (w/2,w/2)

    posOffset = (0,0)

    return beachBgImgs, beachConfirmButtonRect, beachConfirmButtonImg, mainExitRect, addButtonRect, trashButtonRect, trashImgs, addBg, posOffset, rotateImg, scaleImg, rotateRect, scaleRect, flipImg, flipRect

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
        shopItemImgs.append(pygame.transform.scale(pygame.image.load(f"shopItems/{i}.png"), (w*0.18, w*0.18)))
        ogShopItemImgs.append(pygame.image.load(f"shopItems/{i}.png"))

    shopItemPrice = [300, 100, 500, 300, 1200, 1000, 1000, 200, 200, 300, 300, 200, 500, 200]

    return shopBg, shopPage, shopItemRects, shopItemImgs, ogShopItemImgs, shopItemPrice

def setupOthers():
    size = 15 # pixels for the drawing width and height

    gap = w*0.122
    cellW = math.floor((w-gap)/size) # gap of 3 on top and left for numbers

    hp = 100

    offset = -500
    acceleration = 1

    down = False
    solveDown = False

    colors = ((185, 191, 153), (75, 83, 32), (255, 255, 255), (252, 93, 93)) # filled and not filled nonogram colors

    checkButtonRect = pygame.Rect(gap*0.1, gap*0.1, gap*0.8, gap*0.8)
    checkButtonImg = pygame.transform.scale(pygame.image.load("imgs/check.png"), (gap*0.8, gap*0.8))

    return size, gap, cellW, hp, offset, acceleration, down, solveDown, colors, checkButtonRect, checkButtonImg

def setupChange():
    stage = "home" # index
    r = load_data("save").split(",")
    sanddollar = int(r[0])

    return stage, sanddollar

def setup():
    if load_data("save") == None:
        save_data("0,,,,,", "save")
    if load_data("gallery") == None:
        save_data(" ", "gallery")

    size, gap, cellW, hp, offset, acceleration, down, solveDown, colors, checkButtonRect, checkButtonImg = setupOthers()

    crossImg, cellTimers = setupPlayAnimations(cellW, size)

    boardSolution, boardSolving, boardRects = setupBoards(size, cellW, gap)

    yinfo, xinfo, yinfoRects, xinfoRects = setupInfo(size, gap, cellW)

    darken, opacity, fade, fadeo = setupDarkFade()

    # home screen stuff
    playRect, drawRect, playBubble, drawBubble, sanddollarRect, sanddollarImg, shopButtonRect, ogShopImg, shopImg, galleryButtonRect, ogGalleryImg, galleryImg, beachButtonRect, ogBeachImg, beachImg, soundButtonRect, ogSoundImgs, soundImgs, soundOn, infoButtonRect, ogInfoImg, infoImg = setupHome()

    # publish image yes no buttons
    yesRect, noRect, claimSanddollarRect = setupEndScreen()

    # gallery stuff
    galleryBg, popupExitRect, galleryData, galleryBigRects, gallerySmallRects, galleryColors, solveNext, galleryPage, FlipLeftRect, FlipRightRect = setupGallery()

    # beach stuff
    beachBgImgs, beachConfirmButtonRect, beachConfirmButtonImg, mainExitRect, addButtonRect, trashButtonRect, trashImgs, addBg, posOffset, rotateImg, scaleImg, rotateRect, scaleRect, flipImg, flipRect = setupBeach()

    # shop stuff
    shopBg, shopPage, shopItemRects, shopItemImgs, ogShopItemImgs, shopItemPrice = setupShop()

    stage, sanddollar = setupChange()

    selecting, clickBg = -1, False

    shopSDAnimate, shopSDAnimateTxt, scaling, rotating, ogRotation = 0, "", False, False, 0

    choosePredrawnRect, chooseCustomRect = setupChooseSolve()

    infoPageBg = pygame.transform.scale(pygame.image.load("imgs/infoPage.png"), (w*0.9,w*0.9))
    infoPageBgBold = pygame.transform.scale(pygame.image.load("imgs/infoPageBold.png"), (w*0.9,w*0.9))
    infoRect = pygame.Rect(166, 236, 160, 30)

    instructionPages = []
    for i in range(3):
        instructionPages.append(pygame.transform.scale(pygame.image.load(f"imgs/infos/{i}.png"), (w*0.9,w*0.9)))
    instructionPageNo = 0

    XO = "O"
    heartXOimg = {"O": pygame.transform.scale(pygame.image.load("imgs/heartO.png"), (gap, gap)), "X": pygame.transform.scale(pygame.image.load("imgs/heartX.png"), (gap, gap))}
    heartRect = pygame.Rect(0,0,gap,gap)

    return size, gap, cellW, hp, offset, acceleration, down, solveDown, colors, solveNext,\
        checkButtonRect, checkButtonImg, crossImg,\
        cellTimers, boardSolution, boardSolving, boardRects,\
        yinfo, xinfo, yinfoRects, xinfoRects,\
        darken, opacity, fade, fadeo,\
        choosePredrawnRect, chooseCustomRect,\
        playRect, drawRect, playBubble, drawBubble,\
        sanddollarRect, sanddollarImg,\
        shopButtonRect, ogShopImg, shopImg,\
        galleryButtonRect, ogGalleryImg, galleryImg,\
        beachButtonRect, ogBeachImg, beachImg,\
        yesRect, noRect, claimSanddollarRect,\
        popupExitRect, galleryBg, galleryData,\
        galleryBigRects, gallerySmallRects,\
        galleryColors, galleryPage, FlipLeftRect, FlipRightRect,\
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
        infoButtonRect, ogInfoImg, infoImg,\
        infoPageBg, infoPageBgBold, infoRect,\
        instructionPages, instructionPageNo,\
        XO, heartXOimg, heartRect

# other functions

def drawBoard(size, screen, colors, board, gap, w, cellW, boardRects, crossImg, cellTimers):
    for y in range(size):
        for x in range(size):
            if board[y][x] == 3:
                pygame.draw.rect(screen, colors[0], boardRects[y][x])
                surf = pygame.Surface((cellW, cellW), pygame.SRCALPHA)
                surf.fill((252, 93, 93, 4.25*cellTimers[y][x]))
                screen.blit(surf, (boardRects[y][x].x, boardRects[y][x].y))
                cellTimers[y][x] -= 1

                if cellTimers[y][x] <= 0:
                    cellTimers[y][x] = 0
                    board[y][x] = 0
            elif board[y][x] == 2:
                pygame.draw.rect(screen, colors[0], boardRects[y][x])
                screen.blit(crossImg, (boardRects[y][x].x, boardRects[y][x].y))
            else:
                pygame.draw.rect(screen, colors[board[y][x]], boardRects[y][x])
    
    for y in range(1,size):
        lineStart = (gap, gap + cellW*y)
        lineEnd = (w, gap + cellW*y)
        pygame.draw.line(screen, (36,51,5), lineStart, lineEnd, 2)

    for x in range(1,size):
        lineStart = (gap + cellW*x, gap)
        lineEnd = (gap + cellW*x, w)
        pygame.draw.line(screen, (36,51,5), lineStart, lineEnd, 2)

    for y in range(0, size+5, 5):
        lineStart = (gap, gap + cellW*y)
        lineEnd = (w, gap + cellW*y)
        pygame.draw.line(screen, (36,51,5), lineStart, lineEnd, 4)

    for x in range(0, size+5, 5):
        lineStart = (gap + cellW*x, gap)
        lineEnd = (gap + cellW*x, w)
        pygame.draw.line(screen, (36,51,5), lineStart, lineEnd, 4)

def exit_button(exitRect, clickSFX, stage, down, target):
    pygame.draw.rect(screen, (222, 130, 126), exitRect, border_radius=20)

    if exitRect.collidepoint(pygame.mouse.get_pos()) and not down:
        text = pygame.font.Font(FONT, 64).render("X", True, (255,255,255))
        textpos = text.get_rect(centerx=exitRect.centerx, centery=exitRect.centery)
        screen.blit(text, textpos)
        
        if pygame.mouse.get_pressed()[0]:
            clickSFX.play()
            stage = target

    else:
        text = pygame.font.Font(FONT, 48).render("X", True, (255,255,255))
        textpos = text.get_rect(centerx=exitRect.centerx, centery=exitRect.centery)
        screen.blit(text, textpos)
    
    return stage

def beach_setup(shopItemImgs, ogShopItemImgs, stage):
    r = load_data("save")
    beachBgNo = 0
    beachData = ""

    r = r.split(",")
    beachBgNo = r[2]
    beachData = r[4]

    if beachBgNo == '':
        stage = "pick-beach"
        beachBgNo = 0
    else:
        beachBgNo = int(beachBgNo)

    beachItemRects = []
    
    beachData = beachData.split()
    for i in range(len(beachData)):
        beachData[i] = beachData[i].split("/")
        beachData[i][0] = int(beachData[i][0])

        beachData[i][1] = beachData[i][1].split("-")
        
        beachData[i][1][0] = int(beachData[i][1][0]) # x
        beachData[i][1][1] = int(beachData[i][1][1]) # y
        beachData[i][1][2] = float(beachData[i][1][2]) # scale
        beachData[i][1][3] = int(beachData[i][1][3]) # rotation
        beachData[i][1][4] = int(beachData[i][1][4]) # flip

        shopItemImgs[beachData[i][0]] = pygame.transform.rotate(pygame.transform.scale(ogShopItemImgs[beachData[i][0]], (w*0.2 * beachData[i][1][2],  w*0.2*beachData[i][1][2])), beachData[i][1][3])
        beachItemRects.append(pygame.Rect(beachData[i][1][0], beachData[i][1][1], w*0.2 * beachData[i][1][2],  w*0.2*beachData[i][1][2]))
    
    if stage != "pick-beach":
        stage = "beach"

    moveItem = []

    return beachBgNo, beachData, beachItemRects, moveItem, stage

def display_selected_UI(beachItemRects, selecting, scaleRect, scaleImg, rotateRect, rotateImg, flipRect, flipImg, scaling, rotating, beachData, ogRotation, down):
    pygame.draw.rect(screen, (100,100,255), beachItemRects[selecting], 5)

    pygame.draw.rect(screen, "#768F74", scaleRect, border_radius=10)
    screen.blit(scaleImg, (scaleRect.x+w*0.005, scaleRect.y+w*0.005))

    pygame.draw.rect(screen, "#A3BF9F", rotateRect, border_radius=10)
    screen.blit(rotateImg, (rotateRect.x+w*0.005, rotateRect.y+w*0.005))

    pygame.draw.rect(screen, "#8CB48A", flipRect, border_radius=10)
    screen.blit(flipImg, (flipRect.x+w*0.005, flipRect.y+w*0.005))

    if scaleRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not rotating and not scaling:
        scaling = True

    if rotateRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not scaling and not rotating:
        rotating = True
        ogRotation = beachData[selecting][1][3]
    
    if flipRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not scaling and not rotating and not down:
        beachData[selecting][1][4] = (str((beachData[selecting][1][4] + 1) % 2))
        
        r = load_data("save")

        r = r.split(",")
        r[4] = r[4].split()

        r[4][selecting] = r[4][selecting].split("-")
        r[4][selecting][4] = str(beachData[selecting][1][4])
        r[4][selecting] = "-".join(r[4][selecting])

        r[4] = " ".join(r[4])
        r = ",".join(r)

        save_data(r, "save")
    
    return scaling, rotating, ogRotation

def scale_beach_img(beachData, selecting, beachItemRects, shopItemImgs, ogShopItemImgs, rotateRect, scaleRect, flipRect, moveItem):
    beachData[selecting][1][2] = (pygame.mouse.get_pos()[0] - beachItemRects[selecting].x) / (w*0.2)
    shopItemImgs[beachData[selecting][0]] = pygame.transform.scale(ogShopItemImgs[beachData[selecting][0]], (w*0.2 * beachData[selecting][1][2],  w*0.2*beachData[selecting][1][2]))
    
    beachItemRects[selecting] = pygame.Rect(beachData[selecting][1][0], beachData[selecting][1][1], w*0.2 * beachData[selecting][1][2],  w*0.2*beachData[selecting][1][2])

    scaleRect.centerx = beachItemRects[moveItem[-1]].x + beachItemRects[moveItem[-1]].w
    scaleRect.centery = beachItemRects[moveItem[-1]].y + beachItemRects[moveItem[-1]].h

    rotateRect.centerx = beachItemRects[moveItem[-1]].x
    rotateRect.centery = beachItemRects[moveItem[-1]].y + beachItemRects[moveItem[-1]].h

    flipRect.centerx = beachItemRects[moveItem[-1]].x + beachItemRects[moveItem[-1]].h
    flipRect.centery = beachItemRects[moveItem[-1]].y

    r = load_data("save")

    r = r.split(",")
    
    r[4] = r[4].split()
    r[4][moveItem[-1]] = f"{beachData[moveItem[-1]][0]}/{beachData[moveItem[-1]][1][0]}-{beachData[moveItem[-1]][1][1]}-{beachData[moveItem[-1]][1][2]}-{beachData[moveItem[-1]][1][3]}-{beachData[moveItem[-1]][1][4]}"
    
    r[4] = " ".join(r[4])
    
    r = ",".join(r)

    save_data(r, "save")

    return scaleRect, rotateRect, flipRect, beachItemRects

def move_beach_item(moveItem, beachData, posOffset, beachItemRects, scaleRect, rotateRect, flipRect):
    selecting = moveItem[-1]

    beachData[moveItem[-1]][1][0] = pygame.mouse.get_pos()[0] - posOffset[0]
    beachData[moveItem[-1]][1][1] = pygame.mouse.get_pos()[1] - posOffset[1]

    if beachData[moveItem[-1]][1][0] < 0:
        beachData[moveItem[-1]][1][0] = 0
    if beachData[moveItem[-1]][1][1] < 0:
        beachData[moveItem[-1]][1][1] = 0

    r = load_data("save")

    r = r.split(",")
    
    r[4] = r[4].split()
    r[4][moveItem[-1]] = f"{beachData[moveItem[-1]][0]}/{beachData[moveItem[-1]][1][0]}-{beachData[moveItem[-1]][1][1]}-{beachData[moveItem[-1]][1][2]}-{beachData[moveItem[-1]][1][3]}-{beachData[moveItem[-1]][1][4]}"
    
    r[4] = " ".join(r[4])
    
    r = ",".join(r)

    save_data(r, "save")

    beachItemRects[moveItem[-1]].x = beachData[moveItem[-1]][1][0]
    beachItemRects[moveItem[-1]].y = beachData[moveItem[-1]][1][1]

    scaleRect.centerx = beachItemRects[moveItem[-1]].x + beachItemRects[moveItem[-1]].w
    scaleRect.centery = beachItemRects[moveItem[-1]].y + beachItemRects[moveItem[-1]].h

    rotateRect.centerx = beachItemRects[moveItem[-1]].x
    rotateRect.centery = beachItemRects[moveItem[-1]].y + beachItemRects[moveItem[-1]].h

    flipRect.centerx = beachItemRects[moveItem[-1]].x + beachItemRects[moveItem[-1]].w
    flipRect.centery = beachItemRects[moveItem[-1]].y

    return selecting, scaleRect, rotateRect, flipRect

def beach_trash_button(moveItem, beachData, trashButtonRect, trashImgs, selecting, stage):
    pygame.draw.rect(screen, (173, 78, 78), trashButtonRect, border_radius=20)

    if trashButtonRect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(trashImgs[1], (trashButtonRect.x+w*0.01, trashButtonRect.y+w*0.01))

        if moveItem != [] and not pygame.mouse.get_pressed()[0]:
            stage = "beach setup"

            r = load_data("save")

            r = r.split(",")
            r[4] = r[4].split()
            r[4].pop(moveItem[-1])
            r[4] = " ".join(r[4])

            r[3] = r[3].split()
            r[3].append(str(beachData[moveItem[-1]][0]))
            r[3] = " ".join(r[3])

            r = ",".join(r)

            save_data(r, "save")

            selecting = -1

    else:
        screen.blit(trashImgs[0], (trashButtonRect.x+w*0.01, trashButtonRect.y+w*0.01))
    
    return selecting, stage

def beach_add_button(addButtonRect, stage, clickSFX, down):
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

async def main():
    # acceleration: the acceleration of the animation before solving
    # galleryColors: holds data of the images in the gallery (which one is 0 or 1)
    # clickBg: if the background is selected to unselect items on the beach

    size, gap, cellW, hp, offset, acceleration, down, solveDown, colors, solveNext,\
        checkButtonRect, checkButtonImg, crossImg,\
        cellTimers, boardSolution, boardSolving, boardRects,\
        yinfo, xinfo, yinfoRects, xinfoRects,\
        darken, opacity, fade, fadeo,\
        choosePredrawnRect, chooseCustomRect,\
        playRect, drawRect, playBubble, drawBubble,\
        sanddollarRect, sanddollarImg,\
        shopButtonRect, ogShopImg, shopImg,\
        galleryButtonRect, ogGalleryImg, galleryImg,\
        beachButtonRect, ogBeachImg, beachImg,\
        yesRect, noRect, claimSanddollarRect,\
        popupExitRect, galleryBg, galleryData,\
        galleryBigRects, gallerySmallRects,\
        galleryColors, galleryPage, FlipLeftRect, FlipRightRect,\
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
        infoButtonRect, ogInfoImg, infoImg,\
        infoPageBg, infoPageBgBold, infoRect,\
        instructionPages, instructionPageNo,\
        XO, heartXOimg, heartRect = setup()

    pygame.mixer.music.load("music/bgm.ogg")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    clickSFX = pygame.mixer.Sound("music/click.ogg")
    clickSFX.set_volume(0.2)
    flipSFX = pygame.mixer.Sound("music/flip.ogg")
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
            pygame.draw.rect(screen, (248, 250, 247), shopButtonRect, border_radius=20)

            if shopButtonRect.collidepoint(pygame.mouse.get_pos()):
                shopImg = pygame.transform.scale(ogShopImg, (w*0.09, w*0.09))

                if pygame.mouse.get_pressed()[0]:
                    stage = "shop"
                    shopPage = 0
                    clickSFX.play()
            else:
                shopImg = pygame.transform.scale(ogShopImg, (w*0.08, w*0.08))

            screen.blit(shopImg, (shopButtonRect.centerx - shopImg.get_size()[0]/2,
                                  shopButtonRect.centery-shopImg.get_size()[1]/2))
            
            # gallery
            pygame.draw.rect(screen, (248, 250, 247), galleryButtonRect, border_radius=20)

            if galleryButtonRect.collidepoint(pygame.mouse.get_pos()):
                galleryImg = pygame.transform.scale(ogGalleryImg, (w*0.09, w*0.09))

                if pygame.mouse.get_pressed()[0]:
                    stage = "gallery setup"
                    clickSFX.play()

            else:
                galleryImg = pygame.transform.scale(ogGalleryImg, (w*0.08, w*0.08))
            
            screen.blit(galleryImg, (galleryButtonRect.centerx - galleryImg.get_size()[0]/2,
                                     galleryButtonRect.centery-galleryImg.get_size()[1]/2))
            
            # beach
            pygame.draw.rect(screen, (248, 250, 247), beachButtonRect, border_radius=20)

            if beachButtonRect.collidepoint(pygame.mouse.get_pos()):
                beachImg = pygame.transform.scale(ogBeachImg, (w*0.09, w*0.09))

                if pygame.mouse.get_pressed()[0]:
                    stage = "beach setup"
                    clickSFX.play()
                    down = True

            else:
                beachImg = pygame.transform.scale(ogBeachImg, (w*0.08, w*0.08))
            
            screen.blit(beachImg, (beachButtonRect.centerx - beachImg.get_size()[0]/2,
                                   beachButtonRect.centery-beachImg.get_size()[1]/2))
        
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
            pygame.draw.rect(screen, (248, 250, 247), infoButtonRect, border_radius=20)

            if infoButtonRect.collidepoint(pygame.mouse.get_pos()):
                infoImg = pygame.transform.scale(ogInfoImg, (w*0.09, w*0.09))

                if pygame.mouse.get_pressed()[0] and not down:
                    stage = "info"
                    clickSFX.play()

            else:
                infoImg = pygame.transform.scale(ogInfoImg, (w*0.08, w*0.08))
            
            screen.blit(infoImg, (infoButtonRect.centerx - infoImg.get_size()[0]/2,
                                  infoButtonRect.centery-infoImg.get_size()[1]/2))

            # play button
            pygame.draw.rect(screen, (66, 99, 52), playRect, border_radius=20)

            if playRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.Font(FONT, 72).render("Play", True, (171, 204, 157))
                textpos = text.get_rect(centerx=playRect.centerx, centery=playRect.centery)
                screen.blit(text, textpos)

                screen.blit(playBubble, (w*0.2, playRect.y - w*0.2))

                text = pygame.font.Font(FONT, 24).render("Solve a nonogram", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=playRect.y - w*0.15)
                screen.blit(text, textpos)

                text = pygame.font.Font(FONT, 24).render("Earn sand dollars", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=playRect.y - w*0.1)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    stage = "choose-solve"
                    clickSFX.play()

            else:
                text = pygame.font.Font(FONT, 64).render("Play", True, (171, 204, 157))
                textpos = text.get_rect(centerx=playRect.centerx, centery=playRect.centery)
                screen.blit(text, textpos)

            # draw button
            pygame.draw.rect(screen, (171, 204, 157), drawRect, border_radius=20)

            if drawRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.Font(FONT, 53).render("Draw", True, (66, 99, 52))
                textpos = text.get_rect(centerx=drawRect.centerx, centery=drawRect.centery)
                screen.blit(text, textpos)

                screen.blit(drawBubble, (w*0.2, drawRect.y + w*0.12))

                text = pygame.font.Font(FONT, 24).render("Draw and solve your own nonogram", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=drawRect.y + w*0.21)
                screen.blit(text, textpos)

                text = pygame.font.Font(FONT, 24).render("Doesn't earn sand dollars", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=drawRect.y + w*0.26)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    stage = "animation-for-draw"
                    clickSFX.play()
            
            else:
                text = pygame.font.Font(FONT, 48).render("Draw", True, (66, 99, 52))
                textpos = text.get_rect(centerx=drawRect.centerx, centery=drawRect.centery)
                screen.blit(text, textpos)

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

            if instructionPageNo > 0:
                pygame.draw.rect(screen, (91, 107, 79), FlipLeftRect, border_radius=20)

                if FlipLeftRect.collidepoint(pygame.mouse.get_pos()):
                    text = pygame.font.Font(FONT, 96).render("<", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                    screen.blit(text, textpos)

                    if pygame.mouse.get_pressed()[0] and not down:
                        instructionPageNo -= 1
                        flipSFX.play()
                else:
                    text = pygame.font.Font(FONT, 64).render("<", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                    screen.blit(text, textpos)

            if instructionPageNo < len(instructionPages)-1:
                pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

                if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
                    text = pygame.font.Font(FONT, 96).render(">", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                    screen.blit(text, textpos)

                    if pygame.mouse.get_pressed()[0] and not down:
                        instructionPageNo += 1
                        flipSFX.play()
                else:
                    text = pygame.font.Font(FONT, 64).render(">", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                    screen.blit(text, textpos)

            stage = exit_button(popupExitRect, clickSFX, stage, down, "info")

        elif stage.split()[0] == "gallery": # view solved nonograms in gallery
            pygame.draw.rect(screen, (241, 245, 237), galleryBg, border_radius=10)

            if len(stage.split()) > 1 and stage.split()[1] == "setup":
                galleryData = []
                galleryBigRects = []
                gallerySmallRects = []
                galleryColors = []


                saveR = load_data("save")
                galleryR = load_data("gallery").strip().splitlines()
                
                saveR = saveR.split(",")
                galleryData = saveR[1].split("-")

                if galleryData != [""]:
                    data = ""
                    for i in range(len(galleryData)):
                        galleryBigRects.append(pygame.Rect(w*0.2+((i%4)%2 * w*0.35), w*0.2+((i%4)//2 * w*0.35), w*0.25, w*0.25))

                        if galleryData[i][0] == "p":
                            galleryData[i] = galleryData[i][1:]
                            data = PREDRAWN[int(galleryData[i])].split(" ")
                        else:
                            data = galleryR[int(galleryData[i])].split(" ")
                        datasize = int(data[0])
                        data = data[1]

                        dataW = (galleryBigRects[-1].w - w*0.02)/datasize

                        gallerySmallRects.append([])
                        for y in range(datasize):
                            for x in range(datasize):
                                gallerySmallRects[-1].append(pygame.Rect(galleryBigRects[-1].x + w*0.01 + dataW*x, galleryBigRects[-1].y + w*0.01 + dataW*y, dataW, dataW))
                        
                        galleryColors.append(list(data))

                    stage = "gallery"
                    galleryPage = 0

            for y in range(galleryPage*4,galleryPage*4+4):
                if len(galleryBigRects) > y:
                    pygame.draw.rect(screen, (60, 64, 57), galleryBigRects[y], border_radius=10)

                    for x in range(len(gallerySmallRects[y])):
                        if x == 0:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], gallerySmallRects[y][x], border_top_left_radius=10)
                        elif x == datasize-1:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], gallerySmallRects[y][x], border_top_right_radius=10)
                        elif x == datasize**2-datasize:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], gallerySmallRects[y][x], border_bottom_left_radius=10)
                        elif x == datasize**2-1:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], gallerySmallRects[y][x], border_bottom_right_radius=10)
                        else:
                            pygame.draw.rect(screen, colors[int(galleryColors[y][x])], gallerySmallRects[y][x])
            
            if galleryPage > 0:
                pygame.draw.rect(screen, (91, 107, 79), FlipLeftRect, border_radius=20)

                if FlipLeftRect.collidepoint(pygame.mouse.get_pos()):
                    text = pygame.font.Font(FONT, 96).render("<", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                    screen.blit(text, textpos)

                    if pygame.mouse.get_pressed()[0] and not down:
                        galleryPage -= 1
                        flipSFX.play()
                else:
                    text = pygame.font.Font(FONT, 64).render("<", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                    screen.blit(text, textpos)

            if galleryPage < (len(galleryBigRects)-1)//4:
                pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

                if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
                    text = pygame.font.Font(FONT, 96).render(">", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                    screen.blit(text, textpos)

                    if pygame.mouse.get_pressed()[0] and not down:
                        galleryPage += 1
                        flipSFX.play()
                else:
                    text = pygame.font.Font(FONT, 64).render(">", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                    screen.blit(text, textpos)

            if key[pygame.K_LEFT] and galleryPage > 0 and not down:
                galleryPage -= 1
            if key[pygame.K_RIGHT] and galleryPage < (len(galleryBigRects)-1)//4 and not down:
                galleryPage += 1

            stage = exit_button(popupExitRect, clickSFX, stage, down, "home")

        elif stage == "shop": # buy items for beach
            pygame.draw.rect(screen, (249, 250, 242), shopBg, border_radius=10)

            for i in range(shopPage*4,shopPage*4+4):
                if len(shopItemRects) > i:
                    pygame.draw.rect(screen, (204, 209, 171), shopItemRects[i], border_radius=10)

                    if shopItemRects[i].collidepoint(pygame.mouse.get_pos()):
                        shopItemImgs[i] = pygame.transform.scale(ogShopItemImgs[i], (w*0.2, w*0.2))
                        screen.blit(shopItemImgs[i], (shopItemRects[i].centerx - w*0.1, shopItemRects[i].centery - w*0.15))

                        if pygame.mouse.get_pressed()[0] and not down:
                            if sanddollar >= shopItemPrice[i]:
                                shopSDAnimateTxt = str(shopItemPrice[i])
                                shopSDAnimate = 20
                                clickSFX.play()
                                r = load_data("save")

                                # adding item to inventory
                                r = r.split(",")
                                r[3] = r[3].split(" ")
                                r[3].append(str(i))

                                r[3] = " ".join(r[3])
                                r[3] = r[3].strip(" ")
                                r = ",".join(r)

                                # minus money
                                sanddollar -= shopItemPrice[i]

                                r = r.split(",")
                                r[0] = str(sanddollar)
                                r = ",".join(r)

                                save_data(r, "save")
                    
                    else:
                        shopItemImgs[i] = pygame.transform.scale(ogShopItemImgs[i], (w*0.18, w*0.18))
                        screen.blit(shopItemImgs[i], (shopItemRects[i].centerx - w*0.09, shopItemRects[i].centery - w*0.14))

                    text = pygame.font.Font(FONT, 48).render("$"+str(shopItemPrice[i]), True, (80, 82, 66))
                    textpos = text.get_rect(centerx=shopItemRects[i].centerx, centery=shopItemRects[i].centery + w*0.1)
                    screen.blit(text, textpos)
            
            if shopPage > 0:
                pygame.draw.rect(screen, (91, 107, 79), FlipLeftRect, border_radius=20)

                if FlipLeftRect.collidepoint(pygame.mouse.get_pos()):
                    text = pygame.font.Font(FONT, 96).render("<", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                    screen.blit(text, textpos)

                    if pygame.mouse.get_pressed()[0] and not down:
                        shopPage -= 1
                        flipSFX.play()
                else:
                    text = pygame.font.Font(FONT, 64).render("<", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                    screen.blit(text, textpos)

            if shopPage < (len(shopItemRects)-1)//4:
                pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

                if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
                    text = pygame.font.Font(FONT, 96).render(">", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                    screen.blit(text, textpos)

                    if pygame.mouse.get_pressed()[0] and not down:
                        shopPage += 1
                        flipSFX.play()
                else:
                    text = pygame.font.Font(FONT, 64).render(">", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                    screen.blit(text, textpos)

            if key[pygame.K_LEFT] and shopPage > 0 and not down:
                shopPage -= 1
            if key[pygame.K_RIGHT] and shopPage < (len(shopItemRects)-1)//4 and not down:
                shopPage += 1

            sanddollarRect = pygame.Rect(w*0.04, w*0.02, w*0.35, w*0.1)

            pygame.draw.rect(screen, "#CAD4C5", sanddollarRect, border_radius=20)
            screen.blit(sanddollarImg, (sanddollarRect.x+w*0.02, sanddollarRect.centery-w*0.035))

            sdShowTxt = str(sanddollar)
            if len(sdShowTxt) > 9:
                sdShowTxt = str(int(sanddollar/1000000))+"M"
            elif len(sdShowTxt) > 5:
                sdShowTxt = str(int(sanddollar/1000))+"K"

            text = pygame.font.Font(FONT, 48).render(sdShowTxt, True, (66, 99, 52))
            textpos = text.get_rect(x=sanddollarRect.x+w*0.12, centery=sanddollarRect.centery-w*0.003)
            screen.blit(text, textpos)

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

            if key[pygame.K_LEFT] and not down:
                beachBgNo -= 1
            if key[pygame.K_RIGHT] and not down:
                beachBgNo += 1
            
            pygame.draw.rect(screen, (91, 107, 79), FlipLeftRect, border_radius=20)

            if FlipLeftRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.Font(FONT, 96).render("<", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    beachBgNo -= 1
                    flipSFX.play()
            else:
                text = pygame.font.Font(FONT, 64).render("<", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                screen.blit(text, textpos)

            pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

            if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.Font(FONT, 96).render(">", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    beachBgNo += 1
                    flipSFX.play()
            else:
                text = pygame.font.Font(FONT, 64).render(">", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                screen.blit(text, textpos)
            
            beachBgNo = beachBgNo % 3

            screen.blit(beachConfirmButtonImg, (w*0.45,w*0.88))

            if beachConfirmButtonRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not down:
                clickSFX.play()
                stage = "beach setup"

                r = load_data("save")

                r = r.split(",")
                r[2] = str(beachBgNo)

                r = ",".join(r)

                save_data(r, "save")

        elif stage.split()[0] == "beach": # beach main screen
            if len(stage.split()) > 1 and stage.split()[1] == "setup":
                beachBgNo, beachData, beachItemRects, moveItem, stage = beach_setup(shopItemImgs, ogShopItemImgs, stage)

            screen.blit(beachBgImgs[beachBgNo], (0,0))

            clickBg = True

            if not down:
                moveItem = []

            for i in range(len(beachData)):
                scaled_img = pygame.transform.scale(ogShopItemImgs[beachData[i][0]], (int(beachData[i][1][2]*w*0.2), int(beachData[i][1][2]*w*0.2)))
                center = (beachData[i][1][0] + scaled_img.get_width() // 2, beachData[i][1][1] + scaled_img.get_height() // 2)
                img = pygame.transform.flip(pygame.transform.rotate(scaled_img, int(beachData[i][1][3])), int(beachData[i][1][4]), False)
                rect = img.get_rect(center=center)
                screen.blit(img, rect)

                if beachItemRects[i].collidepoint(pygame.mouse.get_pos())\
                    and pygame.mouse.get_pressed()[0] and not down:
                    moveItem.append(i)

                    posOffset = (pygame.mouse.get_pos()[0]-beachData[moveItem[-1]][1][0], pygame.mouse.get_pos()[1]-beachData[moveItem[-1]][1][1])
                    clickBg = False
            
            if pygame.mouse.get_pressed()[0] and clickBg and moveItem == []: # reset selecting if bg is clicked
                selecting = -1
            
            # do things to selected object (blit stuff)
            if selecting != -1:
                scaling, rotating, ogRotation = display_selected_UI(beachItemRects, selecting, scaleRect, scaleImg, rotateRect, rotateImg, flipRect, flipImg, scaling, rotating, beachData, ogRotation, down)
            
            if rotating:
                # find the distance between center of the image and mouse pos and then use trig to find angle to rotate
                try:
                    center = (beachItemRects[selecting].centerx, beachItemRects[selecting].centery)
                    mouse = pygame.mouse.get_pos()
                    diff = (mouse[0] - center[0], center[1] - mouse[1]) 
                    angle = int(math.atan2(diff[1], diff[0]) * 180 / math.pi)

                    beachData[selecting][1][3] = (ogRotation - angle - 135) % 360
                    
                    r = load_data("save")
                    r = r.split(",")
                    r[4] = r[4].split()
                    r[4][selecting] = f"{beachData[selecting][0]}/{beachData[selecting][1][0]}-{beachData[selecting][1][1]}-{beachData[selecting][1][2]}-{beachData[selecting][1][3]}-{beachData[selecting][1][4]}"
                    r[4] = " ".join(r[4])
                    r = ",".join(r)
                    save_data(r, "save")

                except: pass
                
            if scaling:
                if (pygame.mouse.get_pos()[0] - beachItemRects[selecting].x) / (w*0.2) > 0.3:
                    scaleRect, rotateRect, flipRect, beachItemRects = scale_beach_img(beachData, selecting, beachItemRects, shopItemImgs, ogShopItemImgs, rotateRect, scaleRect, flipRect, moveItem)

            if moveItem != [] and not scaleRect.collidepoint(pygame.mouse.get_pos()) and not rotateRect.collidepoint(pygame.mouse.get_pos()) and not scaling and not rotating: # move item
                selecting, scaleRect, rotateRect, flipRect = move_beach_item(moveItem, beachData, posOffset, beachItemRects, scaleRect, rotateRect, flipRect)
            
            if not pygame.mouse.get_pressed()[0]:
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
                
                r = load_data("save")

                addData = ""

                r = r.split(",")
                addData = r[3]
                
                addData = addData.split()

                for i in range(len(addData)):
                    addData[i] = int(addData[i])
                
                addItemRects = []
                for i in range(len(addData)):
                    addItemRects.append(pygame.Rect(w*0.18+((i%9)%3 * w*0.22), w*0.18+((i%9)//3 * w*0.22), w*0.2, w*0.2))

            for i in range(addPage*9, addPage*9+9):
                if len(addItemRects) > i:
                    pygame.draw.rect(screen, (149, 163, 135), addItemRects[i], border_radius=20)
                    
                    if addItemRects[i].collidepoint(pygame.mouse.get_pos()):
                        shopItemImgs[addData[i]] = pygame.transform.scale(ogShopItemImgs[addData[i]], (w*0.17, w*0.17))
                        screen.blit(shopItemImgs[addData[i]], (addItemRects[i].centerx-w*0.085, addItemRects[i].centery-w*0.085))

                        if pygame.mouse.get_pressed()[0]:
                            stage = "beach setup"

                            r = load_data("save")

                            r = r.split(",")
                            r[4] = r[4].split()
                            r[3] = r[3].split()

                            r[3].remove(str(addData[i]))
                            r[4].append(f"{str(addData[i])}/{int(random.randint(int(w/4), int(w/4)*3))}-{int(random.randint(int(w/4), int(w/4)*3))}-1-0-0")
                            r[4] = " ".join(r[4])
                            r[3] = " ".join(r[3])

                            r = ",".join(r)

                            save_data(r, "save")
                    
                    else:
                        shopItemImgs[addData[i]] = pygame.transform.scale(ogShopItemImgs[addData[i]], (w*0.15, w*0.15))
                        screen.blit(shopItemImgs[addData[i]], (addItemRects[i].centerx-w*0.075, addItemRects[i].centery-w*0.075))
            
            if addPage > 0:
                pygame.draw.rect(screen, (91, 107, 79), FlipLeftRect, border_radius=20)

                if FlipLeftRect.collidepoint(pygame.mouse.get_pos()):
                    text = pygame.font.Font(FONT, 96).render("<", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                    screen.blit(text, textpos)

                    if pygame.mouse.get_pressed()[0] and not down:
                        addPage -= 1
                        flipSFX.play()
                else:
                    text = pygame.font.Font(FONT, 64).render("<", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                    screen.blit(text, textpos)

            if addPage < (len(addData)-1)//9:
                pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

                if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
                    text = pygame.font.Font(FONT, 96).render(">", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                    screen.blit(text, textpos)

                    if pygame.mouse.get_pressed()[0] and not down:
                        addPage += 1
                        flipSFX.play()
                else:
                    text = pygame.font.Font(FONT, 64).render(">", True, (255,255,255))
                    textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                    screen.blit(text, textpos)

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

            offset += acceleration

            if w/2+offset < w/8:
                acceleration += 0.2
            elif w/2+offset < w/4*3:
                if acceleration > 5:
                    acceleration /= 1.02
            else:
                acceleration += 0.2

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
                        boardSolution[y][x] = 1
                    if boardRects[y][x].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[2]:
                        boardSolution[y][x] = 0
            
            # done
            if checkButtonRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                stage = "animation-for-solve"

                # info stuff checking stuff
                for y in range(size):
                    yinfo.append("")
                    for x in range(size):
                        if boardSolution[y][x] == 0:
                            yinfo[y] += " "
                        else:
                            yinfo[y] += "#"
                    yinfo[y] = yinfo[y].split()
                    
                    for i in range(len(yinfo[y])):
                        yinfo[y][i] = str(len(yinfo[y][i]))

                for x in range(size):
                    xinfo.append("")
                    for y in range(size):
                        if boardSolution[y][x] == 0:
                            xinfo[x] += " "
                        else:
                            xinfo[x] += "#"
                    xinfo[x] = xinfo[x].split()
                    
                    for i in range(len(xinfo[x])):
                        xinfo[x][i] = str(len(xinfo[x][i]))
        
        elif stage == "choose-solve": # screen to chose to play custom drawn or pr-drawn
            # pre-drawn button
            pygame.draw.rect(screen, (66, 99, 52), choosePredrawnRect, border_radius=20)

            if choosePredrawnRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.Font(FONT, 72).render("Pre-drawn", True, (171, 204, 157))
                textpos = text.get_rect(centerx=choosePredrawnRect.centerx, centery=choosePredrawnRect.centery)
                screen.blit(text, textpos)

                screen.blit(playBubble, (w*0.2, playRect.y - w*0.2))

                text = pygame.font.Font(FONT, 24).render("Solve a pre-drawn nonogram", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=playRect.y - w*0.15)
                screen.blit(text, textpos)

                text = pygame.font.Font(FONT, 24).render("Earn sand dollars", True, (51, 66, 44))
                textpos = text.get_rect(centerx=w/2, centery=playRect.y - w*0.1)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    stage = "animation-for-solve get-from-gallery pre-drawn"
                    clickSFX.play()

            else:
                text = pygame.font.Font(FONT, 64).render("Pre-drawn", True, (171, 204, 157))
                textpos = text.get_rect(centerx=choosePredrawnRect.centerx, centery=choosePredrawnRect.centery)
                screen.blit(text, textpos)

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
                    solveNext = random.randint(1,len(r)-1)
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
                
                # info stuff checking stuff
                for y in range(size):
                    yinfo.append("")
                    for x in range(size):
                        if boardSolution[y][x] == 0:
                            yinfo[y] += " "
                        else:
                            yinfo[y] += "#"
                    yinfo[y] = yinfo[y].split()
                    for i in range(len(yinfo[y])):
                        yinfo[y][i] = str(len(yinfo[y][i]))

                for x in range(size):
                    xinfo.append("")
                    for y in range(size):
                        if boardSolution[y][x] == 0:
                            xinfo[x] += " "
                        else:
                            xinfo[x] += "#"
                    xinfo[x] = xinfo[x].split()
                    
                    for i in range(len(xinfo[x])):
                        xinfo[x][i] = str(len(xinfo[x][i]))

                stage = stage.split()
                stage[1] = "earn-sanddollar"
                stage = " ".join(stage)

            drawBoard(size, screen, colors, boardSolving, gap, w, cellW, boardRects, crossImg, cellTimers)

            screen.blit(heartXOimg[XO], (0,0))

            text = pygame.font.Font(FONT, 32).render(str(hp)+"%", True, (247, 225, 237))
            textpos = text.get_rect(centerx=gap/2, centery=gap/5*4)
            screen.blit(text, textpos)

            # draw background for info
            for y in yinfoRects:
                pygame.draw.rect(screen, (52, 74, 36), y, border_top_left_radius=10, border_bottom_left_radius=10)
            
            for x in xinfoRects:
                pygame.draw.rect(screen, (52, 74, 36), x, border_top_left_radius=10, border_top_right_radius=10)
            
            # draw info
            for y in range(size):
                text = pygame.font.Font(FONT, 24).render(" ".join(yinfo[y]), True, (255,255,255))
                textpos = text.get_rect(centerx=yinfoRects[y].centerx, centery=yinfoRects[y].centery)
                screen.blit(text, textpos)
            
            for x in range(size):
                for i in range(len(xinfo[x])):
                    text = pygame.font.Font(FONT, 24).render((xinfo[x][i]), True, (255,255,255))
                    textpos = text.get_rect(centerx=xinfoRects[x].centerx, y=xinfoRects[x].y + xinfoRects[x].h*i/len(xinfo[x]))
                    screen.blit(text, textpos)

            screen.blit(fade, (0,0))

            text = pygame.font.Font(FONT, 96).render("Solve!", True, (255,255,255))
            textpos = text.get_rect(centerx=w/2+offset, centery=w/2)
            screen.blit(text, textpos)

            offset += acceleration

            if w/2+offset < w/8:
                acceleration += 0.2
            elif w/2+offset < w/4*3:
                if acceleration > 5:
                    acceleration /= 1.02
            else:
                acceleration += 0.2

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

            # draw background for info
            for y in yinfoRects:
                pygame.draw.rect(screen, (52, 74, 36), y, border_top_left_radius=10, border_bottom_left_radius=10)
            
            for x in xinfoRects:
                pygame.draw.rect(screen, (52, 74, 36), x, border_top_left_radius=10, border_top_right_radius=10)
            
            # draw info
            for y in range(size):
                text = pygame.font.Font(FONT, 24).render(" ".join(yinfo[y]), True, (255,255,255))
                textpos = text.get_rect(centerx=yinfoRects[y].centerx, centery=yinfoRects[y].centery)
                screen.blit(text, textpos)
            
            for x in range(size):
                for i in range(len(xinfo[x])):
                    text = pygame.font.Font(FONT, 24).render((xinfo[x][i]), True, (255,255,255))
                    textpos = text.get_rect(centerx=xinfoRects[x].centerx, y=xinfoRects[x].y + xinfoRects[x].h*i/len(xinfo[x]))
                    screen.blit(text, textpos)

            fade.fill((0, 0, 0, fadeo))
            screen.blit(fade, (0,0))
            fadeo -= acceleration
            acceleration += 0.5

            if fadeo <= 0:
                stage = stage.split()
                stage[0] = "solve"
                stage = " ".join(stage)
        
        elif stage.split()[0] == "solve": # solve the nonogram
            drawBoard(size, screen, colors, boardSolving, gap, w, cellW, boardRects, crossImg, cellTimers)

            screen.blit(heartXOimg[XO], heartRect)
            if pygame.mouse.get_pressed()[0] and heartRect.collidepoint(pygame.mouse.get_pos()) and not down:
                if XO == "X":
                    XO = "O"
                else:
                    XO = "X"
                clickSFX.play()

            # draw background for info
            for y in yinfoRects:
                pygame.draw.rect(screen, (52, 74, 36), y, border_top_left_radius=10, border_bottom_left_radius=10)
            
            for x in xinfoRects:
                pygame.draw.rect(screen, (52, 74, 36), x, border_top_left_radius=10, border_top_right_radius=10)
            
            # draw info
            for y in range(size):
                text = pygame.font.Font(FONT, 24).render(" ".join(yinfo[y]), True, (255,255,255))
                textpos = text.get_rect(centerx=yinfoRects[y].centerx, centery=yinfoRects[y].centery)
                screen.blit(text, textpos)
            
            for x in range(size):
                for i in range(len(xinfo[x])):
                    text = pygame.font.Font(FONT, 24).render((xinfo[x][i]), True, (255,255,255))
                    textpos = text.get_rect(centerx=xinfoRects[x].centerx, y=xinfoRects[x].y + xinfoRects[x].h*i/len(xinfo[x]))
                    screen.blit(text, textpos)
            
            # check for fill
            for y in range(size):
                for x in range(size):
                    if boardRects[y][x].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and (boardSolving[y][x] == 0 or boardSolving[y][x] == 3) and not solveDown and XO == "O":
                        if boardSolution[y][x] == 1:
                            boardSolving[y][x] = 1
                        else:
                            boardSolving[y][x] = 3
                            cellTimers[y][x] = 60
                            hp -= 8
                            solveDown = True

                    if boardRects[y][x].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and (boardSolving[y][x] == 0 or boardSolving[y][x] == 3) and not solveDown and XO == "X":
                        if boardSolution[y][x] == 0:
                            boardSolving[y][x] = 2
                        else:
                            boardSolving[y][x] = 3
                            cellTimers[y][x] = 60
                            hp -= 8
                            solveDown = True

            text = pygame.font.Font(FONT, 32).render(str(hp)+"%", True, (247, 225, 237))
            textpos = text.get_rect(centerx=gap/2, centery=gap/5*4)
            screen.blit(text, textpos)

            won = True
            for y in range(size):
                for x in range(size):
                    if not (boardSolving[y][x] == boardSolution[y][x] or (boardSolving[y][x] == 2 and boardSolution[y][x] == 0)):
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
                    pygame.draw.rect(screen, (158, 189, 115), claimSanddollarRect, border_radius=20)
                    text = pygame.font.Font(FONT, 48).render(f"Claim sand dollar {earndollar}x", True, (52, 64, 36))
                    textpos = text.get_rect(centerx=claimSanddollarRect.centerx, centery=claimSanddollarRect.centery)
                    screen.blit(text, textpos)

                    if claimSanddollarRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                        clickSFX.play()
                        sanddollar += earndollar

                        if stage.split()[0] == "win":
                            r = load_data("save")

                            r = r.split(",")
                            r[0] = str(sanddollar)
                            r[1] = r[1].split("-")
                            r[1].append(str(solveNext))
                            r[1] = "-".join(r[1])
                            r[1] = r[1].strip("-")
                            r = ",".join(r)

                            save_data(r, "save")

                        stage = "reset"

                else:
                    text = pygame.font.Font(FONT, 64).render("Publish image?", True, (157, 166, 144))
                    textpos = text.get_rect(centerx=w/2, centery=w*0.55)
                    screen.blit(text, textpos)

                    pygame.draw.rect(screen, (158, 189, 115), yesRect, border_radius=20)
                    text = pygame.font.Font(FONT, 48).render("Yes", True, (52, 64, 36))
                    textpos = text.get_rect(centerx=yesRect.centerx, centery=yesRect.centery)
                    screen.blit(text, textpos)

                    pygame.draw.rect(screen, (189, 117, 115), noRect, border_radius=20)
                    text = pygame.font.Font(FONT, 48).render("No", True, (52, 64, 36))
                    textpos = text.get_rect(centerx=noRect.centerx, centery=noRect.centery)
                    screen.blit(text, textpos)

                    if yesRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                        clickSFX.play()
                        r = load_data("gallery").strip()

                        r += "\n" + str(size)+" "
                        for y in boardSolution:
                            for x in y:
                                r += str(x)
                        
                        solveNext = len(r.splitlines()) - 1

                        save_data(r, "gallery")
                        print(solveNext)

                        r = load_data("save")

                        r = r.split(",")
                        r[1] = r[1].split("-")
                        r[1].append(str(solveNext))
                        r[1] = "-".join(r[1])
                        r[1] = r[1].strip("-")
                        r = ",".join(r)

                        save_data(r, "save")

                        solveNext = -1

                        stage = "reset"
                    
                    if noRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                        clickSFX.play()
                        stage = "reset"

        elif stage == "reset": # reset everything after solving a nonogram
            boardSolution, boardSolving, boardRects = setupBoards(size, cellW, gap)

            colors = ((185, 191, 153), (75, 83, 32), (255, 255, 255), (252, 93, 93)) # filled and not filled nonogram colors

            checkButtonRect = pygame.Rect(gap*0.1, gap*0.1, gap*0.8, gap*0.8)

            # info for the sides
            yinfo, xinfo, yinfoRects, xinfoRects = setupInfo(size, gap, cellW)

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