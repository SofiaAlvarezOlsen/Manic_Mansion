import pygame as pg
import sys
import time
import random as rd

# Konstanter
WIDTH = 500  # Bredden til vinduet
HEIGHT = 400 # Høyden til vinduet

FREEZONE_WIDTH = 100 # Bredden til frisonen

# Størrelsen til vinduet
SIZE = (WIDTH, HEIGHT)

# Frames Per Second (bilder per sekund)
FPS = 120

# Farger (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (100, 200, 90)
GREY = (142, 142, 142)
BLUE = (0, 0, 255)

# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()

# Tittel
pg.display.set_caption("Manic Mansion")

# Henter font
font = pg.font.SysFont("Arial", 20)





# Funksjon som sjekker om lokasjonen er opptatt
def isLocationOccupied(x, y):
    for i in range(len(gameboard.objects)):
        old_x = gameboard.objects[i].xPosition
        old_y = gameboard.objects[i].yPosition
        if old_x <= x <= old_x+gameobject.size or old_x <= x+gameobject.size <= old_x+gameobject.size:
            if old_y <= y <= old_y+gameobject.size or old_y <= y+gameobject.size <= old_y+gameobject.size:
                return True
    return False

# Viser poeng
def showPoints():
    text_img = font.render(f"Antall poeng: {person.points}", True, BLUE)
    surface.blit(text_img, (10,10))





# Klasse for spill
class GameObject:
    def __init__(self):
        self.xPosition = 0
        self.yPosition = 0
        
        # Legger til egenskapen "størrelse" fordi alle objektene har samme størrelse
        self.size = 20
    def placement(self, start_x, stop_x):
        
        x = rd.randint(start_x,stop_x)
        y = rd.randint(0,WIDTH-FREEZONE_WIDTH-self.size)
        
        while isLocationOccupied(x, y) == True:
            x = rd.randint(start_x,stop_x)
            y = rd.randint(0,WIDTH-FREEZONE_WIDTH-self.size)
    
        # Setter posisjonen
        self.xPosition = x
        self.yPosition = y
        
    """
    Bruker ikke "flytt" metoden fordi alle objektene flytter seg på veldig ulike måter:
        - Person: flyttes med piltaster
        - Spøkelse: flyttes med retningsvektor
        - Hindring: flyttes ikke
        - Sau: "festes" til personen
    Jeg ser fortsatt fordelen fordi objektorientert orientering handler om å sortere så det blir lett å finne frem.
    Selve det at objektene flyttes er ganske felles for objektene. 
    """


