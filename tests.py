import unittest

from cube import Cube


class TestCube(unittest.TestCase):
    def test_cube_init(self):
        s = "⬜⬜⬜⬜🟧🟧🟧🟧🟩🟩🟩🟩🟥🟥🟥🟥🟦🟦🟦🟦🟨🟨🟨🟨"
        cube = Cube(state=s)
        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["⬜", "⬜"]
                ],
                [

                    ["🟧", "🟧"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟥", "🟥"],
                    ["🟥", "🟥"],
                ],
                [

                    ["🟦", "🟦"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟨", "🟨"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )
        cube = Cube(n=2)
        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["⬜", "⬜"]
                ],
                [

                    ["🟧", "🟧"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟥", "🟥"],
                    ["🟥", "🟥"],
                ],
                [

                    ["🟦", "🟦"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟨", "🟨"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )

    def test_horizontal_twist(self):
        cube = Cube(n=2)
        cube.horizontal_twist(1, 0)
        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["⬜", "⬜"]
                ],
                [

                    ["🟧", "🟧"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟥", "🟥"],
                ],
                [

                    ["🟥", "🟥"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟦", "🟦"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟨", "🟨"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )
        cube.horizontal_twist(1,1)
        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["⬜", "⬜"]
                ],
                [

                    ["🟧", "🟧"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟥", "🟥"],
                    ["🟥", "🟥"],
                ],
                [

                    ["🟦", "🟦"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟨", "🟨"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )

    def test_vertical_twist(self):
        cube = Cube(n=2)
        cube.vertical_twist(1, 0)
        self.assertEquals(
            [
                [
                    ["⬜", "🟦"],
                    ["⬜", "🟦"],
                ],
                [

                    ["🟧", "🟧"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟩", "⬜"],
                    ["🟩", "⬜"]
                ],
                [

                    ["🟥", "🟥"],
                    ["🟥", "🟥"],
                ],
                [
                    ["🟨", "🟦"],
                    ["🟨", "🟦"]
                ],
                [

                    ["🟨", "🟩"],
                    ["🟨", "🟩"],
                ],
            ],
            cube.cube
        )
        cube.vertical_twist(1,1)
        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["⬜", "⬜"]
                ],
                [

                    ["🟧", "🟧"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟥", "🟥"],
                    ["🟥", "🟥"],
                ],
                [

                    ["🟦", "🟦"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟨", "🟨"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )


    def test_side_twist(self):
        cube = Cube(n=2)
        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["⬜", "⬜"]
                ],
                [

                    ["🟧", "🟧"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟥", "🟥"],
                    ["🟥", "🟥"],
                ],
                [

                    ["🟦", "🟦"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟨", "🟨"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )
        cube.side_twist(1,0)
        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["🟥", "🟥"],

                ],
                [

                    ["🟧", "⬜"],
                    ["🟧", "⬜"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟨", "🟥"],
                    ["🟨", "🟥"],

                ],
                [

                    ["🟦", "🟦"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟧", "🟧"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )
        assert not cube.solved()
        cube.side_twist(1,1)
        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["⬜", "⬜"]
                ],
                [

                    ["🟧", "🟧"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟥", "🟥"],
                    ["🟥", "🟥"],
                ],
                [

                    ["🟦", "🟦"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟨", "🟨"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )
        assert cube.solved()


    def test_forwards_and_backwards_twists(self):
        cube = Cube(n=2)
        cube.horizontal_twist(1,0)
        cube.vertical_twist(1,0)
        cube.side_twist(1,1)
        cube.side_twist(0,1)
        cube.side_twist(0,1)
        cube.show()
        cube.side_twist(0,0)
        cube.side_twist(0,0)
        cube.side_twist(1,0)
        cube.vertical_twist(1,1)
        cube.horizontal_twist(0,0)
        cube.horizontal_twist(0,1)
        cube.horizontal_twist(1,1)

        self.assertEquals(
            [
                [
                    ["⬜", "⬜"],
                    ["⬜", "⬜"]
                ],
                [

                    ["🟧", "🟧"],
                    ["🟧", "🟧"],
                ],
                [

                    ["🟩", "🟩"],
                    ["🟩", "🟩"],
                ],
                [

                    ["🟥", "🟥"],
                    ["🟥", "🟥"],
                ],
                [

                    ["🟦", "🟦"],
                    ["🟦", "🟦"],
                ],
                [

                    ["🟨", "🟨"],
                    ["🟨", "🟨"],
                ],
            ],
            cube.cube
        )
        print("===========SOLVED================")
        assert cube.solved()
        cube.show()
if __name__ == '__main__':
    unittest.main()
