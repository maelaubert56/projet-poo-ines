from PlanetAlpha import PlanetAlpha
import random

class PlanetTk:
    """
    Grid management class for cellular automata simulations.
    
    Handles:
    - Grid creation and management
    - Cell state changes
    - Visual properties
    - Element placement and movement
    """

    def __init__(self, root, latitude_cells_count, longitude_cells_count, authorized_classes, background_color: str='white', foreground_color: str='dark blue', gridlines_color: str='maron', cell_size: int=40, gutter_size: int=0, margin_size: int=0, show_content: bool=True, show_grid_lines: bool=True, **kw):
        """
        Initialize the grid system.
        
        Args:
            root: Parent widget
            latitude_cells_count (int): Number of rows
            longitude_cells_count (int): Number of columns
            authorized_classes (list): List of allowed element classes
            background_color (str): Background color of the grid
            foreground_color (str): Foreground color of the grid
            gridlines_color (str): Color of the grid lines
            cell_size (int): Size of each cell
            gutter_size (int): Size of the gutter between cells
            margin_size (int): Size of the margin around the grid
            show_content (bool): Whether to show the content of the cells
            show_grid_lines (bool): Whether to show the grid lines
            **kw: Additional display parameters
        """
        self.__root = root
        self.__latitude_cells_count = latitude_cells_count
        self.__longitude_cells_count = longitude_cells_count
        self.__authorized_classes = authorized_classes
        self.__background_color = background_color
        self.__foreground_color  = foreground_color
        self.__gridlines_color = gridlines_color
        self.__cell_size = cell_size
        self.__gutter_size = gutter_size
        self.__margin_size = margin_size
        self.__show_content = show_content
        self.__show_grid_lines = show_grid_lines
    
        self.__planetAlpha = PlanetAlpha(
            name="Conway's Game of Life",
            latitude_cell_count=latitude_cells_count,
            longitude_cell_count=longitude_cells_count,
            ground=0  # Using 0 as default ground state
        )

    def get_root(self):
        """
        Get the root widget.
        
        Returns:
            The root widget.
        """
        return root

    def get_background_color(self):
        """
        Get the background color of the grid.
        
        Returns:
            The background color.
        """
        return background_color

    def get_foreground_color(self):
        """
        Get the foreground color of the grid.
        
        Returns:
            The foreground color.
        """
        return foreground_color

    def born(self, cell_number, element):
        """
        Place an element in a specific cell.
        
        Args:
            cell_number (int): The cell number.
            element: The element to place.
        """
        self.__planetAlpha.born(cell_number, element)
    
    def die(self, cell_number, element = 0):
        """
        Remove an element from a specific cell.
        
        Args:
            cell_number (int): The cell number.
            element: The element to remove (default is 0).
        """
        self.__planetAlpha.die(cell_number)

    def born_randomly(self, element):
        """
        Place an element in a random cell.
        
        Args:
            element: The element to place.
        """
        self.born(random.randint(0, self.__planetAlpha.latitude_cells_count * self.__planetAlpha.longitude_cells_count -1), element)
    
    def populate(self, class_names_count):
        """
        Populate the grid with a given number of elements for each class.
        
        Args:
            class_names_count (dict): Dictionary with class names as keys and counts as values.
        """
        for i, j in class_names_count.items():
            for k in range(j):
                self.born_randomly(i())

    def move_element(self, cell_number, new_cell_number):
        """
        Move an element from one cell to another.
        
        Args:
            cell_number (int): The current cell number.
            new_cell_number (int): The new cell number.
        """
        element = self.__planetAlpha.get_cell(cell_number)
        self.die(cell_number)
        self.born(new_cell_number, element)

    def get_classes_cell_numbers(self):
        """
        Get the number of cells occupied by each class.
        
        Returns:
            dict: Dictionary with class names as keys and counts as values.
        """
        dic = {}
        for i in self.__authorized_classes:
            dic[i] = self.__planetAlpha.get_count(i)
        return dic

    def get_grid(self):
        """
        Get the grid object.
        
        Returns:
            PlanetAlpha: The grid object.
        """
        return self.__planetAlpha

    def __repr__(self):
        """
        Get the string representation of the grid.
        
        Returns:
            str: The string representation.
        """
        return self.__planetAlpha.__repr__()

    def __str__(self):
        """
        Get the string representation of the grid.
        
        Returns:
            str: The string representation.
        """
        return self.__repr__()