# Klasse for person
class Person(GameObject):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.points = 0
        self.carryingSheep = False
        
        # La til en egenskap som gir personen en egen farge
        self.color = RED
 
    def placement(self):
        start_x = 0
        stop_x = FREEZONE_WIDTH-self.size
        
        super().placement(start_x,stop_x)
        
    def move(self):
        # Henter knappene fra tastaturet som trykkes på
        keys = pg.key.get_pressed()
        
        # Sjekker om piltasten opp trykkes på
        if keys[pg.K_UP]:
            # Hvis personen ikke kolliderer med en hindring vil berøring av piltast flytte personen
            if not self.isCollisionWithHinderance(self.xPosition, self.yPosition-self.speed):
                self.yPosition -= self.speed
            
        # Sjekker om piltasten ned trykkes på
        if keys[pg.K_DOWN]:
            if not self.isCollisionWithHinderance(self.xPosition, self.yPosition+self.speed):
                self.yPosition += self.speed
            
        # Sjekker om piltasten til venstre trykkes på
        if keys[pg.K_RIGHT]:
            if not self.isCollisionWithHinderance(self.xPosition+self.speed, self.yPosition):
                self.xPosition += self.speed
        
        # Sjekker om piltasten til høyre trykkes på
        if keys[pg.K_LEFT]:
            if not self.isCollisionWithHinderance(self.xPosition-self.speed, self.yPosition):
                self.xPosition -= self.speed
                  
    def increasePoints(self):
        self.points += 1  
        
    # La til en metode som legger fra seg sauen
    def releaseSheep(self):
        self.carryingSheep = False
        self.speed = 2
    
    # La inn redusering av fart inni metode som bærer sauen
    def carrySheep(self, sheep):
        self.carryingSheep = True
        sheep.setGettingPickedUpTrue()
        self.speed = 1
    
    # La til en egen metode som sjekker at det skjer en kollisjon med en hindring (den kalles på i move-meoden)
    def isCollisionWithHinderance(self, x, y):
        for i in range(len(obstacles)):
            obstacle_x = obstacles[i].xPosition
            obstacle_y = obstacles[i].yPosition
            if obstacle_x <= x <= obstacle_x+self.size or obstacle_x <= x+self.size <= obstacle_x+self.size:
                if obstacle_y <= y <= obstacle_y+self.size or obstacle_y <= y+self.size <= obstacle_y+self.size:
                    return True

    def checkCollision(self):   
        # Sjekker kollisjon med høyre vegg
        if self.xPosition + self.size >= WIDTH:
            self.xPosition = WIDTH - self.size
            
        # Sjekker kollisjon med venstre vegg
        if self.xPosition <= 0:
            self.xPosition = 0
        
        # Sjekker kollisjon med topp
        if self.yPosition <= 0:
            self.yPosition = 0
            
        # Sjekker kollisjon med bunn
        if self.yPosition + self.size >= HEIGHT:
            self.yPosition = HEIGHT - self.size
        
        # Sjekker om personen kolliderer med startsonen
        if self.xPosition < FREEZONE_WIDTH and self.carryingSheep == True:
            self.releaseSheep()
            self.increasePoints()
            for sheep in sheeps:
                if sheep.xPosition <= FREEZONE_WIDTH:
                    sheep.removeSheep(sheep)
            placeNewSheepOnBoard()
            placeNewGhostOnBoard()
            placeNewObstacleOnBoard()
            
        # Sjekker kollisjon med sau
        for i in range(len(sheeps)):
            sheep_x = sheeps[i].xPosition
            sheep_y = sheeps[i].yPosition
            if sheep_x <= self.xPosition <= sheep_x+self.size or sheep_x <= self.xPosition+self.size <= sheep_x+self.size:
                if sheep_y <= self.yPosition <= sheep_y+self.size or sheep_y <= self.yPosition+self.size <= sheep_y+self.size:
                    # Dersom person allerede bærer en sau og kolliderer med en annen sau som ikke allerede bæres
                    if self.carryingSheep == True and sheeps[i].isBeingCarried() == False:
                        endGame()
                    self.carrySheep(sheeps[i])
        
        # Sjekker kollisjon med spøkelse
        for i in range(len(ghosts)):
            ghost_x = ghosts[i].xPosition
            ghost_y = ghosts[i].yPosition
            if ghost_x <= self.xPosition <= ghost_x+self.size or ghost_x <= self.xPosition+self.size <= ghost_x+self.size:
                if ghost_y <= self.yPosition <= ghost_y+self.size or ghost_y <= self.yPosition+self.size <= ghost_y+self.size:
                    endGame()
            
    
# Klasse for spøkelse
class Ghost(GameObject):
    def __init__(self):
        super().__init__()
        # La til egenskap for fargen på spøkelse
        self.color = GREY
        
        # La til egenskaper for tilfeldig retningsfart
        self.vx = rd.uniform(-1, 1)
        self.vy = rd.uniform(-1, 1)
        
    def placement(self):
        start_x = FREEZONE_WIDTH
        stop_x = WIDTH-FREEZONE_WIDTH-self.size
        
        super().placement(start_x,stop_x)
    
    # Bestemmer både bevegelse og retning i en move-metode
    def move(self):
        # Oppdaterer posisjonen fra farten
        self.xPosition += self.vx
        self.yPosition += self.vy
        
        # Sjekker kollisjon med høyre vegg
        if self.xPosition + self.size >= WIDTH-FREEZONE_WIDTH:
            self.vx *= -1
            self.xPosition = WIDTH-FREEZONE_WIDTH - self.size
            
        # Sjekker kollisjon med venstre vegg
        if self.xPosition <= FREEZONE_WIDTH:
            self.vx *= -1
            self.xPosition = FREEZONE_WIDTH
        
        # Sjekker kollisjon med topp
        if self.yPosition <= 0:
            self.vy *= -1
            self.yPosition = 0
            
        # Sjekker kollisjon med bunn
        if self.yPosition + self.size >= HEIGHT:
            self.vy *= -1
            self.yPosition = HEIGHT - self.size
 
    

