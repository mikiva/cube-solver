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

def solve(state=None):
    cube = Cube(n=3, state=state)
    cube.show()
    if state is None:
        print("=== SHUFFLING CUBE ===")
        cube.shuffle(l_rot=10, u_rot=25)
        cube.show()

    print("=== SOLVING CUBE ===")
    definition = cube.definition_string()
    #print(cube.definition_string(sep=True))
    algorithm = kociemba.solve(definition)
    print("MOVES: ", algorithm)
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
#order = [TOP, RIGHT, FRONT, BOTTOM, LEFT, BACK]
if __name__ == '__main__':

    state="""
                BFU FUF BUF
RRD LLD FLF     LRR FFU RBR      UUB BRD BBU    LLU LBU FRL
                DRD BDD DDL
    """
    #state=None

    state = "".join(state.split())

    #test_solve()
    #test_many()
    solve(state=state)
    #solve()
