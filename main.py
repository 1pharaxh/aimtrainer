############### TO DO : ###############
######### ADD MUSIC AND MENUS #########
from ursina import *
from random import uniform
from ursina import texture_importer
from ursina.prefabs.first_person_controller import FirstPersonController
app=Ursina(boderless=False)
# Sentinel flag for spawning cubes (for flick training !).
run_cube = False         
# Sentinel flag for moving spheres (for tracking training !).
run_sphere = False
# Sentinel flag for spawning pistol.
spawn_pistol = False
# Sentinel flag for spawning shotgun.
spawn_shotgun = False
# Cube list containing all cube entity objects.                    
cubes=[]
# Sphere list containing all sphere entity objects.                       
spheres =[]
# pistol list containing all pistol entity objects.                    
pistols=[] 
# shotguns list containing all shotguns entity objects.                       
shotguns =[]

Audio("Assets\Audio\Ghostrunner Soundtrack - Truth to Power.ogg", loop=True, volume=0.5)

# Update function for:
# a) Spawning multiple cubes if run_cube is True.
# b) Moving spheres up if run_sphere is True.                      
def update():
    global cubes,spheres, pistols, shotguns, run_cube, run_sphere, spawn_pistol, spawn_shotgun
    # Spawning multiple cubes.
    if run_cube: 
        for c in cubes:
            # If more than 1 cube then getting rid of
            # additional cubes.
            if len(cubes) > 1:
                cubes.remove(c); destroy(c)
        # Only working with cubes so no spheres.
        for s in spheres:
            spheres.remove(s); destroy(s)
    # Spawning spheres and moving them by 
    # the y axis (up)
    if run_sphere:
        for s in spheres:
            s.y += 0.1
            # If they go above 10 in y 
            # then getting rid of them.
            if s.y > 10:
                spheres.remove(s)
                destroy(s)
        # Only working with spheres so no cubes. 
        for c in cubes:
            cubes.remove(c)
            destroy(c)
    # Spawning pistol.
    if spawn_pistol:
        for p in pistols:
            # Removing reduant (previously generated pistols)
            if len(pistols) > 1:
                pistols.remove(p)
                destroy(p)
        # Only working with pistols so no shotguns. 
        for shotgun1 in shotguns:
            shotguns.remove(shotgun1)
            destroy(shotgun1)
    # Spawning shotgun.
    if spawn_shotgun:
        for shotgun1 in shotguns:
            # Removing reduant (previously generated pistols)
            if len(shotguns) > 1:
                shotguns.remove(shotgun1)
                destroy(shotgun1)
        # Only working with shotguns so no pistols. 
        for p in pistols:
            pistols.remove(p)
            destroy(p)
# Sentinel values for clicks, score, final score
# and lives used later on to calculate the final score
# and remaining lives.
clicks = 0
score = 0
final_score = 0
lives = 3
# This function reads keyboard and mouse input
# when '1' is pressed then cubes are spawned.
# when '2' is pressed then spheres are spawned.
# when '3' is pressed then pistol is spawned.
# when '4' is pressed then shotgun is spawned.
heart1 = Entity(model='quad', 
               parent=camera.ui,
               position = (-0.8,0.45),
               scale=0.1,
               texture='Assets\Textures\heart')
heart2 = Entity(model='quad', 
               parent=camera.ui,
               position = (-0.7,0.45),
               scale=0.1,
               texture='Assets\Textures\heart')
heart3 = Entity(model='quad', 
               parent=camera.ui,
               position = (-0.6,0.45),
               scale=0.1,
               texture='Assets\Textures\heart')
scoreList = []
def input(key):
    global cubes, spheres, pistols, shotguns, spawn_pistol, spawn_shotgun, run_cube, run_sphere, clicks, score, final_score, lives, scoreList
    if not run_cube:
        # Pressing '1' calls the new_cube function
        if key == '1':   
            run_cube = True
            run_sphere = False
            invoke(new_cube, delay=0.1)
    if not run_sphere: 
        # Pressing '2' calls the new_sphere function
        if key == '2':
            run_sphere = True
            run_cube = False                
            invoke(new_sphere, delay=0.1) 
    if not spawn_pistol: 
        # Pressing '3' calls the new_pistol function        
        if key == '3':
            spawn_pistol = True
            spawn_shotgun = False
            invoke(new_pistol, delay=0.1)
    if not spawn_shotgun:
        # Pressing '4' calls the new_shotgun function
        if key == '4':
            spawn_pistol = False
            spawn_shotgun = True
            invoke(new_shotgun, delay=0.1)
    if key=="left mouse down":
        # Everytime on clicking left mouse button
        # value of click increases by 1.
        clicks += 1
        Audio("Assets\Audio\Realistic Gunshot Sound Effect.wav")
        for c in cubes:
            if c.hovered:
                # Cube instance removed.
                destroy(c) 
                # Impact audio.
                Audio("Assets\Audio\impact.wav") 
                score += 1
        for s in spheres:
            if s.hovered:
                # Sphere instance removed.
                s.z += -19
                # Impact audio,
                Audio("Assets\Audio\impact.wav")
                score += 1
        if clicks-score == 0:
            # Calculating final score here.
            final_score += 1
        else:
            final_score = score
        if clicks > final_score:
            scoreList.append(final_score)
            final_score, clicks, score = 0,0,0
            lives -= 1
        if lives == 2:
            destroy(heart3)
        if lives == 1:
            destroy(heart2)
        if lives > 0:
            # Displaying text on every mouse click.
            popup = Text('Score '+str(final_score), scale=2, color=color.red, origin =(0,-8))
            # Text is removed every 3 miliseconds of displaying.
            destroy(popup, delay=.3)
        if lives == 0:
            # When lives are 0 then calling the exitGame function after 10 seconds.
            destroy(heart1)
            gameover = Text('GAMEOVER', scale=5, color=color.blue, origin=(0,0))
            exitText = Text('exiting in 10 seconds',origin=(0,4), scale=2)
            final=Text('Your High Score '+str(max(scoreList)), scale=2, color=color.red, origin =(0,-8))
            invoke(exitGame, delay=10)

