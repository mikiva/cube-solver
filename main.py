import json
import os

from cube import Cube

MAX_MOVES = 5

import kociemba

def test_solve():
    tests = [[('h', 1, 2), ('v', 1, 2)],
             [('s', 0, 2), ('h', 1, 2)],
             [('h', 0, 0), ('s', 1, 2)],
             [('h', 0, 2), ('s', 0, 0)],
             [('s', 0, 2), ('v', 1, 0)],
             [('v', 0, 2), ('h', 0, 0)]

             ]
    try:
        m = None
        cube = None
        for test in tests:
            cube = Cube(n=3)
            for move in test:
                print("====")
                m = (test, move)
                cube.twist_cube([move])
                cube.show()
                definition = cube.definition_string()
                algorithm = kociemba.solve(definition)

            print(algorithm)
    except Exception as e:
        print("not working", m)
        print("error cube", cube.definition_string(sep=True))
        raise e

def solve():
    cube = Cube(n=3)
    cube.show()
    print("SHUFFLE")
    cube.shuffle(l_rot=10, u_rot=25)
    cube.show()

    print("SOLVING")
    definition = cube.definition_string()
    algorithm = kociemba.solve(definition)
    cube.solve_from_algorithm(algorithm)

    cube.show()



def test_many():
    for i in range(100):
        try:
            solve()
        except Exception as e:
            print("Failed on: ", i)
            raise e
#

if __name__ == '__main__':
    #test_solve()
    #test_many()
    solve()
