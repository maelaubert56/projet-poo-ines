from PlanetTk import PlanetTk
from Element import Element
import random

from Snake import Snake

class SnakeGame:
    """Snake game class"""    
    DIRECTIONS = {
        'Up': (0, -1),
        'Down': (0, 1),
        'Left': (-1, 0),
        'Right': (1, 0)
    }
    
    COLORS = {
        'head': 'green',
        'body': 'lightgreen',
        'food': 'white',
        'dead_head': 'gray',
        'dead_body': 'lightgray'
    }

    def __init__(self, latitude_cells_count, longitude_cells_count):
        self.__planet = PlanetTk(
            root=None,
            latitude_cells_count=latitude_cells_count,
            longitude_cells_count=longitude_cells_count,
            authorized_classes=[Snake],  # Supprimer Human
            cell_size=20
        )
        self.__is_running = False
        self.__score = 0
        self.__snake_segments = []
        self.__food_position = None
        self.__game_over = False
        self.__direction = 'Right'  # Ajout de la direction comme attribut
        self.__initialize_game()

    def get_grid(self):
        """Return the underlying PlanetAlpha grid object."""
        return self.__planet._PlanetTk__planetAlpha
    
    def __initialize_game(self):
        """Initialize snake with head and body segments"""
        # Place snake in the middle
        start_x = self.__planet._PlanetTk__longitude_cells_count // 4
        start_y = self.__planet._PlanetTk__latitude_cells_count // 2
        
        # Create head
        head_pos = start_y * self.__planet._PlanetTk__longitude_cells_count + start_x
        head = Snake(is_head=True)
        self.__planet.born(head_pos, head)
        self.__snake_segments.append(head_pos)
        
        # Create body
        for i in range(1, 3):
            pos = start_y * self.__planet._PlanetTk__longitude_cells_count + (start_x - i)
            self.__snake_segments.append(pos)
            self.__planet.born(pos, Snake())
        
        self.__place_food()

    def __place_food(self):
        """Place food in random empty cell"""
        grid = self.__planet.get_grid()
        while True:
            pos = random.randint(0, 
                               self.__planet._PlanetTk__latitude_cells_count * 
                               self.__planet._PlanetTk__longitude_cells_count - 1)
            if not isinstance(grid.get_cell(pos), Element):
                self.__food_position = pos
                self.__planet.born(pos, Snake(is_food=True))  # Utiliser Snake avec is_food=True
                break

    def toggle_running(self):
        """Toggle snake movement state with spacebar"""
        self.__is_running = not self.__is_running
        return self.__is_running

    def rotate_left(self):
        """Rotate snake 90 degrees left"""
        directions = ['Up', 'Left', 'Down', 'Right']
        current_idx = directions.index(self.__direction)
        self.__direction = directions[(current_idx + 1) % 4]
        # Mettre à jour la direction de la tête
        head = self.__planet._PlanetTk__planetAlpha.get_cell(self.__snake_segments[0])
        head.direction = self.__direction

    def rotate_right(self):
        """Rotate snake 90 degrees right"""
        directions = ['Up', 'Right', 'Down', 'Left']
        current_idx = directions.index(self.__direction)
        self.__direction = directions[(current_idx + 1) % 4]
        # Mettre à jour la direction de la tête
        head = self.__planet._PlanetTk__planetAlpha.get_cell(self.__snake_segments[0])
        head.direction = self.__direction

    def set_direction(self, new_direction):
        """Set snake direction directly, preventing 180° turns"""
        # Prevent 180° turns
        opposite_directions = {
            'Left': 'Right',
            'Right': 'Left',
            'Up': 'Down',
            'Down': 'Up'
        }
        
        # Don't allow turning back on itself
        if opposite_directions.get(new_direction) != self.__direction:
            self.__direction = new_direction
            head = self.__planet._PlanetTk__planetAlpha.get_cell(self.__snake_segments[0])
            head.direction = new_direction

    def step(self):
        """Move snake by moving tail to new head position"""
        if not self.__is_running or self.__game_over:
            return False

        dx, dy = self.DIRECTIONS[self.__direction]
        head_pos = self.__snake_segments[0]
        head_x = head_pos % self.__planet._PlanetTk__longitude_cells_count
        head_y = head_pos // self.__planet._PlanetTk__longitude_cells_count
        
        new_x = head_x + dx
        new_y = head_y + dy
        
        # Check collisions
        if (new_x < 0 or new_x >= self.__planet._PlanetTk__longitude_cells_count or
            new_y < 0 or new_y >= self.__planet._PlanetTk__latitude_cells_count):
            self.__game_over = True
            self.__kill_snake()
            return False
            
        new_head = new_y * self.__planet._PlanetTk__longitude_cells_count + new_x
        
        if new_head in self.__snake_segments[:-1]:  # Exclude tail from collision check
            self.__game_over = True
            self.__kill_snake()
            return False
            
        # Convert current head to body before creating new head
        current_head = self.__planet._PlanetTk__planetAlpha.get_cell(self.__snake_segments[0])
        current_head.is_head = False
        
        if new_head == self.__food_position:
            # Delete food first
            self.__planet.die(self.__food_position)
            # Grow snake
            self.__score += 1
            self.__snake_segments.insert(0, new_head)
            self.__planet.born(new_head, Snake(is_head=True))
            self.__place_food()
        else:
            # Move tail to new head position
            tail = self.__snake_segments.pop()
            self.__planet.die(tail)
            self.__snake_segments.insert(0, new_head)
            self.__planet.born(new_head, Snake(is_head=True))
            
        return True

    def __kill_snake(self):
        """Change snake appearance to dead state"""
        for segment in self.__snake_segments:
            current_snake = self.__planet._PlanetTk__planetAlpha.get_cell(segment)
            # Créer un nouveau serpent mort avec les mêmes propriétés et direction
            dead_snake = Snake(
                direction=current_snake.direction,
                is_head=current_snake.is_head,
                is_dead=True
            )
            # Remplacer le segment vivant par le segment mort
            self.__planet.die(segment)
            self.__planet.born(segment, dead_snake)

    def get_score(self):
        """Return current score"""
        return self.__score

    def is_game_over(self):
        """Return game over state"""
        return self.__game_over

    def reset(self):
        """Reset the game to initial state"""
        # Clear grid
        for cell in range(self.__planet._PlanetTk__latitude_cells_count * 
                         self.__planet._PlanetTk__longitude_cells_count):
            self.__planet.die(cell)
            
        # Reset variables
        self.__score = 0
        self.__direction = 'Right'
        self.__snake_segments = []
        self.__food_position = None
        self.__game_over = False
        
        # Initialize new game
        self.__initialize_game()

    def handle_game_over(self):
        """Handle game over state and offer restart"""
        if self.__game_over:
            return True
        return False
