from Grid import Grid
import random

class PlanetAlpha(Grid):

    NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
    NORTH_EAST, SOUTH_EAST, SOUTH_WEST, NORTH_WEST = (-1, 1), (1, 1), (1, -1), (-1, -1)
    CARDINAL_POINTS = (NORTH, EAST, SOUTH, WEST)
    WIND_ROSE = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)


    def __init__(self, name: str, latitude_cell_count, longitude_cell_count,  ground):
        grille = []
        for _ in range(latitude_cell_count):
            ligne = []
            for _ in range(longitude_cell_count):
                ligne.append(ground)
            grille.append(ligne)
            
        Grid.__init__(self, grille)

        self.__name = name
        self.__ground = ground

    def get_name(self):
        return self.__name
    
    def get_ground(self):
        return self.__ground

    def get_random_free_place(self):
        list_empty = self.get_same_value_cell_numbers(self.__ground)
        if len(list_empty) == 0:
            return -1
        return random.choice(list_empty)

    def born(self, cell_number, element):
        grille = self.get_grid()
        i,j = self.get_coordinates_from_cell_number(cell_number)
        if grille[i][j] == self.__ground:
            grille[i][j] = element
            return 1
        return 0

    def die(self, cell_number):
        grille = self.get_grid()
        (i,j) = self.get_coordinates_from_cell_number(cell_number)
        if grille[i][j] == self.__ground:
            return 0
        grille[i][j] = self.__ground
        return 1

    def __repr__(self):
        grille = self.get_grid()
        res =""
        for ligne in grille:
            res += " ".join(str(el) for el in ligne) + "\n"
        return res
