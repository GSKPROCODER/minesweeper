import tkinter as tk
import random
from tkinter import messagebox

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = {}
        self.mine_positions = set()
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)
        
        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.frame, width=2, command=lambda r=r, c=c: self.on_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[(r, c)] = button

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            self.mine_positions.add((r, c))

    def on_click(self, r, c):
        if (r, c) in self.mine_positions:
            self.buttons[(r, c)].config(text='*', bg='red')
            self.game_over()
        else:
            self.reveal(r, c)
            if self.check_win():
                self.win()

    def reveal(self, r, c):
        if (r, c) in self.mine_positions or self.buttons[(r, c)]['state'] == 'disabled':
            return
        self.buttons[(r, c)].config(state='disabled')
        mines_around = self.count_mines_around(r, c)
        if mines_around > 0:
            self.buttons[(r, c)].config(text=str(mines_around))
        else:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r + dr < self.rows and 0 <= c + dc < self.cols:
                        self.reveal(r + dr, c + dc)

    def count_mines_around(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in self.mine_positions:
                    count += 1
        return count

    def game_over(self):
        for (r, c) in self.mine_positions:
            self.buttons[(r, c)].config(text='*', bg='red')
        for button in self.buttons.values():
            button.config(state='disabled')
        messagebox.showinfo("Game Over", "You hit a mine! Game Over.")

    def check_win(self):
        for (r, c), button in self.buttons.items():
            if (r, c) not in self.mine_positions and button['state'] != 'disabled':
                return False
        return True

    def win(self):
        messagebox.showinfo("Congratulations", "You have won the game!")
        for button in self.buttons.values():
            button.config(state='disabled')

    def new_game(self):
        self.mine_positions.clear()
        for button in self.buttons.values():
            button.destroy()
        self.buttons.clear()
        self.create_widgets()
        self.place_mines()

    def show_about(self):
        messagebox.showinfo("About", "Minesweeper Game\nCreated by GitHub Copilot")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()