# Klasse for obstacle
class Obstacle(GameObject):
    def __init__(self):
        super().__init__()
        # La til egenskap for fargen på hindringen
        self.color = BLACK
    
    def placement(self):
        start_x = FREEZONE_WIDTH
        stop_x = WIDTH-FREEZONE_WIDTH-self.size
        
        super().placement(start_x,stop_x)
        
        
# Klasse for sau
class Sheep(GameObject):
    def __init__(self):
        super().__init__()
        self.beingCarried = False
        
        # La til egenskap for fargen på spøkelse
        self.color = WHITE
        
    # La til metode som sender beskjed om sauen blir bært eller ikke (mer objektorientert)
    def isBeingCarried(self):
        return self.beingCarried
    
    def placement(self):
        start_x = WIDTH-FREEZONE_WIDTH
        stop_x = WIDTH-self.size
        
        super().placement(start_x,stop_x)
    
    # La til metode som setter boolean-en "beingCarried" til true (mer objektorienter en at det gjøres i en annen klasse)
    def setGettingPickedUpTrue(self):
        self.beingCarried = True
    
    # Metode som utfører at sauen bli løftet (får samme x og y posisjon som menneske)
    def gettingPickedUp(self):
        if self.beingCarried == True:
            self.xPosition = person.xPosition
            self.yPosition = person.yPosition
        
    def removeSheep(self, sheep):
        sheeps.remove(sheep)
        gameboard.removeObject(sheep)


# Klasse for spillebrett
class GameBoard:
    def __init__(self):
        # Bruker globale konstanter for høyde og bredde i stedet for å legge de inn som egenskaper i gameboard.
        # Det korter ned antall bokstaver/ord, som er fint fordi det brukes mye.
        self.objects = []
        
    def addObject(self, theObject):
        self.objects.append(theObject)
        
    def removeObject(self, theObject):
        self.objects.remove(theObject)
    
    # Jeg lagde en egen metode som tegner objektene, og som kalles på i kjøre-løkken
    def drawObjects(self):
        for theobject in self.objects:
            pg.draw.rect(surface, theobject.color, pg.Rect(theobject.xPosition,theobject.yPosition,theobject.size,theobject.size))

    
    
        
# Objekter

# Spilleobjekt
gameobject = GameObject()

# Spillebrett
gameboard = GameBoard()

# Person
person = Person()
person.placement()
gameboard.addObject(person)

# Spøkelse
ghosts = []
def placeNewGhostOnBoard():
    ghost = Ghost()
    ghost.placement()
    gameboard.addObject(ghost)
    ghosts.append(ghost)
placeNewGhostOnBoard()
    
# Hindring
obstacles = []
def placeNewObstacleOnBoard():
    obstacle = Obstacle()
    obstacle.placement()
    gameboard.addObject(obstacle)
    obstacles.append(obstacle)
for i in range(3):
    placeNewObstacleOnBoard()

# Sau
sheeps = []
def placeNewSheepOnBoard():
    sheep = Sheep()
    sheep.placement()
    gameboard.addObject(sheep)
    sheeps.append(sheep)
for i in range(3):
    placeNewSheepOnBoard()






# Variabel som styrer om spillet skal kjøres
run = True

# Funksjon som ender spillet og printer ut poeng til konsoll
def endGame():
    global run
    run = False
    print(f"Du fikk {person.points} poeng!")





# Spill-løkken
while run:
    # Sørger for at løkken kjører i korrekt hastighet
    clock.tick(FPS)
    
    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekket om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False # Spillet skal avsluttes
            
            
            
    # Fyller skjermen med en farge
    surface.fill(GREEN)
    
    # Lager frisone for høyre side
    pg.draw.rect(surface, GREY, pg.Rect(0,0,FREEZONE_WIDTH,HEIGHT))
    
    # Lager frisone for venstre side
    pg.draw.rect(surface, GREY, pg.Rect(WIDTH-(FREEZONE_WIDTH),0,FREEZONE_WIDTH,HEIGHT))
    
    
    
    # Tegner objekter
    gameboard.drawObjects()
    
    # Metoder for personens bevegelse og kollisjoner
    person.move()
    person.checkCollision()
    
    # Beveger spøkelset
    for ghost in ghosts:
        ghost.move()
    
    # Sjekker om mennesket plukker opp sauen og "fester" saueobjektet til menneskeobjektet
    for sheep in sheeps:
        sheep.gettingPickedUp()



    # Viser poeng
    showPoints()
    

    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()



# Avslutter pygame
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()
