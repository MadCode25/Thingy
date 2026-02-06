from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()
window.title = "Simple Craft | sc1826"
player = FirstPersonController()
Sky(color=color.cyan)
inventory_sprite = Sprite(model='quad', color=color.gray, texture="inventory.jpg", position=(0,-0.3), parent=camera.ui)
box_images = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"]
Sprite(texture=box_images[0], parent=inventory_sprite, position=(-0.39,-0.06), scale=0.3, z=-2)
Sprite(texture=box_images[1], parent=inventory_sprite, position=(-0.19,-0.06), scale=0.3, z=-2)
Sprite(texture=box_images[2], parent=inventory_sprite, position=(0.02,-0.06), scale=0.3, z=-2)
Sprite(texture=box_images[3], parent=inventory_sprite, position=(0.22,-0.06), scale=0.3, z=-2)
Sprite(texture=box_images[4], parent=inventory_sprite, position=(0.40,-0.06), scale=0.3, z=-2)

with open("data.mct", "w") as data:
    data.write("")
    data.write("SC1826DTF\n")
    data.write("def TerrainData():\n")

boxes = []
box_type = 'grass'

# Generate Platform of Boxes (50x50)
for i in range(40):
    for j in range(40):
        box = Button(color=color.green, position=(i,0,j), 
                     texture="1.jpg", model='cube', scale=1, parent=scene, origin_y=-0.5)
        boxes.append(box)
        with open("data.mct", "a") as data:
            data.write(f"{box.position} {box.texture}\n")

def input(key):
    global box_type
    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                if box_type == 'grass':
                    new = Button(color=color.green, position=box.position + mouse.normal, 
                                texture="1.jpg", model='cube', scale=1, parent=scene, origin_y=-0.5)
                    boxes.append(new)
                    with open("data.mct", "a") as data:
                        data.write(f"{new.position} {new.texture}\n")

                if box_type == 'mud':
                    new = Button(color=color.brown, position=box.position + mouse.normal, 
                                texture="2.jpg", model='cube', scale=1, parent=scene, origin_y=-0.5)
                    boxes.append(new)
                    with open("data.mct", "a") as data:
                        data.write(f"{new.position} {new.texture}\n")
                if box_type == 'scratched metal':
                    new = Button(color=color.gray, position=box.position + mouse.normal, 
                                texture="3.jpg", model='cube', scale=1, parent=scene, origin_y=-0.5)
                    boxes.append(new)
                    with open("data.mct", "a") as data:
                        data.write(f"{new.position} {new.texture}\n")
                if box_type == 'stone':
                    new = Button(color=color.gray, position=box.position + mouse.normal, 
                                texture="4.jpg", model='cube', scale=1, parent=scene, origin_y=-0.5)
                    boxes.append(new)
                    with open("data.mct", "a") as data:
                        data.write(f"{new.position} {new.texture}\n")
                if box_type == 'error_block_fake':
                    new = Button(color=color.white, position=box.position + mouse.normal, 
                                texture="5.jpg", model='cube', scale=1, parent=scene, origin_y=-0.5)
                    boxes.append(new)
                    with open("data.mct", "a") as data:
                        data.write(f"{new.position} {new.texture}\n")
                
            if key == 'right mouse down':
                line_to_remove = f"{box.position} {box.texture}\n"
                with open("data.mct", "r") as data:
                    content = data.readlines()
                if line_to_remove in content:
                    content.remove(line_to_remove)
                    with open("data.mct", "w") as data:
                        data.writelines(content)
                boxes.remove(box)
                destroy(box)

    if key == '1':
        box_type = 'grass'
    if key == '2':
        box_type = 'mud'
    if key == '3':
        box_type = 'scratched metal'
    if key == '4':
        box_type = 'stone'
    if key == '5':
        box_type = "error_block_fake"
    if key == 'escape':
        quit()

app.run()