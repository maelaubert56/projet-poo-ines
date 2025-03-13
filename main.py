from tkinter import Tk, Canvas
from Grid import Grid
from MyApp import MyApp

if __name__ == "__main__":

    LINES_COUNT = 40
    COLUMNS_COUNT = 40
    GRID_TEST = Grid([[0] * COLUMNS_COUNT for _ in range(LINES_COUNT)])
    GRID_TEST.fill_random([0, 1])
    CELL_SIZE = 20
    GUTTER_SIZE = 0
    MARGIN_SIZE = 10

    app = MyApp(GRID_TEST, CELL_SIZE, GUTTER_SIZE, MARGIN_SIZE)
    app.mainloop()