# This function quits game when invoked.
def exitGame():
    exit()
# Function to make cube entities.
def new_cube():
    global cubes, run_cube
    wx=uniform(-10, -20)
    wy=uniform(13, 3)
    wz=uniform(.8, 5)
    # Generating cubes with silver color.
    cube = Entity(model='cube', 
                  scale=1, 
                  collider="box", 
                  position=(wx,wy,wz), 
                  texture='white_cube',
                  highlight_color=color.violet,
                  color=color.light_gray)
    cubes.append(cube)
    # Generating more cubes if run_cubes is True using recursion.
    if run_cube:
        # UPDATE 1. can speed up cube generation by modifying the delay
        invoke(new_cube,delay = random.uniform(1,3))
# Function to make sphere entities.
def new_sphere():
    global spheres, run_sphere
    sx=uniform(-12, -7) 
    sy=uniform(1, 5)
    sz=uniform(5, 10)
    # Generating sphere with golden color.
    sphere = Entity(model='sphere',
                    scale=1, collider="box", 
                    position=(sx, sy, sz), 
                    color=color.rgb(255,215,0))
    spheres.append(sphere)
    # Generating more spheres if run_sphere is True using recursion.
    if run_sphere:
        # UPDATE 2. can speed up cube generation by modifying the delay
        invoke(new_sphere,delay = random.uniform(1,3))
# Function to make pistol entity.
def new_pistol():
    global pistols, spawn_pistol
    Pistol=Entity(model="Assets\Models\Colt\colt1911", 
            parent=camera.ui, 
            texture=load_texture('Assets\Models\Colt\Colt_M1911_1688'),
            scale=0.11,
            position=(.27, -.2),
            rotation=(100, 170, -90))
    pistols.append(Pistol)
    # Generating pistols if spawn_pistol is True using recursion.
    if spawn_pistol:
        invoke(new_pistol, delay = 0.1)
# Function to make shotgun entity.
def new_shotgun():
    global shotguns, spawn_shotgun
    Shotgun=Entity(model="Assets\Models\M1887\M1887", 
           parent=camera.ui, 
           texture=load_texture('Assets\Models\M1887\P_PW_M1887_D'),
           scale=1.4,
           position=(.3, -.3),
           rotation=(0, 95, -5))
    shotguns.append(Shotgun)
    # Generating shotguns if spawn_shotgun is True using recursion.
    if spawn_shotgun:
        invoke(new_shotgun, delay = 0.1)
# Generating custom sky.
Sky(texture = load_texture('Assets\Textures\synthwave_retrowave___neon_80s___background_by_rafael_de_jongh_d9wsq5j.jpg'))
# Loading textures for grid(PNG,JPG OR JPEG would work).
grid_texture = load_texture('Assets\Textures\grid_texture.jpg')
# Setting FirstPersonController instance to player
player=FirstPersonController()
# Generating the grid ground
ground=Entity(model='plane', 
              scale=(100, 1, 100), 
              color=color.white, 
              texture="grid_texture", 
              texture_scale=(1, 1), 
              collider='box')
# Generating the robot.
robot=Entity(model="Assets\Models\Robo warrior\Robo warrior", 
              collider="box", 
              scale=0.1,
              position=(-30, -2, 0),
              rotation=(0,50,0),
              texture="white_cube",
              color=color.violet,
              highlight_color=color.pink)

# Generating the crosshair
crosshair = Entity(model='quad', 
               parent=camera.ui,
               position = (0,0),
               scale=0.050,
               texture='Assets\Textures\crosshair')
#making full screen
window.fullscreen=True
app.run()
