from ursina import *
from helper import moves, annotation_to_move
from cube import Cube as RubiksCube
from functools import partial
import time


app = Ursina()

rubiks = None

animations = []
current_animation = "INIT"

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
    if mouse.hovered_entity == collider:
        f = [i for i in cube_faces if cube_faces[i] == mouse.normal][0]
        print(f)
        if key == "left mouse down":
            twist(f, 1)
        if key == "right mouse down":
            twist(f, -1)

    # collider.ignore_input = True

    # @after(.25 * 1)
    # def _():
    #    collider.ignore_input = False
    #    # check_for_win()


BASE_SPEED = 0.1
TURN_DEGREES = 90

ANIMATION_FINISHED = True


def _animated():
    ...


def face_rotation_animation_toggle():
    global ANIMATION_FINISHED
    ANIMATION_FINISHED = not ANIMATION_FINISHED


CURVE = curve.linear
INTERRUPT = "finish"


def rotate_side(normal, direction=1, speed=1.0):
    animated = "UNKNOWN"
    if normal == Vec3(1, 0, 0):  # Right
        def animated(_speed=speed):
            reset_rotation_helper()
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.x > 0]
            return rotation_helper.animate("rotation_x", TURN_DEGREES * direction, duration=BASE_SPEED * _speed,
                                           curve=CURVE,
                                           interrupt=INTERRUPT)
    elif normal == Vec3(-1, 0, 0):  # Left
        def animated(_speed=speed):
            reset_rotation_helper()
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.x < 0]
            return rotation_helper.animate("rotation_x", -TURN_DEGREES * direction, duration=BASE_SPEED * _speed,
                                           curve=CURVE,
                                           interrupt=INTERRUPT)

    elif normal == Vec3(0, 1, 0):  # Up
        def animated(_speed=speed):
            reset_rotation_helper()
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.y > 0]
            return rotation_helper.animate("rotation_y", TURN_DEGREES * direction, duration=BASE_SPEED * _speed,
                                           curve=CURVE,
                                           interrupt=INTERRUPT)
    elif normal == Vec3(0, -1, 0):  # Down
        def animated(_speed=speed):
            reset_rotation_helper()

            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.y < 0]
            return rotation_helper.animate("rotation_y", -TURN_DEGREES * direction, duration=BASE_SPEED * _speed,
                                           curve=CURVE,
                                           interrupt=INTERRUPT)

    elif normal == Vec3(0, 0, 1):  # Back
        def animated(_speed=speed):
            reset_rotation_helper()
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.z > 0]
            return rotation_helper.animate("rotation_z", -TURN_DEGREES * direction, duration=BASE_SPEED * _speed,
                                           curve=CURVE,
                                           interrupt=INTERRUPT)
    elif normal == Vec3(0, 0, -1):  # Front
        def animated(_speed=speed):
            reset_rotation_helper()
            [setattr(e, "world_parent", rotation_helper) for e in cubes if e.z < 0]
            return rotation_helper.animate("rotation_z", TURN_DEGREES * direction, duration=BASE_SPEED * _speed,
                                           curve=CURVE,
                                           interrupt=INTERRUPT)


    return animated


def twist(face, direction):
    animation = rotate_side(cube_faces[face[0]], direction=direction, speed=1)
    if animation:
        animations.append(animation)
        f = f"{face}\'" if direction < 0 else face
        rubiks.twist_cube([moves[f]])
        rubiks.show()


def reset_rotation_helper():
    global cubes, rotation_helper
    [setattr(e, "world_parent", scene) for e in cubes]
    rotation_helper.rotation = (0, 0, 0)


def randomize():
    faces = list(
        cube_faces.values())  # (Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1), Vec3(-1, 0, 0), Vec3(0, -1, 0), Vec3(0, 0, -1)) #R, U, B, L, D, F
    for i in range(20):
        rotate_side(normal=random.choice(faces), direction=random.choice((-1, 1)), speed=0)


debug_text = Text(text="debug", origin=(0, 18), color=color.white)


def shuffle(speed=1):
    # print(moves.keys())
    all_moves = list(moves.keys())

    for i in range(20):
        a = random.choice(all_moves)
        direction = -1 if "\'" in a else 1
        animation = rotate_side(cube_faces[a[0]], direction=direction, speed=speed)
        if animation is not None:
            animations.append(animation)
            rubiks.twist_cube([moves[a]])

        # time.sleep(0.4)
    debug_text.text = rubiks.get_solution()
    rubiks.show()



last_animation = 0


def update():
    global current_animation, shuffle_button, animations, last_animation

    if len(animations) > 0:
        if current_animation == "INIT" or current_animation.finished:  # time.time() > last_animation + BASE_SPEED + .01:
            next_animation = animations.pop(0)
            if next_animation:
                animation_result = next_animation()
                if animation_result is not None:
                    current_animation = animation_result

            last_animation = time.time()
        shuffle_button.enabled = False


    else:
        shuffle_button.enabled = True


def input(key):
    ...
    # print(key)


def solve(speed=1):
    global animations
    algorithm = rubiks.get_solution()
    print(algorithm)

    for a in algorithm.split(" "):
        move = annotation_to_move(a)
        rubiks.twist_cube(move)
        if "2" in a:
            rot1 = rotate_side(cube_faces[a[0]], speed=speed)
            rot2 = rotate_side(cube_faces[a[0]], speed=speed)
            animations.append(rot1)
            animations.append(rot2)
        else:
            direction = -1 if "\'" in a else 1
            rot = rotate_side(cube_faces[a[0]], direction=direction, speed=speed)
            animations.append(rot)

    rubiks.show()


def reset():
    scene.clear()
    init()


def init(state=None):
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


shuffle_button = Button(text="Shuffle", color=color.azure, position=(.7, -.3), on_click=partial(shuffle, 0))
shuffle_button.fit_to_text()
solve_button = Button(text="Solve", color=color.azure, position=(.7, -.36), on_click=partial(solve, 1))
solve_button.fit_to_text()

init()
EditorCamera()
# combine_parent.on_click = spin

if __name__ == '__main__':
    rubiks = RubiksCube(n=3)

    window.size = (1200, 600)
    window.update_aspect_ratio()
    app.run()
