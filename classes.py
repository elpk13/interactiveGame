import math

# Any object that exists in the world is of object class.
class Object:
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance):
        self.xpos = xpos # Distance between object's left side and that of the world.
        self.ypos = ypos # Distance between object's TOP side and that of the world.
        self.width = width
        self.height = height
        self.dynamic = dynamic # A Boolean indicating whether the object is animated.
        self.appearance = appearance # Could be a Surface or a list or a list of lists of surfaces
        self.nightappearance = nightappearance
        self.ybase = ypos + height # Used for sorting blit order.

    def draw(self,screen,playerx,playery,window_width,window_height,night):
        if night: # Night-time is defined in globals.  Seasons are defined in the tree class.
            if self.dynamic:
                appearance = self.nightappearance[len(self.nightappearance)/time]
            else:
                appearance = self.nightappearance
        else:
            if self.dynamic:
                appearance = self.appearance[len(self.appearance)/time]
            else:
                appearance = self.appearance
        screen.blit(appearance,(int(self.xpos-playerx+window_width/2),int(self.ypos-playery+window_height/2)))

# Objects that impede the player's movement have a collision box as well.
# The 'collidesat' checks if a point is inside it.
# A collision box is - in this code - a tuple (a,b,c,d), 0 < a < b < 1,
# 0 < c < d < 1, referring to the portion of the image considered the box.
class Obstacle(Object):
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance,collisionBox):
        self.collisionBox = collisionBox
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance)

    def collidesat(self,possiblex,possibley):
        if self.collisionBox[0] < (possiblex-self.xpos)/self.width < self.collisionBox[1] and self.collisionBox[2] < (possibley-self.ypos)/self.height < self.collisionBox[3]:
            return True
        return False

# Objects below have specific appearances that should relate to other properties,
# like a stream's aim or a tree's type; however, these are passed to the class in
# the initialization functions like 'pourStream' or 'plantTree' so that the
# graphics dictionaries can be passed as well.

class StreamSegment(Object): # appearance should come from the getStreamGraphics dictionary
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance,aim):
        self.aim = aim
        if len(aim) < 4:
            self.a = int(aim[:2])*math.pi/180 # Angle in radians as float, for straights and sources
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance)

    def __str__(self):
        return 'A stream segment of aim ' + self.aim + ' at (' + self.xpos + ',' + self.ypos + ')'

    def covers(self,possiblex,possibley,streamCurveCoefficients): # Curve coefficients come from
        x = possiblex - self.xpos                                 # the dictionary.
        y = self.ypos + self.height - possibley
        if not (0 < x < self.width and 0 < y < self.height):
            return False
        if self.aim in ['30','45','60']:
            if y > x*math.tan(self.a) and y < x*math.tan(self.a) + 50/math.cos(self.a):
                return True
            return False
        elif self.aim[-1] == 's':
            if ((x-self.width/2)**2+(y-self.height/2)**2)**0.5 < self.width/2:
                return True
            elif x < self.width/2 and y > x*math.tan(self.a) and y < x*math.tan(self.a) + 50/math.cos(self.a):
                return True
            return False
        else:
            f, g = streamCurveCoefficients[self.aim]
            if f[0]*x**3 + f[1]*x**2 + f[2]*x + f[3] > y > g[0]*x**3 + g[1]*x**2 + g[2]*x + g[3]:
                return True
            return False

class Tree(Obstacle): # The 'appearance' and 'evergreen' states should come from the getTreeGraphics dictionary.
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance,type,evergreen):
        self.type = type
        self.evergreen = evergreen # Collision box for trees is defined here \|/
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance,(0.4,0.6,0.6,0.8))

    def __str__(self):
        return 'A(n) ' + self.type + ' tree at (' + self.xpos + ',' + self.ypos + ')'

    def draw(self,screen,playerx,playery,window_width,window_height,time,night):
        if time % 2400 < 1200:
            s = 0 # And the leaves that are green...
        elif time % 2400 < 1800:
            s = 1 # turn to brown
        else:
            s = 2 # and they wither with the wind
        m = 3
        t = time % (8*m)
        if t % (4*m) < 2*m: # Unique animation for trees is described in a
            f = m # side document.
        elif t < 3*m:
            f = t - m
        elif t < 4*m:
            f = 5*m - t
        elif t < 7*m:
            f = 7*m - t
        else:
            f = t-7*m
        if night:
            if self.evergreen:
                appearance = self.nightappearance[f]
            else:
                appearance = self.nightappearance[s][f]
        else:
            if self.evergreen:
                appearance = self.appearance[f]
            else:
                appearance = self.appearance[s][f]
        screen.blit(appearance,(int(self.xpos-playerx+window_width/2),int(self.ypos-playery+window_height/2)))

class Rock(Obstacle): # Appearance can be any Surface.  Ideally one depicting a rock.
    def __init__(self,xpos,ypos,height,width,appearance,nightappearance):
        super().__init__(xpos,ypos,height,width,False,appearance,nightappearance,(0.2,0.8,0.2,0.8))

class Decoration(Object): # Not necessary, but seemed nice
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance):
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance)

class Interactive(Object):
    def __init__(self,xpos,ypos,height,width,dynamic,appearance,nightappearance):
        super().__init__(xpos,ypos,height,width,dynamic,appearance,nightappearance)

    def covers(self,possiblex,possibley):
        if self.xpos < possiblex < self.xpos + self.width and self.ypos < possibley < self.ypos + self.height:
            return True
        return False

class Print(Interactive): # Apperance should come from dictionary
    def __init__(self,xpos,ypos,height,width,animal,appearance):
        self.animal = animal
        super().__init__(xpos,ypos,height,width,False,appearance,appearance)

class Wolf: # Consider making part of a general animal class for the hunting game?
    def __init__(self,name,framelists):
        self.name = name
        self.framelists = framelists

class World:
    def __init__(self,worldx,worldy,background,nightbackground,streams,forest,rocks,prints,decorations,settlements):
        self.width = worldx # Dimensions of the world
        self.height = worldy
        self.background = background # Background, which should be scaled to the dimensions of the world.
        self.nightbackground = nightbackground # in its initializer, generateWorld().
        self.streams = streams # A list of lists of stream segments
        self.forest = forest # A list of trees
        self.rocks = rocks # A list of rocks (really, any obstacles)
        self.prints = prints # A list of prints
        self.decorations = decorations # A list of decoration objects
        self.settlements = settlements # A list of settlement objects
        self.obstacles = forest + rocks # All obstacles, to be sent to the posok() function
        self.interactives = prints + settlements # All interactives, to be sent to the collision() function
        self.objectsofheight = forest + rocks + prints + decorations + settlements
        self.objectsofheight.sort(key=lambda x:x.ybase) # Sort all blittables, to be sent to the drawscreen() function
