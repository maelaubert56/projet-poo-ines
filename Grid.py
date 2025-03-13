import random


class Grid:

    def __init__(self, grid_init):
        """ Classe 'Grid' avec 3 attributs :
                - 'grid' : initialisé avec le paramètre 'grid_init'
                - 'lines_count' : initialisé avec le nombre de lignes de 'grid_init'
                - columns_count' : initialisé avec le nombre de colonnes de 'grid_init'."""
        self.__grid = grid_init
        self.__lines_count = len(grid_init)
        self.__columns_count = len(grid_init[0]) if len(grid_init) else 0

    def get_grid(self):
        return self.__grid

    def get_lines_count(self):
        return self.__lines_count

    def get_columns_count(self):
        return self.__columns_count

    def fill_random(self, values):
        """ Rempli la grille de valeurs aléatoires de la liste 'values'"""
        self.__grid = [[random.choice(values)
                        for _ in range(self.__columns_count)]
                       for _ in range(self.__lines_count)]

    def get_line(self, line_number):
        """ Extrait la ligne numéro 'line_number' de la grille."""
        return self.__grid[line_number]

    def get_column(self, column_number):
        """ Extrait la colonne numéro 'column_number' de la grille."""
        return [line[column_number] for line in self.__grid]

    def get_diagonal(self):
        """ Extrait la diagonale de la grille."""
        diagonal_size = min(self.__lines_count, self.__columns_count)
        return [self.__grid[line_number][line_number] for line_number in range(diagonal_size)]

    def get_anti_diagonal(self):
        """ Extrait l'antidiagonale de la grille."""
        diagonal_size = min(self.__lines_count, self.__columns_count)
        return [self.__grid[line_number][self.__columns_count - line_number - 1]
                for line_number in range(diagonal_size)]

    def get_line_str(self, line_number, separator='\t'):
        """ Retourne la chaine de caractère correspondant à la concaténation des valeurs de la ligne numéro
        'line_number' de la grille. Les caractères sont séparés par le caractère 'separator'."""
        return separator.join(str(value) for value in self.__grid[line_number])

    def get_grid_str(self, separator='\t'):
        """ Retourne la chaine de caractère représentant la grille.
                Les caractères de chaque ligne sont séparés par le caractère 'separator'.
                Les lignes sont séparées par le caractère de retour à la ligne '\n'."""
        return '\n'.join(self.get_line_str(line_number, separator) for line_number in range(self.__lines_count))

    def has_equal_values(self, value):
        """ Teste si toutes les valeurs de la grille sont égales à 'value'."""
        return all([all([value == grid_value for grid_value in line]) for line in self.__grid])

    def is_square(self):
        """ Teste si la grille a le même nombre de lignes et de colonnes."""
        return self.__lines_count == self.__columns_count

    def get_count(self, value):
        """ Compte le nombre d'occurrences de 'value' dans la grille."""
        return sum(line.count(value) for line in self.__grid)

    def get_sum(self):
        """ Fait la somme de tous les éléments de la grille."""
        return sum(sum(line) for line in self.__grid)

    def get_coordinates_from_cell_number(self, cell_number):
        """ Converti un numéro de case 'cell_number' de la grille vers les coordonnées (ligne, colonne)
        correspondants."""
        return cell_number // self.__columns_count, cell_number % self.__columns_count

    def get_cell_number_from_coordinates(self, line_number, column_number):
        """ Converti les coordonnées ('line_number', 'column_number') de la grille vers le numéro de case
        correspondant."""
        return line_number * self.__columns_count + column_number

    def get_cell(self, cell_number):
        """ Extrait la valeur de la grille en position 'cell_number'."""
        line_number, column_number = self.get_coordinates_from_cell_number(cell_number)
        return self.__grid[line_number][column_number]

    def set_cell(self, cell_number, value):
        """ Positionne la valeur 'value' dans la case 'cell_number' de la grille."""
        line_number, column_number = self.get_coordinates_from_cell_number(cell_number)
        self.__grid[line_number][column_number] = value

    def get_same_value_cell_numbers(self, value):
        """ Fourni la liste des numéros des cases à valeur égale à 'value' dans la grille."""
        return [cell_number
                for cell_number in range(self.__lines_count * self.__columns_count)
                if self.get_cell(cell_number) == value]

    def get_neighbour(self, line_number, column_number, delta, is_tore=True):
        """ Retourne le voisin de la cellule ('line_number', 'column_number') de la grille. La définition de voisin
        correspond à la distance positionnelle indiquée par le 2-uplet 'delta' = (delta_ligne, delta_colonne). La case
        voisine est alors (ligne + delta_ligne, colonne + delta_colonne).
                Si 'is_tore' est à 'True' le voisin existe toujours en considérant la grille comme un tore.
                Si 'is_tore' est à 'False' retourne 'None' lorsque le voisin est hors de la grille."""
        new_line_number, new_column_number = line_number + delta[0], column_number + delta[1]
        if is_tore or 0 <= new_line_number < self.__lines_count and 0 <= new_column_number < self.__columns_count:
            return self.__grid[new_line_number % self.__lines_count][new_column_number % self.__columns_count]
        return None

    def get_neighborhood(self, line_number, column_number, deltas, is_tore=True):
        """ Retourne la liste des N voisins de la position ('lins_number', 'column_number') dans la grille correspondant
         aux N 2-uplet (delta_ligne, delta_colonne) fournis par la liste deltas.
                Si 'is_tore' est à 'True' le voisin existe toujours en considérant la grille comme un tore.
                Si 'is_tore' est à 'False' un voisin hors de la grille n'est pas considéré."""
        return [self.get_neighbour(line_number, column_number, delta, is_tore)
                for delta in deltas]

    def get_cell_neighbour_number(self, cell_number, delta, is_tore=True):
        """ Retourne le numéro de cellule voisine de la cellule 'cell_number' de la grille. La définition de
        voisin correspond à la distance positionnelle indiquée par le 2-uplet 'delta' = (delta_ligne, delta_colonne).
        La case voisine est alors (ligne + delta_ligne, colonne + delta_colonne).
                Si 'is_tore' est à 'True' le voisin existe toujours en considérant la grille comme un tore.
                Si 'is_tore' est à 'False' retourne 'None' lorsque le voisin est hors de la grille."""
        line_number, column_number = self.get_coordinates_from_cell_number(cell_number)
        line_number, column_number = line_number + delta[0], column_number + delta[1]
        if is_tore or 0 <= line_number < self.__lines_count and 0 <= column_number < self.__columns_count:
            line_number %= self.__lines_count
            column_number %= self.__columns_count
            return self.get_cell_number_from_coordinates(line_number, column_number)
        return None

    def get_cell_neighborhood_numbers(self, cell_number, deltas, is_tore=True):
        """ Retourne la liste des N cellules voisines de la position 'cell_number'
        dans la grille correspondant aux N 2-uplet (delta_ligne, delta_colonne) fournis par la liste deltas.
                Si 'is_tore' est à 'True' le voisin existe toujours en considérant la grille comme un tore.
                Si 'is_tore' est à 'False' un voisin hors de la grille n'est pas considéré."""
        res = []
        for delta in deltas:
            neighbour = self.get_cell_neighbour_number(cell_number, delta, is_tore)
            if neighbour is not None:
                res.append(neighbour)
        return sorted(res)
