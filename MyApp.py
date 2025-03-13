import tkinter as tk
from tkinter import messagebox
from Conway import Conway
from Human import Human
import random

from Snake import Snake
from SnakeGame import SnakeGame

class MyApp(tk.Tk):
    """
    Main application class for the game suite, including Conway's Game of Life.
    
    Provides a graphical interface for:
    - Game selection menu
    - Game visualization
    - Game controls
    - Rules display
    """
    COLORS = {'cell_background': 'white',
              'cell_foreground': 'black',
              'grid_lines':'gray',
              'grid_text':'white',
              'widget_text': 'orange'}

    def __init__(self, grid, cell_size, gutter_size=0, margin_size=10):
        tk.Tk.__init__(self)
        self.title("My App")
        self.grid = grid
        self.cell_size = cell_size
        self.gutter_size = gutter_size
        self.margin_size = margin_size
        self.current_game = None  # Add this line
        self.draw_menu()

    def draw_menu(self):
        """Create and display the main menu with game selection buttons."""
        menubar = tk.Menu(self)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Conway", command=self.start_conway)
        game_menu.add_command(label="Turmites", command=self.start_turmites)
        game_menu.add_command(label="Snake", command=self.start_snake)
        game_menu.add_separator()
        game_menu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="Games", menu=game_menu)
        self.config(menu=menubar)

        # Create a frame for the hub
        self.f_hub = tk.Frame(self)
        self.f_hub.pack(pady=20)

        # Add buttons for each game in the hub
        self.b_conway = tk.Button(self.f_hub, text="Start Conway's Game of Life", command=self.start_conway)
        self.b_conway.pack(pady=5)
        self.b_turmites = tk.Button(self.f_hub, text="Start Turmites", command=self.start_turmites)
        self.b_turmites.pack(pady=5)
        self.b_snake = tk.Button(self.f_hub, text="Start Snake", command=self.start_snake)
        self.b_snake.pack(pady=5)
        self.b_quit = tk.Button(self.f_hub, text="Quit", command=self.quit)
        self.b_quit.pack(pady=5)

    def clear_game(self):
        """Clear the current game display"""
        if hasattr(self, 'f_hub'):
            self.f_hub.destroy()
        if hasattr(self, 'f_main'):
            self.f_main.destroy()
        
        # Create new main frame
        self.f_main = tk.Frame(self)
        self.f_main.pack()

    def setup_game(self, grid):
        """
        Initialize the game display with the given grid.
        
        Args:
            grid: Grid object implementing get_grid() method
        """
        if hasattr(grid, 'get_grid'):
            self.grid = grid.get_grid()
        else:
            self.grid = grid
            
        canvas_size = (len(self.grid.get_grid()[0]) * (self.cell_size + self.gutter_size)) + 2 * self.margin_size
        
        self.c_draw = tk.Canvas(self.f_main,
                               width=canvas_size,
                               height=canvas_size,
                               bg=self.COLORS['cell_background'])
        self.c_draw.pack()
        
        # Only bind click for Conway's Game
        if isinstance(grid, Conway):
            self.c_draw.bind('<Button-1>', self.on_canvas_click)
        
        # Replace quit button with back button
        self.b_back = tk.Button(self.f_main,
                               text='Back to Menu',
                               command=self.back_to_menu,
                               fg=self.COLORS['widget_text'])
        self.b_back.pack(pady=5)

    def back_to_menu(self):
        """Return to the main menu"""
        # Stop any ongoing game
        if hasattr(self, 'is_playing'):
            self.is_playing = False
        
        # Clear game frame
        if hasattr(self, 'f_main'):
            self.f_main.destroy()
            
        self.current_game = None  # Add this line
        
        # Redraw menu
        self.draw_menu()

    def on_canvas_click(self, event):
        """Handle canvas clicks to toggle cells"""
        # Convert click coordinates to grid cell
        clicked_x = event.x - self.margin_size
        clicked_y = event.y - self.margin_size
        
        # Calculate cell position
        col = clicked_x // (self.cell_size + self.gutter_size)
        row = clicked_y // (self.cell_size + self.gutter_size)
        
        # Ensure click is within grid bounds
        if 0 <= col < len(self.grid.get_grid()[0]) and 0 <= row < len(self.grid.get_grid()):
            # Convert to cell number
            cell_number = row * len(self.grid.get_grid()[0]) + col
            
            # Toggle cell state
            if isinstance(self.grid.get_cell(cell_number), Human):
                self.grid.die(cell_number)
            else:
                self.grid.born(cell_number, Human(['Conway'], 'Being', 'XX', 'Hello'))
            
            # Redraw grid
            self.draw_grid(True)

    def start_conway(self):
        self.clear_game()
        grid_size = len(self.grid.get_grid())
        self.conway_grid = Conway(grid_size, grid_size)
        self.current_game = 'conway'  # Add this line
        self.setup_game(self.conway_grid)
        
        # Add control frames
        controls_container = tk.Frame(self.f_main)
        controls_container.pack(side=tk.TOP, fill=tk.X, padx=5)
        
        # Left controls
        left_controls = tk.Frame(controls_container)
        left_controls.pack(side=tk.LEFT, padx=5)
        
        # Add show age toggle
        self.show_age = tk.BooleanVar(value=True)
        tk.Checkbutton(left_controls, 
                      text="Show Age", 
                      variable=self.show_age,
                      command=self.refresh_grid).pack(side=tk.LEFT, padx=2)
        
        self.is_playing = False
        self.play_button = tk.Button(left_controls, 
                                   text="Play", 
                                   command=self.toggle_autoplay)
        self.play_button.pack(side=tk.LEFT, padx=2)
        
        # Speed control
        speed_frame = tk.Frame(left_controls)
        speed_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(speed_frame, text="Delay (ms):").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="500")
        speed_entry = tk.Entry(speed_frame, 
                             textvariable=self.speed_var, 
                             width=5)
        speed_entry.pack(side=tk.LEFT, padx=2)
        
        # Center controls
        center_controls = tk.Frame(controls_container)
        center_controls.pack(side=tk.LEFT, padx=5, expand=True)
        
        tk.Button(center_controls,
                 text="Rules",
                 command=self.show_rules).pack(side=tk.LEFT, padx=2)
        
        # Right controls
        right_controls = tk.Frame(controls_container)
        right_controls.pack(side=tk.RIGHT, padx=5)
        
        tk.Button(right_controls, 
                 text="Next Step", 
                 command=lambda: [self.conway_grid.step(), self.draw_grid(True)]).pack(side=tk.LEFT, padx=2)
        
        tk.Button(right_controls, 
                 text="Reset", 
                 command=self.reset_conway).pack(side=tk.LEFT, padx=2)
        
        # Adjust random cell count for larger grid
        cell_count = (grid_size * grid_size) // 10  # 10% of cells
        for _ in range(cell_count):
            cell = random.randint(0, grid_size * grid_size - 1)
            self.grid.born(cell, Human(['Conway'], 'Being', 'XX', 'Hello'))
        
        self.draw_grid(True)

    def toggle_autoplay(self):
        self.is_playing = not self.is_playing
        self.play_button.config(text="Stop" if self.is_playing else "Play")
        if self.is_playing:
            self.auto_step()

    def auto_step(self):
        if self.is_playing:
            self.conway_grid.step()
            self.draw_grid(True)
            try:
                delay = int(self.speed_var.get())
            except ValueError:
                delay = 100
            self.after(delay, self.auto_step)

    def reset_conway(self):
        self.is_playing = False
        self.play_button.config(text="Play")
        self.conway_grid.reset()
        self.draw_grid(True)

    def start_turmites(self):
        # Add logic to start Turmites
        pass

    def start_snake(self):
        """Initialize and start Snake game"""
        self.clear_game()
        grid_size = len(self.grid.get_grid())
        self.snake_game = SnakeGame(grid_size, grid_size)
        self.current_game = 'snake'
        self.setup_game(self.snake_game)
        
        # Bind controls
        self.bind('<space>', lambda e: self.toggle_snake())
        self.bind('<Button-1>', lambda e: self.snake_game.rotate_left())
        self.bind('<Button-3>', lambda e: self.snake_game.rotate_right())
        # Add keyboard controls
        self.bind('<Left>', lambda e: self.snake_game.set_direction('Left'))
        self.bind('<Right>', lambda e: self.snake_game.set_direction('Right'))
        self.bind('<Up>', lambda e: self.snake_game.set_direction('Up'))
        self.bind('<Down>', lambda e: self.snake_game.set_direction('Down'))
        
        # Add score display
        self.score_label = tk.Label(self.f_main, 
                                  text="Score: 0",
                                  font=('Arial', 16, 'bold'))
        self.score_label.pack(side=tk.TOP, pady=5)
        
        self.draw_grid(True)

    def toggle_snake(self):
        """Toggle snake movement with spacebar"""
        if self.snake_game.toggle_running():
            self.snake_step()

    def snake_step(self):
        """Execute snake game step"""
        if self.snake_game.step():
            self.score_label.config(text=f"Score: {self.snake_game.get_score()}")
            self.draw_grid(True)
            self.after(150, self.snake_step)
        elif self.snake_game.handle_game_over():
            if messagebox.askyesno("Game Over", 
                                 f"Score: {self.snake_game.get_score()}\nVoulez-vous recommencer?"):
                self.start_snake()

    def reset_snake(self):
        """Reset snake game"""
        if hasattr(self, 'snake_game'):
            self.snake_game.reset()
            self.score_label.config(text="Score: 0")
            self.draw_grid(True)
            self.snake_step()

    def show_snake_rules(self):
        """Display snake game rules"""
        rules_window = tk.Toplevel(self)
        rules_window.title("Snake Game Rules")
        rules_window.geometry("400x300")
        
        rules_text = """Snake Game Rules:

- Use arrow keys or WASD to control the snake
- Eat food to grow and increase score
- Avoid hitting walls
- Avoid hitting yourself
- Try to get the highest score!

Controls:
- Arrow keys or WASD: Move snake
- New Game: Start a new game
"""
        
        text_widget = tk.Text(rules_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.insert("1.0", rules_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH)
        
        tk.Button(rules_window, 
                 text="Close", 
                 command=rules_window.destroy).pack(pady=5)

    def refresh_grid(self):
        """Refresh the grid display"""
        self.draw_grid(True)

    def draw_grid(self, grid_lines):
        self.c_draw.delete(tk.ALL)

        line, column = len(self.grid.get_grid()), len(self.grid.get_grid()[0])
        for cell_number in range(line * column):
            i, j = self.grid.get_coordinates_from_cell_number(cell_number)
            x = j*(self.cell_size + self.gutter_size) + self.margin_size
            y = i*(self.cell_size + self.gutter_size) + self.margin_size
            
            cell_content = self.grid.get_cell(cell_number)
            
            if grid_lines:
                if isinstance(cell_content, Snake):
                    if cell_content.is_food:
                        fill_color = SnakeGame.COLORS['food']
                        self.c_draw.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                                  outline=self.COLORS['grid_lines'],
                                                  fill=fill_color)
                        self.c_draw.create_text(x + self.cell_size/2,
                                              y + self.cell_size/2,
                                              text='🍎',
                                              fill='white',
                                              font=('Arial', int(self.cell_size/2)))
                    else:
                        # Vérifier d'abord si le serpent est mort
                        if hasattr(cell_content, 'is_dead') and cell_content.is_dead:
                            fill_color = SnakeGame.COLORS['dead_head'] if cell_content.is_head else SnakeGame.COLORS['dead_body']
                        else:
                            fill_color = SnakeGame.COLORS['head'] if cell_content.is_head else SnakeGame.COLORS['body']
                        self.c_draw.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                                  outline=self.COLORS['grid_lines'],
                                                  fill=fill_color)
                elif isinstance(cell_content, Human):
                    fill_color = self.COLORS['cell_foreground']
                    self.c_draw.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                              outline=self.COLORS['grid_lines'],
                                              fill=fill_color)
                else:
                    fill_color = self.COLORS['cell_background']
                    self.c_draw.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                              outline=self.COLORS['grid_lines'],
                                              fill=fill_color)
                
                # Draw age if enabled and cell contains Human (except food)
                if hasattr(self, 'show_age') and self.show_age.get() and isinstance(cell_content, Human) and cell_content.get_full_name() != 'Food':
                    self.c_draw.create_text(x + self.cell_size/2,
                                          y + self.cell_size/2,
                                          text=str(cell_content.get_age()),
                                          fill=self.COLORS['grid_text'])

    def show_rules(self):
        """Display a popup window with the current game's rules."""
        rules_window = tk.Toplevel(self)
        rules_window.title("Conway's Game of Life Rules")
        rules_window.geometry("400x300")
        
        rules_text = f"""Conway's Game of Life Rules:

Birth: A dead cell becomes alive if it has exactly 3 living neighbors.

Survival: A living cell survives if it has 2 or 3 living neighbors.
Otherwise, it dies of loneliness (<2) or overcrowding (>3).

Aging:
- Each human ages by 1 year at each step
- After age {Human.LIFE_EXPECTANCY}, humans have an increasing chance of natural death
- Death chance = (current_age - {Human.LIFE_EXPECTANCY})/100 per step

Controls:
- Click cells to toggle their state
- Use Play/Stop to control automatic evolution
- Adjust simulation speed with delay value
- Toggle age display with the checkbox
"""
        
        text_widget = tk.Text(rules_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.insert("1.0", rules_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH)
        
        tk.Button(rules_window, 
                 text="Close", 
                 command=rules_window.destroy).pack(pady=5)