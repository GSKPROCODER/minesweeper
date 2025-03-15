import tkinter as tk
from tkinter import messagebox, filedialog
import random
import time
import json


class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.master.geometry("500x500")
        self.master.resizable(False, False)

        # Set up default game variables
        self.difficulty = 'Easy'
        self.grid_size = 8
        self.num_mines = 10
        self.mines = []
        self.buttons = []
        self.revealed = set()
        self.start_time = None
        self.timer_running = False
        self.game_over = False
        self.dark_mode = False

        # Initialize the game UI
        self.create_widgets()
        self.create_game()

    def create_widgets(self):
        """ Create UI components like buttons, menu, and timer """
        self.timer_label = tk.Label(self.master, text="Time: 0", font=("Arial", 12))
        self.timer_label.grid(row=0, column=0, columnspan=8)

        # Menu bar setup
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Game", menu=self.game_menu)
        self.game_menu.add_command(label="New Game", command=self.new_game)
        self.game_menu.add_command(label="Save Game", command=self.save_game)
        self.game_menu.add_command(label="Load Game", command=self.load_game)
        self.game_menu.add_separator()
        self.game_menu.add_command(label="Exit", command=self.master.quit)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Easy", command=lambda: self.set_difficulty('Easy'))
        self.settings_menu.add_command(label="Medium", command=lambda: self.set_difficulty('Medium'))
        self.settings_menu.add_command(label="Hard", command=lambda: self.set_difficulty('Hard'))
        self.settings_menu.add_command(label="Dark Mode", command=self.toggle_dark_mode)

    def create_game(self):
        """ Set up the grid and mines """
        self.revealed = set()
        self.buttons = []

        # Create grid of buttons
        for row in range(self.grid_size):
            row_buttons = []
            for col in range(self.grid_size):
                button = tk.Button(self.master, width=4, height=2, font=("Arial", 12), relief=tk.RAISED,
                                   command=lambda r=row, c=col: self.reveal_cell(r, c))
                button.grid(row=row + 1, column=col, padx=3, pady=3)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        # Place mines randomly
        self.mines = []
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if (row, col) not in self.mines:
                self.mines.append((row, col))

        # Start the timer when the game begins
        self.start_time = time.time()

    def reveal_cell(self, row, col):
        """ Reveal a cell when clicked """
        if self.game_over or (row, col) in self.revealed:
            return

        self.revealed.add((row, col))
        if (row, col) in self.mines:
            self.game_over = True
            self.show_game_over("Game Over! You hit a mine!")
            return

        nearby_mines = self.count_nearby_mines(row, col)
        button = self.buttons[row][col]
        button.config(text=str(nearby_mines) if nearby_mines > 0 else '', relief=tk.SUNKEN, state=tk.DISABLED)

        # Reveal adjacent cells if no mines nearby
        if nearby_mines == 0:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.grid_size and 0 <= c < self.grid_size and (r, c) not in self.revealed:
                        self.reveal_cell(r, c)

        # Check win condition
        if len(self.revealed) == self.grid_size ** 2 - self.num_mines:
            self.game_over = True
            self.show_game_over("Congratulations! You win!")

        # Update the timer
        self.update_timer()

    def count_nearby_mines(self, row, col):
        """ Count how many mines are nearby """
        nearby_mines = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.grid_size and 0 <= c < self.grid_size and (r, c) in self.mines:
                    nearby_mines += 1
        return nearby_mines

    def update_timer(self):
        """ Update the timer during the game """
        if self.game_over:
            return
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}")

    def show_game_over(self, message):
        """ Show a message box when the game ends """
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = self.buttons[row][col]
                button.config(state=tk.DISABLED)
        messagebox.showinfo("Game Over", message)

    def new_game(self):
        """ Start a new game with the selected difficulty """
        self.game_over = False
        self.start_time = None
        self.revealed = set()

        # Reset all buttons
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = self.buttons[row][col]
                button.config(text="", relief=tk.RAISED, state=tk.NORMAL)

        self.create_game()

    def save_game(self):
        """ Save the current game state to a file chosen by the user """
        # Open a file dialog to select save location
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return  # If no file was selected, do nothing

        # Save game state to the selected file
        game_state = {
            'grid_size': self.grid_size,
            'num_mines': self.num_mines,
            'revealed': list(self.revealed),
            'mines': self.mines
        }
        with open(file_path, "w") as file:
            json.dump(game_state, file)
        messagebox.showinfo("Saved", "Game saved successfully!")

    def load_game(self):
        """ Load a saved game file selected by the user """
        # Open a file dialog to select the saved game file
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return  # If no file was selected, do nothing

        # Load the game state from the selected file
        try:
            with open(file_path, "r") as file:
                game_state = json.load(file)

            # Set the grid size and number of mines
            self.grid_size = game_state['grid_size']
            self.num_mines = game_state['num_mines']
            self.mines = game_state['mines']
            self.revealed = set(tuple(cell) for cell in game_state['revealed'])

            # Recreate the game UI
            self.create_game()

            # Reveal the cells that were previously revealed
            for row, col in self.revealed:
                self.reveal_cell(row, col)

            messagebox.showinfo("Loaded", "Game loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game: {e}")

    def set_difficulty(self, difficulty):
        """ Set the difficulty of the game """
        if difficulty == 'Easy':
            self.grid_size = 8
            self.num_mines = 10
        elif difficulty == 'Medium':
            self.grid_size = 16
            self.num_mines = 40
        elif difficulty == 'Hard':
            self.grid_size = 24
            self.num_mines = 99
        self.difficulty = difficulty
        self.new_game()

    def toggle_dark_mode(self):
        """ Toggle dark mode for the UI """
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.master.config(bg='black')
            self.timer_label.config(bg='black', fg='white')
            for row in self.buttons:
                for button in row:
                    button.config(bg='gray', fg='white')
        else:
            self.master.config(bg='white')
            self.timer_label.config(bg='white', fg='black')
            for row in self.buttons:
                for button in row:
                    button.config(bg='lightgray', fg='black')


if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()