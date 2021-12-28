############### TO DO : ###############
######### IMPROVE TEXTURES ############
######### ADD MUSIC AND MENUS #########
######### IMPROVE COLORS ##############
######### WORK ON UPDATES 1 & 2 #######

from ursina import *
from random import uniform
from ursina.prefabs.first_person_controller import FirstPersonController
import time
app=Ursina()
# Sentinel flag for spawning cubes (for flick training !)
run_cube = False         
# Sentinel flag for moving spheres (for tracking training !)
run_sphere = False
# Cube list containing all cube entity onjects.                      
cubes=[]
# Sphere list containing all sphere entity objects.                       
spheres =[]
# Update function for:
# a) Spawning multiple cubes if run_cube is True.
# b) Moving spheres up if run_sphere is True.                      
def update():
    global cubes,spheres, run_cube, run_sphere
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
# Sentinel values for clicks, score and final score
# used later on to calculate the final score
clicks = 0
score = 0
final_score = 0
# This function reads keyboard and mouse input
# when '1' is pressed then cubes are spawned
# when '2' is pressed then spheres are spawned 
def input(key):
    global cubes, spheres, run_cube, run_sphere, clicks, score, final_score
    if not run_cube:
        # Pressing '1' calls the new_cube function
        if key == '1':   
            run_cube = True
            run_sphere = False
            invoke(new_cube, delay=0.01)
    if not run_sphere: 
        # Pressing '2' calls the new_sphere function
        if key == '2':
            run_sphere = True
            run_cube = False                
            invoke(new_sphere, delay=0.1)  
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
        # Displaying text on every mouse click.
        popup = Text('Score '+str(final_score), scale=2, color=color.red, origin =(0,-8))
        # Text is removed every 3 miliseconds of displaying.
        destroy(popup, delay=.3)
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
                  color=color.rgb(192,192,192))
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
# Generating custom sky.
Sky(texture = load_texture('Assets\Textures\Skybox.png'))
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
# Generating the wall.
wall_1=Entity(model="cube", 
              collider="box", 
              position=(-2, 0, 0), 
              scale=(8, 5, 1), 
              rotation=(0,90,0),
              texture="brick", 
              texture_scale=(5,5), 
              color=color.red)
# Generating gun based on custom model.
gun=Entity(model="Assets\Models\Submachine_Gun_LP_1.obj", 
           parent=camera.ui, 
           scale=.001,
           position=(.3, -.2),
           rotation=(0, 105, 0),
           color=color.rgb(166, 220, 237))
app.run()
