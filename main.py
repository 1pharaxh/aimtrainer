from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import * # import as usual
app = Ursina()       # create app as usual
grid_texture = load_texture('Assets\Textures\grid_texture.jpg')

ground = Entity(model='plane', color=color.rgb(255,250,240), texture='grid_texture', collider='mesh', scale=(100,1,100)) # rgb vals for floral white
player = FirstPersonController()

box = Entity(model='cube',        #replace this for a gun.
             origin=(0,0.7,-5),   
             parent=camera,        
             color=color.blue,     
             texture='grass')     

def update():   #update function for movement                  
    if held_keys['a']:
        camera.x -= 10 * time.dt 
    elif held_keys['d']:
        camera.x += 10 * time.dt
    elif held_keys['w']:
        camera.z += 10 * time.dt
    elif held_keys['s']:
        camera.z -= 10 * time.dt

Sky() 
app.run() # run