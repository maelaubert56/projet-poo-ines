from PlanetTk import PlanetTk
from Human import Human
import random

class Conway:
    """
    Implementation of Conway's Game of Life with aging Humans.
    
    This class manages the game grid and rules, including:
    - Classic Conway rules (birth with 3 neighbors, survival with 2-3)
    - Aging mechanism for Humans
    - Natural death probability based on age
    """
    def __init__(self, latitude_cells_count, longitude_cells_count):
        self.__planet = PlanetTk(
            root=None,
            latitude_cells_count=latitude_cells_count,
            longitude_cells_count=longitude_cells_count,
            authorized_classes=[Human],
            cell_size=20
        )
        self.__step_count = 0

    def get_grid(self):
        """Return the underlying PlanetAlpha grid object."""
        print("hello")
        return self.__planet.get_grid()

    def step(self):
        """
        Execute one step of Conway's Game of Life.
        
        For each cell:
        1. Age existing Humans
        2. Check for natural death based on age
        3. Apply Conway's rules:
           - Birth: Dead cell with exactly 3 neighbors becomes alive
           - Survival: Live cell with 2-3 neighbors survives
           - Death: All other live cells die
        """
        self.__step_count += 1
        changes = []
        grid = self.__planet.get_grid()
        
        # Check each cell
        for cell in range(self.__planet._PlanetTk__latitude_cells_count * self.__planet._PlanetTk__longitude_cells_count):
            cell_content = grid.get_cell(cell)
            if isinstance(cell_content, Human):
                # Age the human
                cell_content.ageing()
                # Check for natural death
                if cell_content.get_age() > Human.LIFE_EXPECTANCY:
                    death_chance = (cell_content.get_age() - Human.LIFE_EXPECTANCY) / 100
                    if random.random() < death_chance:
                        changes.append((cell, 'die'))
                        continue

            neighbors = self.__count_live_neighbors(cell)
            current_state = isinstance(cell_content, Human)

            # Apply rules
            if current_state:
                if neighbors < 2 or neighbors > 3:
                    changes.append((cell, 'die'))
            else:
                if neighbors == 3:
                    changes.append((cell, 'born'))

        # Apply changes
        for cell, action in changes:
            if action == 'born':
                self.__planet.born(cell, Human(['Conway'], 'Being', 'XX', 'Hello'))
            else:
                self.__planet.die(cell)

    def __count_live_neighbors(self, cell):
        """
        Count the number of living Human neighbors for a given cell.
        
        Args:
            cell (int): Cell number to check neighbors for
            
        Returns:
            int: Number of living Human neighbors (0-8)
        """
        count = 0
        row, col = cell // self.__planet._PlanetTk__longitude_cells_count, cell % self.__planet._PlanetTk__longitude_cells_count
        grid = self.__planet.get_grid()
        
        # Check all 8 neighboring cells
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                # Calculate new position without wrapping
                new_row = row + dx
                new_col = col + dy
                
                # Skip if outside grid boundaries
                if (new_row < 0 or 
                    new_row >= self.__planet._PlanetTk__latitude_cells_count or 
                    new_col < 0 or 
                    new_col >= self.__planet._PlanetTk__longitude_cells_count):
                    continue
                
                neighbor_cell = new_row * self.__planet._PlanetTk__longitude_cells_count + new_col
                if isinstance(grid.get_cell(neighbor_cell), Human):
                    count += 1
        
        return count

    def get_step_count(self):
        """Return the current step count of the simulation."""
        return self.__step_count

    def reset(self):
        """Reset the grid to empty state and step count to 0."""
        for cell in range(self.__planet._PlanetTk__latitude_cells_count * self.__planet._PlanetTk__longitude_cells_count):
            self.__planet.die(cell)
        self.__step_count = 0
