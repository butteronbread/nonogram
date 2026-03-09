import pygame, math, random

pygame.init()

w = 720

screen = pygame.display.set_mode((w,w))

clock = pygame.time.Clock()

pygame.display.set_caption("Nonogram")

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, addto):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    addto.append(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(350, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def drawBoard(size, screen, colors, board, gap, w, cellW):
    for y in range(size):
        for x in range(size):
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

size = 15 # pixels for the drawing width and height

boardSolution = [] # answer
for y in range(size):
    boardSolution.append([])
    for x in range(size):
        boardSolution[-1].append(0)

boardSolving = [] # the current stage of the board while solving
for y in range(size):
    boardSolving.append([])
    for x in range(size):
        boardSolving[-1].append(0)

gap = w*0.122
cellW = math.floor((w-gap)/size) # gap of 3 on top and left for numbers

boardRects = []
for y in range(size):
    boardRects.append([])
    for x in range(size):
        boardRects[-1].append(pygame.Rect(x*cellW + gap, y*cellW + gap, cellW, cellW))

colors = ((185, 191, 153), (75, 83, 32), (255, 255, 255), (252, 93, 93)) # filled and not filled nonogram colors

checkButtonRect = pygame.Rect(gap*0.1, gap*0.1, gap*0.8, gap*0.8)
checkButtonImg = pygame.transform.scale(pygame.image.load("check.png"), (gap*0.8, gap*0.8))

heartImg = pygame.transform.scale(pygame.image.load("heart.png"), (gap, gap))

# info for the sides
yinfo = []
xinfo = []

yinfoRects = []
for y in range(size):
    yinfoRects.append(pygame.Rect(0, gap+cellW*y+3, gap, cellW-6))

xinfoRects = []
for x in range(size):
    xinfoRects.append(pygame.Rect(gap+cellW*x+3, 0, cellW-6, gap))

# for win and loose and animation word screen
darken = pygame.Surface((w,w), pygame.SRCALPHA)
darken.fill((0, 0, 0, 0))
opacity = 0

# for fade in and out of the darken
fade = pygame.Surface((w,w), pygame.SRCALPHA)
fade.fill((0, 0, 0, 127))
fadeo = 127

# login, signup stuff
loginRect = pygame.Rect(0,0,w*0.4,w*0.15)
loginRect.centerx = w/2
loginRect.centery = w*0.3

signupRect = pygame.Rect(0,0,w*0.4,w*0.15)
signupRect.centerx = w/2
signupRect.centery = w*0.6

loginUsername = InputBox(w/2-175, w*0.5-24, 350, 32)
loginPassword = InputBox(w/2-175, w*0.7-24, 350, 32)
loginInputs = [loginUsername, loginPassword]

signupUsername = InputBox(w/2-175, w*0.5-24, 350, 32)
signupPassword = InputBox(w/2-175, w*0.7-24, 350, 32)
signupInputs = [signupUsername, signupPassword]

validCredit = True

# home screen stuff
playRect = pygame.Rect(0,0,w*0.4,w*0.15) # play button: Solve a pre-drawn nonogram. Earn coins according to puzzle difficulty
playRect.centerx = w/2
playRect.centery = w*0.35

drawRect = pygame.Rect(0,0,w*0.3,w*0.12) # draw button: Draw and solve your own nonogram design. This will not increase coins
drawRect.centerx = w/2
drawRect.centery = w*0.55

playBubble = pygame.transform.scale(pygame.image.load("upbubble.png"), (w*0.6, w*0.2))
drawBubble = pygame.transform.scale(pygame.image.load("downbubble.png"), (w*0.6, w*0.2))

sanddollarRect = pygame.Rect(w*0.63, w*0.02, w*0.35, w*0.1)
sanddollarImg = pygame.transform.scale(pygame.image.load("sanddollar.png"), (w*0.07, w*0.07))

shopButtonRect = pygame.Rect(w*0.02, w*0.02, w*0.12, w*0.12)
ogShopImg = pygame.image.load("shop.png")
shopImg = pygame.transform.scale(pygame.image.load("shop.png"), (w*0.08, w*0.08))

galleryButtonRect = pygame.Rect(w*0.16, w*0.02, w*0.12, w*0.12)
ogGalleryImg = pygame.image.load("gallery.png")
galleryImg = pygame.transform.scale(pygame.image.load("gallery.png"), (w*0.08, w*0.08))

beachButtonRect = pygame.Rect(w*0.02, w*0.86, w*0.12, w*0.12)
ogBeachImg = pygame.image.load("beach.png")
beachImg = pygame.transform.scale(pygame.image.load("beach.png"), (w*0.08, w*0.08))

# publish image yes no buttons
yesRect = pygame.Rect(0,0,w*0.3,w*0.1)
yesRect.centerx = w*0.3
yesRect.centery = w*0.7

noRect = pygame.Rect(0,0,w*0.3,w*0.1)
noRect.centerx = w*0.7
noRect.centery = w*0.7

# claim sand dollar
claimSanddollarRect = pygame.Rect(0,0,w*0.75,w*0.1)
claimSanddollarRect.centerx = w/2
claimSanddollarRect.centery = w*0.6

# gallery stuff
galleryBg = pygame.Rect(0,0,w*0.9,w*0.9)
galleryBg.center = (w/2,w/2)
popupExitRect = pygame.Rect(w*0.83, w*0.07, w*0.1, w*0.1)

galleryData = []
galleryBigRects = []
gallerySmallRects = []
galleryColors = []

chosen = 0

galleryPage = 0

FlipLeftRect = pygame.Rect(0,0,w*0.1,w*0.15)
FlipLeftRect.centerx = w*0.125
FlipLeftRect.centery = w*0.5

FlipRightRect = pygame.Rect(0,0,w*0.1,w*0.15)
FlipRightRect.centerx = w*0.875
FlipRightRect.centery = w*0.5

# beach stuff
beachBgImgs = [pygame.transform.scale(pygame.image.load("beachBg/1.png"), (w,w)), pygame.transform.scale(pygame.image.load("beachBg/2.png"), (w,w)), pygame.transform.scale(pygame.image.load("beachBg/3.png"), (w,w))]

beachConfirmButtonRect = pygame.Rect(w*0.45,w*0.88,w*0.1,w*0.1)
beachConfirmButtonImg = pygame.transform.scale(pygame.image.load("check.png"), (w*0.1,w*0.1))

beachExitRect = pygame.Rect(w*0.88, w*0.02, w*0.1, w*0.1)

addButtonRect = pygame.Rect(w*0.02, w*0.88, w*0.1, w*0.1)
trashButtonRect = pygame.Rect(w*0.14, w*0.88, w*0.1, w*0.1)

trashImgs = [pygame.transform.scale(pygame.image.load("close.png"), (w*0.08, w*0.08)), pygame.transform.scale(pygame.image.load("open.png"), (w*0.08, w*0.08))]

# add stuff
addBg = pygame.Rect(0,0,w*0.9,w*0.9)
addBg.center = (w/2,w/2)

# shop stuff

# shell, rock, pearl, fish, paraglider, woman, man, umbrella, chair, beach ball, beach towel, swim ring, sand castle, bucket and shovel
# 14 items total

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

offset = (0,0)

stage = "home"
username = "username"
password = "password"

hp = 100

offset = -500
acceleration = 1

down = False
solveDown = False

sanddollar = 1999

# CLEAR BUTTON: CLEAR ALL ITEMS ON THE BEACH TO RESTART

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if stage == "login":
            loginUsername.handle_event(event, username)
            loginPassword.handle_event(event, password)
            
        if stage == "signup":
            signupUsername.handle_event(event, username)
            signupPassword.handle_event(event, password)
    
    screen.fill((224, 232, 218))

    key = pygame.key.get_pressed()

    if stage == "index":
        pygame.draw.rect(screen, (171, 204, 157), loginRect, border_radius=20)

        if loginRect.collidepoint(pygame.mouse.get_pos()):
            text = pygame.font.SysFont("Comic Sans", 64).render("Log in", True, (66, 99, 52))
            textpos = text.get_rect(centerx=loginRect.centerx, centery=loginRect.centery)
            screen.blit(text, textpos)

            if pygame.mouse.get_pressed()[0] and not down:
                stage = "login"
        
        else:
            text = pygame.font.SysFont("Comic Sans", 56).render("Log in", True, (66, 99, 52))
            textpos = text.get_rect(centerx=loginRect.centerx, centery=loginRect.centery)
            screen.blit(text, textpos)
        
        pygame.draw.rect(screen, (66, 99, 52), signupRect, border_radius=20)
        
        if signupRect.collidepoint(pygame.mouse.get_pos()):
            text = pygame.font.SysFont("Comic Sans", 64).render("Sign up", True, (171, 204, 157))
            textpos = text.get_rect(centerx=signupRect.centerx, centery=signupRect.centery)
            screen.blit(text, textpos)

            if pygame.mouse.get_pressed()[0] and not down:
                stage = "signup"
        
        else:
            text = pygame.font.SysFont("Comic Sans", 56).render("Sign up", True, (171, 204, 157))
            textpos = text.get_rect(centerx=signupRect.centerx, centery=signupRect.centery)
            screen.blit(text, textpos)
    
    if stage == "login":
        text = pygame.font.SysFont("Comic Sans", 64).render("Log in", True, (66, 99, 52))
        textpos = text.get_rect(centerx=w/2, centery=w*0.2)
        screen.blit(text, textpos)

        text = pygame.font.SysFont("Comic Sans", 32).render("Username:", True, (108, 128, 99))
        textpos = text.get_rect(centerx=w/2, centery=w*0.42)
        screen.blit(text, textpos)

        text = pygame.font.SysFont("Comic Sans", 32).render("Password:", True, (108, 128, 99))
        textpos = text.get_rect(centerx=w/2, centery=w*0.62)
        screen.blit(text, textpos)

        if not validCredit:
            text = pygame.font.SysFont("Comic Sans", 16).render("*Invalid Credentials*", True, (235, 117, 117))
            textpos = text.get_rect(centerx=w/2, centery=w*0.3)
            screen.blit(text, textpos)

        for box in loginInputs:
            box.update()
        
        for box in loginInputs:
            box.draw(screen)
        
        if len(username) > 0 and len(password) > 0:
            validCredit = False

            f = open("save.txt", "r")
            r = f.read().splitlines()

            for i in range(len(r)):
                r[i] = r[i].split(",")
            
            for i in r:
                if i[0] == username[-1] and i[1] == password[-1]:
                    username = username[-1]
                    password = password[-1]
                    sanddollar = int(i[2])
                    f.close()
                    stage = "home"
                    validCredit = True
                    break
    
    if stage == "signup":
        text = pygame.font.SysFont("Comic Sans", 64).render("Sign up", True, (66, 99, 52))
        textpos = text.get_rect(centerx=w/2, centery=w*0.2)
        screen.blit(text, textpos)

        text = pygame.font.SysFont("Comic Sans", 32).render("Username:", True, (108, 128, 99))
        textpos = text.get_rect(centerx=w/2, centery=w*0.42)
        screen.blit(text, textpos)

        text = pygame.font.SysFont("Comic Sans", 32).render("Password:", True, (108, 128, 99))
        textpos = text.get_rect(centerx=w/2, centery=w*0.62)
        screen.blit(text, textpos)

        if not validCredit:
            text = pygame.font.SysFont("Comic Sans", 16).render("*Username already exists*", True, (235, 117, 117))
            textpos = text.get_rect(centerx=w/2, centery=w*0.3)
            screen.blit(text, textpos)

        for box in signupInputs:
            box.update()
        
        for box in signupInputs:
            box.draw(screen)
        
        if len(username) > 0 and len(password) > 0:
            validCredit = True

            f = open("save.txt", "r")
            r = f.read().splitlines()

            for i in range(len(r)):
                r[i] = r[i].split(",")
            
            for i in r:
                if i[0] == username[-1]:
                    validCredit = False
            
            if validCredit:
                username = username[-1]
                password = password[-1]
                sanddollar = 0
                stage = "home"

                f.close()
                f = open("save.txt", "a")
                f.write(f"\n{username},{password},0,,,,")

            f.close()

    if stage == "home":
        # money
        pygame.draw.rect(screen, (248, 250, 247), sanddollarRect, border_radius=20)
        screen.blit(sanddollarImg, (sanddollarRect.x+w*0.02, sanddollarRect.centery-w*0.035))

        sdShowTxt = str(sanddollar)
        if len(sdShowTxt) > 9:
            sdShowTxt = str(int(sanddollar/1000000))+"M"
        elif len(sdShowTxt) > 5:
            sdShowTxt = str(int(sanddollar/1000))+"K"

        text = pygame.font.SysFont("Comic Sans", 48).render(sdShowTxt, True, (66, 99, 52))
        textpos = text.get_rect(x=sanddollarRect.x+w*0.12, centery=sanddollarRect.centery-w*0.003)
        screen.blit(text, textpos)

        # shop
        pygame.draw.rect(screen, (248, 250, 247), shopButtonRect, border_radius=20)

        if shopButtonRect.collidepoint(pygame.mouse.get_pos()):
            shopImg = pygame.transform.scale(ogShopImg, (w*0.09, w*0.09))

            if pygame.mouse.get_pressed()[0]:
                stage = "shop"
                shopPage = 0
        else:
            shopImg = pygame.transform.scale(ogShopImg, (w*0.08, w*0.08))

        screen.blit(shopImg, (shopButtonRect.centerx - shopImg.get_size()[0]/2, shopButtonRect.centery-shopImg.get_size()[1]/2))
        
        # gallery
        pygame.draw.rect(screen, (248, 250, 247), galleryButtonRect, border_radius=20)

        if galleryButtonRect.collidepoint(pygame.mouse.get_pos()):
            galleryImg = pygame.transform.scale(ogGalleryImg, (w*0.09, w*0.09))

            if pygame.mouse.get_pressed()[0]:
                stage = "gallery setup"

        else:
            galleryImg = pygame.transform.scale(ogGalleryImg, (w*0.08, w*0.08))
        
        screen.blit(galleryImg, (galleryButtonRect.centerx - galleryImg.get_size()[0]/2, galleryButtonRect.centery-galleryImg.get_size()[1]/2))
        
        # beach
        pygame.draw.rect(screen, (248, 250, 247), beachButtonRect, border_radius=20)

        if beachButtonRect.collidepoint(pygame.mouse.get_pos()):
            beachImg = pygame.transform.scale(ogBeachImg, (w*0.09, w*0.09))

            if pygame.mouse.get_pressed()[0]:
                stage = "beach setup"
                down = True

        else:
            beachImg = pygame.transform.scale(ogBeachImg, (w*0.08, w*0.08))
        
        screen.blit(beachImg, (beachButtonRect.centerx - beachImg.get_size()[0]/2, beachButtonRect.centery-beachImg.get_size()[1]/2))

        # play button
        pygame.draw.rect(screen, (66, 99, 52), playRect, border_radius=20)

        if playRect.collidepoint(pygame.mouse.get_pos()):
            text = pygame.font.SysFont("Comic Sans", 72).render("Play", True, (171, 204, 157))
            textpos = text.get_rect(centerx=playRect.centerx, centery=playRect.centery)
            screen.blit(text, textpos)

            screen.blit(playBubble, (w*0.2, playRect.y - w*0.2))

            text = pygame.font.SysFont("Comic Sans", 24).render("Solve a pre-drawn nonogram", True, (51, 66, 44))
            textpos = text.get_rect(centerx=w/2, centery=playRect.y - w*0.15)
            screen.blit(text, textpos)

            text = pygame.font.SysFont("Comic Sans", 24).render("Earn sand dollars", True, (51, 66, 44))
            textpos = text.get_rect(centerx=w/2, centery=playRect.y - w*0.1)
            screen.blit(text, textpos)

            if pygame.mouse.get_pressed()[0] and not down:
                stage = "animation-for-solve get-from-gallery"

        else:
            text = pygame.font.SysFont("Comic Sans", 64).render("Play", True, (171, 204, 157))
            textpos = text.get_rect(centerx=playRect.centerx, centery=playRect.centery)
            screen.blit(text, textpos)

        # draw button
        pygame.draw.rect(screen, (171, 204, 157), drawRect, border_radius=20)

        if drawRect.collidepoint(pygame.mouse.get_pos()):
            text = pygame.font.SysFont("Comic Sans", 53).render("Draw", True, (66, 99, 52))
            textpos = text.get_rect(centerx=drawRect.centerx, centery=drawRect.centery)
            screen.blit(text, textpos)

            screen.blit(drawBubble, (w*0.2, drawRect.y + w*0.12))

            text = pygame.font.SysFont("Comic Sans", 24).render("Draw and solve your own nonogram", True, (51, 66, 44))
            textpos = text.get_rect(centerx=w/2, centery=drawRect.y + w*0.21)
            screen.blit(text, textpos)

            text = pygame.font.SysFont("Comic Sans", 24).render("Doesn't earn sand dollars", True, (51, 66, 44))
            textpos = text.get_rect(centerx=w/2, centery=drawRect.y + w*0.26)
            screen.blit(text, textpos)

            if pygame.mouse.get_pressed()[0] and not down:
                stage = "animation-for-draw"
        
        else:
            text = pygame.font.SysFont("Comic Sans", 48).render("Draw", True, (66, 99, 52))
            textpos = text.get_rect(centerx=drawRect.centerx, centery=drawRect.centery)
            screen.blit(text, textpos)

    if stage.split()[0] == "gallery":
        pygame.draw.rect(screen, (241, 245, 237), galleryBg, border_radius=10)

        if len(stage.split()) > 1 and stage.split()[1] == "setup":
            galleryData = [] # test if when it is here it works if not remove it pls
            galleryBigRects = []
            gallerySmallRects = []
            galleryColors = []

            savef = open("save.txt","r")
            galleryf = open("gallery.txt","r")

            saver = savef.read().splitlines()
            galleryr = galleryf.read().splitlines()
            
            for i in saver:
                i = i.split(",")
                if i[0] == username:
                    galleryData = i[3].split("-")
                    break

            if galleryData != [""]:
                for i in range(len(galleryData)):
                    galleryData[i] = int(galleryData[i])
                
                f = open("gallery.txt","r")
                r = f.read().splitlines()

                data = ""
                for i in range(len(galleryData)):
                    galleryBigRects.append(pygame.Rect(w*0.2+((i%4)%2 * w*0.35), w*0.2+((i%4)//2 * w*0.35), w*0.25, w*0.25))

                    data = r[galleryData[i]].split(" ")
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
                text = pygame.font.SysFont("Comic Sans", 96).render("<", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    galleryPage -= 1
            else:
                text = pygame.font.SysFont("Comic Sans", 64).render("<", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                screen.blit(text, textpos)

        if galleryPage < (len(galleryBigRects)-1)//4:
            pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

            if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.SysFont("Comic Sans", 96).render(">", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    galleryPage += 1
            else:
                text = pygame.font.SysFont("Comic Sans", 64).render(">", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                screen.blit(text, textpos)

        if key[pygame.K_LEFT] and galleryPage > 0 and not down:
            galleryPage -= 1
        if key[pygame.K_RIGHT] and galleryPage < (len(galleryBigRects)-1)//4 and not down:
            galleryPage += 1

        if popupExitRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (222, 130, 126), popupExitRect, border_radius=20)
            text = pygame.font.SysFont("Comic Sans", 64).render("X", True, (255,255,255))
            textpos = text.get_rect(centerx=popupExitRect.centerx, centery=popupExitRect.centery)
            screen.blit(text, textpos)
            
            if pygame.mouse.get_pressed()[0]:
                stage = "home"

        else:
            pygame.draw.rect(screen, (222, 130, 126), popupExitRect, border_radius=20)
            text = pygame.font.SysFont("Comic Sans", 48).render("X", True, (255,255,255))
            textpos = text.get_rect(centerx=popupExitRect.centerx, centery=popupExitRect.centery)
            screen.blit(text, textpos)

    if stage == "shop":
        pygame.draw.rect(screen, (249, 250, 242), shopBg, border_radius=10)

        for i in range(shopPage*4,shopPage*4+4):
            if len(shopItemRects) > i:
                pygame.draw.rect(screen, (204, 209, 171), shopItemRects[i], border_radius=10)

                if shopItemRects[i].collidepoint(pygame.mouse.get_pos()):
                    shopItemImgs[i] = pygame.transform.scale(ogShopItemImgs[i], (w*0.2, w*0.2))
                    screen.blit(shopItemImgs[i], (shopItemRects[i].centerx - w*0.1, shopItemRects[i].centery - w*0.15))

                    if pygame.mouse.get_pressed()[0] and not down:
                        if sanddollar >= shopItemPrice[i]:
                            f = open("save.txt","r")
                            r = f.read().splitlines()
                            f.close()

                            for j in range(len(r)):
                                r[j] = r[j].split(",")
                                if r[j][0] == username:
                                    r[j][6] = r[j][6].split(" ")
                                    r[j][6].append(str(i))

                                    r[j][6] = " ".join(r[j][6])
                                    r[j][6] = r[j][6].strip(" ")
                                r[j] = ",".join(r[j])

                            r = "\n".join(r)

                            f = open("save.txt", "w")
                            f.write(r)
                            f.close()

                            sanddollar -= shopItemPrice[i]

                            f = open("save.txt", "r")
                            r = f.read().splitlines()
                            f.close()

                            for i in range(len(r)):
                                r[i] = r[i].split(",")
                                if r[i][0] == username:
                                    r[i][2] = str(sanddollar)
                                r[i] = ",".join(r[i])

                            r = "\n".join(r)
                            
                            f = open("save.txt", "w")
                            f.write(r)
                            f.close()
                
                else:
                    shopItemImgs[i] = pygame.transform.scale(ogShopItemImgs[i], (w*0.18, w*0.18))
                    screen.blit(shopItemImgs[i], (shopItemRects[i].centerx - w*0.09, shopItemRects[i].centery - w*0.14))

                text = pygame.font.SysFont("Comic Sans", 48).render("$"+str(shopItemPrice[i]), True, (80, 82, 66))
                textpos = text.get_rect(centerx=shopItemRects[i].centerx, centery=shopItemRects[i].centery + w*0.1)
                screen.blit(text, textpos)
        
        if shopPage > 0:
            pygame.draw.rect(screen, (91, 107, 79), FlipLeftRect, border_radius=20)

            if FlipLeftRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.SysFont("Comic Sans", 96).render("<", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    shopPage -= 1
            else:
                text = pygame.font.SysFont("Comic Sans", 64).render("<", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                screen.blit(text, textpos)

        if shopPage < (len(shopItemRects)-1)//4:
            pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

            if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.SysFont("Comic Sans", 96).render(">", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    shopPage += 1
            else:
                text = pygame.font.SysFont("Comic Sans", 64).render(">", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                screen.blit(text, textpos)

        if key[pygame.K_LEFT] and shopPage > 0 and not down:
            shopPage -= 1
        if key[pygame.K_RIGHT] and shopPage < (len(shopItemRects)-1)//4 and not down:
            shopPage += 1

        if popupExitRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (222, 130, 126), popupExitRect, border_radius=20)
            text = pygame.font.SysFont("Comic Sans", 64).render("X", True, (255,255,255))
            textpos = text.get_rect(centerx=popupExitRect.centerx, centery=popupExitRect.centery)
            screen.blit(text, textpos)
            
            if pygame.mouse.get_pressed()[0]:
                stage = "home"

        else:
            pygame.draw.rect(screen, (222, 130, 126), popupExitRect, border_radius=20)
            text = pygame.font.SysFont("Comic Sans", 48).render("X", True, (255,255,255))
            textpos = text.get_rect(centerx=popupExitRect.centerx, centery=popupExitRect.centery)
            screen.blit(text, textpos)

    if stage == "pick-beach":
        screen.blit(beachBgImgs[beachBgNo], (0,0))

        if key[pygame.K_LEFT] and not down:
            beachBgNo -= 1
        if key[pygame.K_RIGHT] and not down:
            beachBgNo += 1
        
        pygame.draw.rect(screen, (91, 107, 79), FlipLeftRect, border_radius=20)

        if FlipLeftRect.collidepoint(pygame.mouse.get_pos()):
            text = pygame.font.SysFont("Comic Sans", 96).render("<", True, (255,255,255))
            textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
            screen.blit(text, textpos)

            if pygame.mouse.get_pressed()[0] and not down:
                beachBgNo -= 1
        else:
            text = pygame.font.SysFont("Comic Sans", 64).render("<", True, (255,255,255))
            textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
            screen.blit(text, textpos)

        pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

        if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
            text = pygame.font.SysFont("Comic Sans", 96).render(">", True, (255,255,255))
            textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
            screen.blit(text, textpos)

            if pygame.mouse.get_pressed()[0] and not down:
                beachBgNo += 1
        else:
            text = pygame.font.SysFont("Comic Sans", 64).render(">", True, (255,255,255))
            textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
            screen.blit(text, textpos)
        
        beachBgNo = beachBgNo % 3

        screen.blit(beachConfirmButtonImg, (w*0.45,w*0.88))

        if beachConfirmButtonRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            stage = "beach setup"

            f = open("save.txt", "r")
            r = f.read().splitlines()

            for i in range(len(r)):
                if username in r[i]:
                    r[i] = r[i].split(",")
                    r[i][4] = str(beachBgNo)

                    r[i] = ",".join(r[i])

            r = "\n".join(r)
            f.close()

            f = open("save.txt", "w")
            f.write(r)
            f.close()

    if stage.split()[0] == "beach":
        if len(stage.split()) > 1 and stage.split()[1] == "setup":
            f = open("save.txt","r")
            r = f.read().splitlines()
            beachBgNo = 0
            beachData = ""

            for i in r:
                i = i.split(",")
                if i[0] == username:
                    beachBgNo = i[4]
                    beachData = i[5]
                    break
            
            f.close()

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
                
                beachData[i][1][0] = int(beachData[i][1][0])
                beachData[i][1][1] = int(beachData[i][1][1])

                shopItemImgs[beachData[i][0]] = pygame.transform.scale(ogShopItemImgs[beachData[i][0]], (w*0.2,w*0.2))

                beachItemRects.append(pygame.Rect(beachData[i][1][0], beachData[i][1][1], w*0.2, w*0.2))
            
            stage = "beach"

            moveItem = []

        screen.blit(beachBgImgs[beachBgNo], (0,0))

        if not down:
            moveItem = []

        for i in range(len(beachData)):
            screen.blit(shopItemImgs[beachData[i][0]], (beachData[i][1][0], beachData[i][1][1]))
            if beachItemRects[i].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not down:
                moveItem.append(i)
                offset = (pygame.mouse.get_pos()[0]-beachData[moveItem[-1]][1][0], pygame.mouse.get_pos()[1]-beachData[moveItem[-1]][1][1])
        
        if moveItem != []:
            beachData[moveItem[-1]][1][0] = pygame.mouse.get_pos()[0] - offset[0]
            beachData[moveItem[-1]][1][1] = pygame.mouse.get_pos()[1] - offset[1]

            f = open("save.txt", "r")
            r = f.read().splitlines()
            f.close()

            for i in range(len(r)):
                r[i] = r[i].split(",")
                
                if r[i][0] == username:
                    r[i][5] = r[i][5].split()
                    r[i][5][moveItem[-1]] = f"{beachData[moveItem[-1]][0]}/{beachData[moveItem[-1]][1][0]}-{beachData[moveItem[-1]][1][1]}"

                    r[i][5] = " ".join(r[i][5])
                
                r[i] = ",".join(r[i])
            
            r = "\n".join(r)

            f = open("save.txt","w")
            f.write(r)
            f.close()

            beachItemRects[moveItem[-1]].x = pygame.mouse.get_pos()[0] - offset[0]
            beachItemRects[moveItem[-1]].y = pygame.mouse.get_pos()[1] - offset[1]
        
        pygame.draw.rect(screen, (126, 166, 119), addButtonRect, border_radius=20)

        if addButtonRect.collidepoint(pygame.mouse.get_pos()) and not down:
            text = pygame.font.SysFont("Comic Sans", 96).render("+", True, (255,255,255))
            textpos = text.get_rect(centerx=addButtonRect.centerx, centery=addButtonRect.centery-w*0.01)
            screen.blit(text, textpos)
            
            if pygame.mouse.get_pressed()[0]:
                stage = "add setup"

        else:
            text = pygame.font.SysFont("Comic Sans", 64).render("+", True, (255,255,255))
            textpos = text.get_rect(centerx=addButtonRect.centerx, centery=addButtonRect.centery-w*0.01)
            screen.blit(text, textpos)
        
        pygame.draw.rect(screen, (173, 78, 78), trashButtonRect, border_radius=20)

        if trashButtonRect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(trashImgs[1], (trashButtonRect.x+w*0.01, trashButtonRect.y+w*0.01))

            if moveItem != [] and not pygame.mouse.get_pressed()[0]:
                stage = "beach setup"

                f = open("save.txt", "r")
                r = f.read().splitlines()
                f.close()

                for i in range(len(r)):
                    r[i] = r[i].split(",")
                    if r[i][0] == username:
                        r[i][5] = r[i][5].split()
                        r[i][5].pop(moveItem[-1])
                        r[i][5] = " ".join(r[i][5])

                        r[i][6] = r[i][6].split()
                        r[i][6].append(str(beachData[moveItem[-1]][0]))
                        r[i][6] = " ".join(r[i][6])

                    r[i] = ",".join(r[i])
                
                r = "\n".join(r)

                f = open("save.txt", "w")
                f.write(r)
                f.close()

        else:
            screen.blit(trashImgs[0], (trashButtonRect.x+w*0.01, trashButtonRect.y+w*0.01))

        pygame.draw.rect(screen, (222, 130, 126), beachExitRect, border_radius=20)

        if beachExitRect.collidepoint(pygame.mouse.get_pos()) and not down:
            text = pygame.font.SysFont("Comic Sans", 64).render("X", True, (255,255,255))
            textpos = text.get_rect(centerx=beachExitRect.centerx, centery=beachExitRect.centery)
            screen.blit(text, textpos)
            
            if pygame.mouse.get_pressed()[0]:
                stage = "home"

        else:
            text = pygame.font.SysFont("Comic Sans", 48).render("X", True, (255,255,255))
            textpos = text.get_rect(centerx=beachExitRect.centerx, centery=beachExitRect.centery)
            screen.blit(text, textpos)

    if stage.split()[0] == "add":
        pygame.draw.rect(screen, (241, 245, 237), addBg, border_radius=10)

        if len(stage.split()) > 1 and stage.split()[1] == "setup":
            stage = "add"

            addPage = 0
            
            f = open("save.txt", "r")
            r = f.read().splitlines()
            f.close()

            addData = ""

            for i in r:
                i = i.split(",")
                if i[0] == username:
                    addData = i[6]
                    break
            
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

                        f = open("save.txt", "r")
                        r = f.read().splitlines()
                        f.close()

                        for j in range(len(r)):
                            r[j] = r[j].split(",")
                            if r[j][0] == username:
                                r[j][5] = r[j][5].split()
                                r[j][6] = r[j][6].split()

                                r[j][6].remove(str(addData[i]))
                                r[j][5].append(f"{str(addData[i])}/{int(random.randint(int(w/4), int(w/4)*3))}-{int(random.randint(int(w/4), int(w/4)*3))}")

                                r[j][5] = " ".join(r[j][5])
                                r[j][6] = " ".join(r[j][6])
                            
                            r[j] = ",".join(r[j])
                        
                        r = "\n".join(r)

                        f = open("save.txt", "w")
                        f.write(r)
                        f.close()
                
                else:
                    shopItemImgs[addData[i]] = pygame.transform.scale(ogShopItemImgs[addData[i]], (w*0.15, w*0.15))
                    screen.blit(shopItemImgs[addData[i]], (addItemRects[i].centerx-w*0.075, addItemRects[i].centery-w*0.075))
        
        if addPage > 0:
            pygame.draw.rect(screen, (91, 107, 79), FlipLeftRect, border_radius=20)

            if FlipLeftRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.SysFont("Comic Sans", 96).render("<", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    addPage -= 1
            else:
                text = pygame.font.SysFont("Comic Sans", 64).render("<", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipLeftRect.centerx, centery=FlipLeftRect.centery)
                screen.blit(text, textpos)

        if addPage < (len(addData)-1)//9:
            pygame.draw.rect(screen, (91, 107, 79), FlipRightRect, border_radius=20)

            if FlipRightRect.collidepoint(pygame.mouse.get_pos()):
                text = pygame.font.SysFont("Comic Sans", 96).render(">", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                screen.blit(text, textpos)

                if pygame.mouse.get_pressed()[0] and not down:
                    addPage += 1
            else:
                text = pygame.font.SysFont("Comic Sans", 64).render(">", True, (255,255,255))
                textpos = text.get_rect(centerx=FlipRightRect.centerx, centery=FlipRightRect.centery)
                screen.blit(text, textpos)

        if key[pygame.K_LEFT] and addPage > 0 and not down:
            addPage -= 1
        if key[pygame.K_RIGHT] and addPage < (len(shopItemRects)-1)//9 and not down:
            addPage += 1

        if popupExitRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (222, 130, 126), popupExitRect, border_radius=20)
            text = pygame.font.SysFont("Comic Sans", 64).render("X", True, (255,255,255))
            textpos = text.get_rect(centerx=popupExitRect.centerx, centery=popupExitRect.centery)
            screen.blit(text, textpos)
            
            if pygame.mouse.get_pressed()[0]:
                stage = "beach setup"

        else:
            pygame.draw.rect(screen, (222, 130, 126), popupExitRect, border_radius=20)
            text = pygame.font.SysFont("Comic Sans", 48).render("X", True, (255,255,255))
            textpos = text.get_rect(centerx=popupExitRect.centerx, centery=popupExitRect.centery)
            screen.blit(text, textpos)

    if stage == "animation-for-draw":
        drawBoard(size, screen, colors, boardSolution, gap, w, cellW)
        
        screen.blit(checkButtonImg, (gap*0.1,gap*0.1))

        screen.blit(fade, (0,0))

        text = pygame.font.SysFont("Comic Sans", 96).render("Draw your Nonogram!", True, (255,255,255))
        textpos = text.get_rect(centerx=w/2-offset, centery=w*0.4)
        screen.blit(text, textpos)

        text = pygame.font.SysFont("Comic Sans", 48).render("Have a friend draw it for a challenge", True, (255,255,255))
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
    
    if stage == "fade-for-draw":
        drawBoard(size, screen, colors, boardSolution, gap, w, cellW)
        
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
    
    if stage == "draw":
        # draw the board
        drawBoard(size, screen, colors, boardSolution, gap, w, cellW)
        
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
    
    if stage.split()[0] == "animation-for-solve":
        if len(stage.split()) > 1 and stage.split()[1] == "get-from-gallery":
            f = open("gallery.txt", "r")
            r = f.read().splitlines()
            chosen = random.randint(0,len(r)-1)
            r = r[chosen]
            f.close()

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

            stage = "animation-for-solve earn-sanddollar"

        drawBoard(size, screen, colors, boardSolving, gap, w, cellW)

        # draw background for info
        for y in yinfoRects:
            pygame.draw.rect(screen, (52, 74, 36), y, border_top_left_radius=10, border_bottom_left_radius=10)
        
        for x in xinfoRects:
            pygame.draw.rect(screen, (52, 74, 36), x, border_top_left_radius=10, border_top_right_radius=10)
        
        # draw info
        for y in range(size):
            text = pygame.font.SysFont("Comic Sans", 24).render(" ".join(yinfo[y]), True, (255,255,255))
            textpos = text.get_rect(centerx=yinfoRects[y].centerx, centery=yinfoRects[y].centery)
            screen.blit(text, textpos)
        
        for x in range(size):
            for i in range(len(xinfo[x])):
                text = pygame.font.SysFont("Comic Sans", 24).render((xinfo[x][i]), True, (255,255,255))
                textpos = text.get_rect(centerx=xinfoRects[x].centerx, y=xinfoRects[x].y + xinfoRects[x].h*i/len(xinfo[x]))
                screen.blit(text, textpos)

        screen.blit(fade, (0,0))

        text = pygame.font.SysFont("Comic Sans", 96).render("Solve!", True, (255,255,255))
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
            if len(stage.split()) > 1 and stage.split()[1] == "earn-sanddollar":
                stage = "fade-for-solve earn-sanddollar"
            else:
                stage = "fade-for-solve"
            acceleration = 1
    
    if stage.split()[0] == "fade-for-solve":
        drawBoard(size, screen, colors, boardSolving, gap, w, cellW)

        # draw background for info
        for y in yinfoRects:
            pygame.draw.rect(screen, (52, 74, 36), y, border_top_left_radius=10, border_bottom_left_radius=10)
        
        for x in xinfoRects:
            pygame.draw.rect(screen, (52, 74, 36), x, border_top_left_radius=10, border_top_right_radius=10)
        
        # draw info
        for y in range(size):
            text = pygame.font.SysFont("Comic Sans", 24).render(" ".join(yinfo[y]), True, (255,255,255))
            textpos = text.get_rect(centerx=yinfoRects[y].centerx, centery=yinfoRects[y].centery)
            screen.blit(text, textpos)
        
        for x in range(size):
            for i in range(len(xinfo[x])):
                text = pygame.font.SysFont("Comic Sans", 24).render((xinfo[x][i]), True, (255,255,255))
                textpos = text.get_rect(centerx=xinfoRects[x].centerx, y=xinfoRects[x].y + xinfoRects[x].h*i/len(xinfo[x]))
                screen.blit(text, textpos)

        fade.fill((0, 0, 0, fadeo))
        screen.blit(fade, (0,0))
        fadeo -= acceleration
        acceleration += 0.5

        if fadeo <= 0:
            if len(stage.split()) > 1 and stage.split()[1] == "earn-sanddollar":
                stage = "solve earn-sanddollar"
            else:
                stage = "solve"
    
    if stage.split()[0] == "solve":
        drawBoard(size, screen, colors, boardSolving, gap, w, cellW)

        # draw background for info
        for y in yinfoRects:
            pygame.draw.rect(screen, (52, 74, 36), y, border_top_left_radius=10, border_bottom_left_radius=10)
        
        for x in xinfoRects:
            pygame.draw.rect(screen, (52, 74, 36), x, border_top_left_radius=10, border_top_right_radius=10)
        
        # draw info
        for y in range(size):
            text = pygame.font.SysFont("Comic Sans", 24).render(" ".join(yinfo[y]), True, (255,255,255))
            textpos = text.get_rect(centerx=yinfoRects[y].centerx, centery=yinfoRects[y].centery)
            screen.blit(text, textpos)
        
        for x in range(size):
            for i in range(len(xinfo[x])):
                text = pygame.font.SysFont("Comic Sans", 24).render((xinfo[x][i]), True, (255,255,255))
                textpos = text.get_rect(centerx=xinfoRects[x].centerx, y=xinfoRects[x].y + xinfoRects[x].h*i/len(xinfo[x]))
                screen.blit(text, textpos)
        
        # check for fill
        for y in range(size):
            for x in range(size):
                if boardRects[y][x].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and (boardSolving[y][x] == 0 or boardSolving[y][x] == 3) and not solveDown:
                    if boardSolution[y][x] == 1:
                        boardSolving[y][x] = 1
                    else:
                        boardSolving[y][x] = 3
                        hp -= 8
                        solveDown = True

                if boardRects[y][x].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[2] and (boardSolving[y][x] == 0 or boardSolving[y][x] == 3) and not solveDown:
                    if boardSolution[y][x] == 0:
                        boardSolving[y][x] = 2
                    else:
                        boardSolving[y][x] = 3
                        hp -= 8
                        solveDown = True
        
        screen.blit(heartImg, (0,0))

        text = pygame.font.SysFont("Comic Sans", 32).render(str(hp)+"%", True, (250, 215, 231))
        textpos = text.get_rect(centerx=gap/2, centery=gap/5*2)
        screen.blit(text, textpos)

        won = True
        for y in range(size):
            for x in range(size):
                if not (boardSolving[y][x] == boardSolution[y][x] or (boardSolving[y][x] == 2 and boardSolution[y][x] == 0)):
                    won = False
        
        if won:
            if len(stage.split()) > 1 and stage.split()[1] == "earn-sanddollar":
                stage = "win earn-sanddollar"
            else:
                stage = "win"
        
        if hp <= 0:
            if len(stage.split()) > 1 and stage.split()[1] == "earn-sanddollar":
                stage = "lose earn-sanddollar"
            else:
                stage = "lose"
    
    if stage.split()[0] == "win" or stage.split()[0] == "lose":
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
            text = pygame.font.SysFont("Comic Sans", 128).render("YOU WIN!", True, (211, 232, 179))
            earndollar = 100
        elif stage.split()[0] == "lose":
            text = pygame.font.SysFont("Comic Sans", 128).render("YOU LOSE!", True, (232, 195, 195))
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
                text = pygame.font.SysFont("Comic Sans", 48).render(f"Claim sand dollar {earndollar}x", True, (52, 64, 36))
                textpos = text.get_rect(centerx=claimSanddollarRect.centerx, centery=claimSanddollarRect.centery)
                screen.blit(text, textpos)

                if claimSanddollarRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    sanddollar += earndollar
                    f = open("save.txt", "r")
                    r = f.read().splitlines()
                    f.close()

                    for i in range(len(r)):
                        r[i] = r[i].split(",")
                        if r[i][0] == username:
                            r[i][2] = str(sanddollar)
                        r[i] = ",".join(r[i])
                    r = "\n".join(r)
                    
                    f = open("save.txt", "w")
                    f.write(r)
                    f.close()

                    stage = "reset"

                    if stage.split()[0] == "win":
                        f = open("save.txt", "r")
                        r = f.read().splitlines()

                        for i in range(len(r)):
                            if username in r[i]:
                                r[i] = r[i].split(",")
                                r[i][2] = str(sanddollar)

                                r[i][3] = r[i][3].split("-")
                                r[i][3].append(str(chosen))
                                r[i][3] = "-".join(r[i][3])

                                r[i] = ",".join(r[i])

                        r = "\n".join(r)
                        f.close()

                        f = open("save.txt", "w")
                        f.write(r)
                        f.close()

            else:
                text = pygame.font.SysFont("Comic Sans", 64).render("Publish image?", True, (157, 166, 144))
                textpos = text.get_rect(centerx=w/2, centery=w*0.55)
                screen.blit(text, textpos)

                pygame.draw.rect(screen, (158, 189, 115), yesRect, border_radius=20)
                text = pygame.font.SysFont("Comic Sans", 48).render("Yes", True, (52, 64, 36))
                textpos = text.get_rect(centerx=yesRect.centerx, centery=yesRect.centery)
                screen.blit(text, textpos)

                pygame.draw.rect(screen, (189, 117, 115), noRect, border_radius=20)
                text = pygame.font.SysFont("Comic Sans", 48).render("No", True, (52, 64, 36))
                textpos = text.get_rect(centerx=noRect.centerx, centery=noRect.centery)
                screen.blit(text, textpos)

                if yesRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    f = open("gallery.txt", 'a')
                    r = str(size)+" "
                    for y in boardSolution:
                        for x in y:
                            r += str(x)
                    f.write("\n"+r)
                    f.close()

                    stage = "reset"
                
                if noRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    stage = "reset"

    if stage == "reset":
        size = 15 # pixels for the drawing width and height
        boardSolution = [] # answer
        for y in range(size):
            boardSolution.append([])
            for x in range(size):
                boardSolution[-1].append(0)

        boardSolving = [] # the current stage of the board while solving
        for y in range(size):
            boardSolving.append([])
            for x in range(size):
                boardSolving[-1].append(0)

        gap = w*0.122
        cellW = math.floor((w-gap)/size) # gap of 3 on top and left for numbers

        boardRects = []
        for y in range(size):
            boardRects.append([])
            for x in range(size):
                boardRects[-1].append(pygame.Rect(x*cellW + gap, y*cellW + gap, cellW, cellW))

        colors = ((185, 191, 153), (75, 83, 32), (255, 255, 255), (252, 93, 93)) # filled and not filled nonogram colors

        checkButtonRect = pygame.Rect(gap*0.1, gap*0.1, gap*0.8, gap*0.8)
        checkButtonImg = pygame.transform.scale(pygame.image.load("check.png"), (gap*0.8, gap*0.8))

        heartImg = pygame.transform.scale(pygame.image.load("heart.png"), (gap, gap))

        # info for the sides
        yinfo = []
        xinfo = []

        yinfoRects = []
        for y in range(size):
            yinfoRects.append(pygame.Rect(0, gap+cellW*y+3, gap, cellW-6))

        xinfoRects = []
        for x in range(size):
            xinfoRects.append(pygame.Rect(gap+cellW*x+3, 0, cellW-6, gap))

        # for win and loose and animation word screen
        darken = pygame.Surface((w,w), pygame.SRCALPHA)
        darken.fill((0, 0, 0, 0))
        opacity = 0

        # for fade in and out of the darken
        fade = pygame.Surface((w,w), pygame.SRCALPHA)
        fade.fill((0, 0, 0, 127))
        fadeo = 127

        validCredit = True

        chosen = 0

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
