from turtle import Turtle, Screen
from itertools import cycle


class App:
    colors = ['blue', 'yellow']

    def __init__(self, master):
        self.master = master
        self.colors = iter(cycle(App.colors))

        self.turtle = Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(2)
        self.turtle.pensize(4)

        self.master.onclick(self.run_lap)

        self.go(-60, 0)
        self.turtle.color('white')
        self.turtle.write('Click to Start', font='arial 20')

    def run_lap(self, *args):
        self.turtle.clear()

        sides = self.master.numinput('N Polygon', 'Sides: ', minval=3, maxval=15)
        if sides is None:
            self.exit()
            return

        sides = int(sides)
        total_angle = 180 * (sides - 2)
        angle = total_angle / sides
        angle = 180 - angle  # reverse direction
        length = 150 - (sides * 2)
        self.go(50, -180 + ((10 - sides) * 25))  # start point

        for side in range(1, sides+1):
            if (sides % 2) and (side == sides):  # if it is the last side and the number of sides is an odd number
                self.turtle.color('gray')
            else:
                self.turtle.color(next(self.colors))

            self.turtle.left(angle)
            self.turtle.forward(length)

    def go(self, x, y):
        self.turtle.penup()
        self.turtle.goto(x=x, y=y)
        self.turtle.pendown()

    def exit(self):
        self.go(-70, 0)
        self.turtle.color('white')
        self.turtle.write('Click to Quit', font='arial 20')
        self.master.exitonclick()


if __name__ == "__main__":
    root = Screen()
    root.bgcolor('black')
    root.title('N Polygon')
    root.setup(width=700, height=700, startx=350, starty=70)

    app = App(root)
    root.mainloop()
