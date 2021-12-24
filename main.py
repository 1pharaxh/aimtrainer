from ursina import *
def update():
    cube.x+=time.dt*.5
    cube.y+=time.dt*.5
    cube.z-=time.dt*.5
app = Ursina()

cube = Entity(model='cube', scale=(2,3,1),position=(0,0,0), rotation = (45,45,0), color=color.red)

app.run()