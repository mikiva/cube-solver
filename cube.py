from random import randint, choice
from helper import annotation_to_move

TOP = 0
LEFT = 1
FRONT = 2
RIGHT = 3
BACK = 4
BOTTOM = 5


class Cube:
    def __init__(self,
                 n=3,
                 # colors = ['w', 'o', 'g', 'r', 'b', 'y'],
                 colors=["⬜", "🟧", "🟩", "🟥", "🟦", "🟨"],
                 # colors=["U", "R", "F", "D", "L", "B"],
                 state=None
                 ):
        if state is None:

            self.state = state
            self.n = n
            self.colors = colors
            self.reset()
        else:
            self.n = int((len(state) / 6) ** (0.5))
            self.colors = []
            self.cube = [[[]]]
            for i, s in enumerate(state):
                if s not in self.colors:
                    self.colors.append(s)
                self.cube[-1][-1].append(s)
                if len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) < self.n:
                    self.cube[-1].append([])
                elif len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) == self.n and i < len(state) - 1:
                    self.cube.append([[]])
        # self.show()

    def reset(self):
        self.cube = [[[c for x in range(self.n)] for y in range(self.n)] for c in self.colors]

    def shuffle(self, l_rot=5, u_rot=100):
        moves = randint(l_rot, u_rot)
        actions = [
            ("h", 0),
            ("h", 1),
            ("v", 0),
            ("v", 1),
            ("s", 0),
            ("s", 1),
        ]

        for i in range(moves):
            a = choice(actions)
            if self.n % 2 != 0:
                j = choice([i for i in range(self.n) if i != self.n // 2])
            else:
                j = randint(0, self.n - 1)

            move = (a[0], a[1], j)
            self.twist_cube([move])

    def twist_cube(self, moves):
        for a in moves:
            j = a[2]
            if a[0] == "h":
                self.horizontal_twist(j, a[1])
            elif a[0] == "v":
                self.vertical_twist(j, a[1])
            elif a[0] == "s":
                self.side_twist(j, a[1])

    def horizontal_twist(self, row, direction):
        if row < len(self.cube[0]):
            if direction == 0:
                self.cube[LEFT][row], self.cube[FRONT][row], self.cube[RIGHT][row], self.cube[BACK][row] = (
                    self.cube[FRONT][row],
                    self.cube[RIGHT][row],
                    self.cube[BACK][row],
                    self.cube[LEFT][row]
                )
            elif direction == 1:
                self.cube[LEFT][row], self.cube[FRONT][row], self.cube[RIGHT][row], self.cube[BACK][row] = (
                    self.cube[BACK][row],
                    self.cube[LEFT][row],
                    self.cube[FRONT][row],
                    self.cube[RIGHT][row]
                )
            else:
                print("ERROR - Directions is 0 (left) or 1 (right)")
                return

            if direction == 0:  # Twist left
                if row == 0:
                    self.cube[TOP] = [list(x) for x in zip(*reversed(self.cube[TOP]))]  # Transpose top
                elif row == len(self.cube[0]) - 1:
                    self.cube[BOTTOM] = [list(x) for x in zip(*self.cube[BOTTOM])][::-1]  # Transpose bottom
            elif direction == 1:  # Twist right
                if row == 0:
                    self.cube[TOP] = [list(x) for x in zip(*self.cube[TOP])][::-1]  # Transpose top
                elif row == len(self.cube[0]) - 1:
                    self.cube[BOTTOM] = [list(x) for x in zip(*reversed(self.cube[BOTTOM]))]  # Transpose bottom
        else:
            print("ERROR Horizontal twist - please select row between 0 - %d".format(len(self.cube[0]) - 1))
            return

    def vertical_twist(self, column, direction):
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0:  # DOWN
                    self.cube[TOP][i][column], self.cube[FRONT][i][column], self.cube[BACK][-i - 1][-column - 1], \
                        self.cube[BOTTOM][i][column] = (
                        self.cube[BACK][-i - 1][-column - 1],
                        self.cube[TOP][i][column],
                        self.cube[BOTTOM][i][column],
                        self.cube[FRONT][i][column],
                    )

                elif direction == 1:  # UP
                    self.cube[TOP][i][column], self.cube[FRONT][i][column], self.cube[BACK][-i - 1][-column - 1], \
                        self.cube[BOTTOM][i][column] = (
                        self.cube[FRONT][i][column],
                        self.cube[BOTTOM][i][column],
                        self.cube[TOP][i][column],
                        self.cube[BACK][-i - 1][-column - 1],
                    )
            if direction == 0:
                if column == 0:
                    self.cube[LEFT] = [list(x) for x in zip(*reversed(self.cube[LEFT]))]
                elif column == len(self.cube[0]) - 1:
                    self.cube[RIGHT] = [list(x) for x in zip(*self.cube[RIGHT])][::-1]
            elif direction == 1:
                if column == 0:
                    self.cube[LEFT] = [list(x) for x in zip(*self.cube[LEFT])][::-1]
                elif column == len(self.cube[0]) - 1:
                    self.cube[RIGHT] = [list(x) for x in zip(*reversed(self.cube[RIGHT]))]

        else:
            print("ERROR Vertical twist - please select column between 0 - %d".format(len(self.cube[0]) - 1))
            return

    def side_twist(self, column, direction):
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0:  # Twist down
                    self.cube[0][column][i], self.cube[1][-i - 1][column], self.cube[3][i][-column - 1], \
                        self.cube[5][-column - 1][-1 - i] = (self.cube[3][i][-column - 1],
                                                             self.cube[0][column][i],
                                                             self.cube[5][-column - 1][-1 - i],
                                                             self.cube[1][-i - 1][column])
                elif direction == 1:  # Twist up
                    self.cube[0][column][i], self.cube[1][-i - 1][column], self.cube[3][i][-column - 1], \
                        self.cube[5][-column - 1][-1 - i] = (self.cube[1][-i - 1][column],
                                                             self.cube[5][-column - 1][-1 - i],
                                                             self.cube[0][column][i],
                                                             self.cube[3][i][-column - 1])
            if direction == 1:
                if column == 0:
                    self.cube[BACK] = [list(x) for x in zip(*self.cube[BACK])][::-1]
                elif column == len(self.cube[0]) - 1:
                    self.cube[FRONT] = [list(x) for x in zip(*reversed(self.cube[FRONT]))]
            elif direction == 0:
                if column == 0:
                    self.cube[BACK] = [list(x) for x in zip(*reversed(self.cube[BACK]))]
                elif column == len(self.cube[0]) - 1:
                    self.cube[FRONT] = [list(x) for x in zip(*self.cube[FRONT])][::-1]

        else:
            print("ERROR Vertical twist - please select column between 0 - %d".format(len(self.cube[0]) - 1))
            return

    def solved(self):
        for side in self.cube:
            hold = []
            check = True
            for row in side:
                if len(set(row)) == 1:
                    hold.append(row[0])

                else:
                    check = False
                    break
            if not check:
                break
            if len(set(hold)) > 1:
                check = False
                break
        return check

    def stringify(self):
        return "".join([i for r in self.cube for s in r for i in s])

    K = {
        "⬜": "U",
        "🟧": "L",
        "🟩": "F",
        "🟥": "R",
        "🟦": "B",
        "🟨": "D"
    }

    # K = {
    #        "⬜": "⬜",
    #        "🟧": "🟧",
    #        "🟩": "🟩",
    #        "🟥": "🟥",
    #        "🟦": "🟦",
    #        "🟨": "🟨"
    #    }

    def definition_string(self, sep=False):
        order = [TOP, RIGHT, FRONT, BOTTOM, LEFT, BACK]
        definition = []
        for side in order:
            for s in self.cube[side]:
                definition.append("".join([self.K[cc] for cc in s]))

        if sep:
            return " ".join(definition)
        return "".join(definition)

        # return "".join([i for r in self.cube for s in r for i in s])
        # return "".join([self.K[i] for r in self.cube for s in r for i in s])

    def show(self):
        """
        Input: None
        Description: Show the rubiks cube
        Output: None
        """

        spacing = " " * (len(str(self.cube[0][0])) + 2)
        l1 = '\n'.join(spacing + str(c) for c in self.cube[TOP])
        l2 = '\n'.join(' '.join(str(self.cube[i][j]) for i in range(1, 5)) for j in range(len(self.cube[0])))
        l3 = '\n'.join(spacing + str(c) for c in self.cube[BOTTOM])
        print("{}\n\n{}\n\n{}".format(l1, l2, l3))

    def solve_from_algorithm(self, algorithm):
        ms = algorithm.split(" ")

        for m in ms:
            move = annotation_to_move(m)
            self.twist_cube(move)



if __name__ == '__main__':
    state = """
    ⬜⬜⬜
    ⬜⬜⬜
    ⬜⬜⬜
    🟧🟧🟧
    🟧🟧🟧
    🟧🟧🟧
    🟩🟩🟩
    🟩🟩🟩
    🟩🟩🟩
    🟥🟥🟥
    🟥🟥🟥
    🟥🟥🟥
    🟦🟦🟦
    🟦🟦🟦
    🟦🟦🟦
    🟨🟨🟨
    🟨🟨🟨
    🟨🟨🟨
    """
    c = Cube(state="".join(state.split()))
