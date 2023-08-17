import random

from ursina import *
from UIhelpers import after
from helper import moves, annotation_to_move
from cube import Cube as RubiksCube

app = Ursina()

rubiks = None

cube_colors = [
    color.red,
    color.orange,
    color.white,
    color.yellow,
    color.blue,
    color.green
]
# (Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1), Vec3(-1, 0, 0), Vec3(0, -1, 0), Vec3(0, 0, -1)) #R, U, B, L, D, F
cube_faces = {
    "R": Vec3(1, 0, 0),
    "L": Vec3(-1, 0, 0),
    "U": Vec3(0, 1, 0),
    "D": Vec3(0, -1, 0),
    "B": Vec3(0, 0, 1),
    "F": Vec3(0, 0, -1)
}


def spin(entity):
    print(entity)
    entity.animate("rotation_y", entity.rotation_y + 360, duration=2, curve=curve.in_out_expo)


cubes = []
combine_parent = None
rotation_helper: Entity = None
collider = None
shuffle_button = None

def collider_input(key):
    global animations
    if mouse.hovered_entity == collider:
        if key == "left mouse down":
            animations.append(rotate_side(mouse.normal, 1))
        if key == "right mouse down":
            animations.append(rotate_side(mouse.normal, -1))

    collider.ignore_input = True

    @after(.25 * 1)
    def _():
        collider.ignore_input = False
        # check_for_win()

BASE_SPEED = 0.1
def rotate_side(normal, direction=1, speed=1):
    animated = "UNKNOWN"
    if normal == Vec3(1, 0, 0):
        def animated():

            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.x > 0]
            return rotation_helper.animate("rotation_x", 90 * direction, duration=BASE_SPEED * speed,
                                           curve=curve.linear,
                                           interrupt="kill")
    elif normal == Vec3(-1, 0, 0):
        def animated():
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.x < 0]
            return rotation_helper.animate("rotation_x", -90 * direction, duration=BASE_SPEED * speed,
                                           curve=curve.linear,
                                           interrupt="kill")

    elif normal == Vec3(0, 1, 0):
        def animated():
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.y > 0]
            return rotation_helper.animate("rotation_y", 90 * direction, duration=BASE_SPEED * speed,
                                           curve=curve.linear,
                                           interrupt="kill")
    elif normal == Vec3(0, -1, 0):
        def animated():

            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.y < 0]
            return rotation_helper.animate("rotation_y", -90 * direction, duration=BASE_SPEED * speed,
                                           curve=curve.linear,
                                           interrupt="kill")

    elif normal == Vec3(0, 0, 1):
        def animated():
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.z > 0]
            rotation_helper.animate("rotation_z", 90 * direction, duration=BASE_SPEED * speed,
                                    curve=curve.linear,
                                    interrupt="kill")
    elif normal == Vec3(0, 0, -1):
        def animated():
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.z < 0]
            return rotation_helper.animate("rotation_z", -90 * direction, duration=BASE_SPEED * speed,
                                           curve=curve.linear,
                                           interrupt="kill")

    # if animated:
    #    print("ANIMATED", animated.finished)
    # invoke(reset_rotation_helper, delay=.22 * speed)
    return animated


#
# if speed:
#    collider.ignore_input = True
#
#    @after(.25 * speed)
#    def _():
#        collider.ignore_input = False
#        # check_for_win()


def reset_rotation_helper():
    global cubes, rotation_helper
    [setattr(e, "world_parent", scene) for e in cubes]
    rotation_helper.rotation = (0, 0, 0)


# cube = Entity(model='cube', color=hsv(300, 1, 1), scale=2, collider='box')


def randomize():
    faces = list(
        cube_faces.values())  # (Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1), Vec3(-1, 0, 0), Vec3(0, -1, 0), Vec3(0, 0, -1)) #R, U, B, L, D, F
    for i in range(20):
        rotate_side(normal=random.choice(faces), direction=random.choice((-1, 1)), speed=0)



animations = []
current_animation = "INIT"


def shuffle():
    print(moves.keys())
    all_moves = list(moves.keys())

    for i in range(20):
        a = random.choice(all_moves)
        direction = 1 if "\'" in a else -1
        print(direction, a[0])
        animation = rotate_side(cube_faces[a[0]], direction=direction, speed=1)
        if animation is not None:
            animations.append(animation)
            rubiks.twist_cube([moves[a]])

        # time.sleep(0.4)

    rubiks.show()

debug_text = Text(text=len(cubes), x=.3, y=-.2)


import time
last_animation = 0
def update():
    global current_animation, shuffle_button, animations, last_animation
    if len(animations) > 0:
        if current_animation == "INIT" or time.time() > last_animation + 0.15:

            next_animation = animations.pop()
            if next_animation:
                invoke(reset_rotation_helper)
                animation_result = next_animation()
                if animation_result is not None:
                    current_animation = animation_result
            last_animation = time.time()
        shuffle_button.enabled = False
        shuffle_button.text = "disabled"

    else:
        shuffle_button.enabled = True
        shuffle_button.text = "enabled"


def input(key):
    ...
    # print(key)


def solve():

    import kociemba
    global animations
    definition = rubiks.definition_string()
    algorithm = kociemba.solve(definition)

    print(algorithm)

    for a in algorithm.split(" "):
        move = annotation_to_move(a)
        rubiks.twist_cube(move)
        if "2" in a:
            rot1 = rotate_side(cube_faces[a[0]])
            rot2 = rotate_side(cube_faces[a[0]])
            print("2ROTATIONS", rot1, rot2)
            animations.append(rot1)
            animations.append(rot2)
        else:
            direction = 1 if "\'" in a else -1
            rot = rotate_side(cube_faces[a[0]], direction=direction)
            print("ROTATION", rot)
            animations.append(rot)



    rubiks.show()





def reset():
    scene.clear()
    init()
def init():
    global cubes, combine_parent, collider, rotation_helper

    combine_parent = Entity(enabled=False)
    for i in range(3):
        dir = Vec3(0, 0, 0)
        dir[i] = 1
        e = Entity(parent=combine_parent, model="plane", origin_y=-.5, texture="white_cube", color=cube_colors[i * 2])
        e.look_at(dir, "up")
        e_flipped = Entity(parent=combine_parent, model="plane", origin_y=-.5, texture="white_cube",
                           color=cube_colors[(i * 2) + 1])
        e_flipped.look_at(-dir, "up")
    combine_parent.combine()

    cubes = []
    for x in range(3):
        for y in range(3):
            for z in range(3):
                e = Entity(model=copy(combine_parent.model), position=Vec3(x, y, z) - Vec3(3, 3, 3) / 3,
                           texture="white_cube")
                cubes.append(e)

    rotation_helper = Entity()
    collider = Entity(model="cube", scale=3, collider="box", visible=False)
    collider.input = collider_input


shuffle_button = Button(text="Shuffle", color=color.azure, position=(.7, -.3), on_click=shuffle)
shuffle_button.fit_to_text()
solve_button = Button(text="Solve", color=color.azure, position=(.7, -.36), on_click=solve)
solve_button.fit_to_text()

reset_button = Button(text="Reset", color=color.azure, position=(.7, -.2), on_click=reset)
reset_button.fit_to_text()
init()
EditorCamera()
# combine_parent.on_click = spin

if __name__ == '__main__':
    rubiks = RubiksCube(n=3)

    print(shuffle)
    app.run()
