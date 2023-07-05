import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import random


class SudokuBoard:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]

    def print_board(self):
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")

            for j in range(len(self.board[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j)

        return None

    def gen(self):
        pn = list(range(1, 10))
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if self.board[row][col] == 0:
                random.shuffle(pn)
                for num in pn:
                    if self.safe_place(num, row, col):
                        self.board[row][col] = num

                        if not self.find_empty():
                            return True

                        if self.gen():
                            return True

                break

        self.board[row][col] = 0
        return False

    def safe_place(self, num, row, col):
        for i in range(9):
            if self.board[row][i] == num:
                return False

        for j in range(9):
            if self.board[j][col] == num:
                return False
        startR = (row // 3) * 3
        startC = (col // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[startR + i][startC + j] == num:
                    return False
        return True


class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def solve(self):
        find = self.board.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if self.board.safe_place(num, row, col):
                self.board.board[row][col] = num

                if self.solve():
                    return True

                self.board.board[row][col] = 0

        return False


from tkinter import messagebox


class Validation:
    def __init__(self, board):
        self.board = board

    def check_range(self):
        for i in range(9):
            for j in range(9):
                val = int(self.board[i][j])
                if val < 0 or val > 9:
                    return False
        return True

    def check_duplicates(self):
        for i in range(9):
            row_values = []
            column_values = []
            for j in range(9):
                val = self.board[i][j]
                if val != 0:
                    if val in row_values:
                        return True
                    row_values.append(val)

                val = self.board[j][i]
                if val != 0:
                    if val in column_values:
                        return True
                    column_values.append(val)

        return False

    def is_valid(self):
        if not self.check_range():
            return False

        if self.check_duplicates():
            messagebox.showinfo("Duplicate Values", "The Sudoku board contains duplicate values in rows or columns.")
            return False

        return True


class Remove:

    @staticmethod
    def remove(board, dif):
        n = 0
        if dif == "easy":
            n = 30
        if dif == "medium":
            n = 40
        if dif == "difficult":
            n = 50
        solver = SudokuSolver(board)
        solver.solve()
        pn = list(range(0, 81))
        x = random.sample(pn, n)
        x = [(i // 9, i % 9) for i in x]
        for v in x:
            board.board[v[0]][v[1]] = 0
        board.print_board()
        return board.board


class SudokuGUI:
    Buttons = [[0] * 9 for i in range(9)]

    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.master.geometry("550x540")
        self.master.resizable(0, 0)
        self.board = [[0] * 9 for i in range(9)]

        self.btn_frame = tk.Frame(master)
        self.btn_frame.config(background="black")
        self.btn_frame.pack()

        for rows in range(9):
            for columns in range(9):
                btn = tk.Entry(
                    self.btn_frame,
                    font=("Times New Roman", 18),
                    bg="black",
                    fg="white",
                    width=3,
                    highlightbackground="black",
                    highlightcolor="white",
                    highlightthickness=2,
                )
                btn.grid(row=rows, column=columns)
                btn.bind("<Enter>", lambda event, b=btn: b.config(bg="darkgray"))
                btn.bind("<Leave>", lambda event, b=btn: b.config(bg="black"))
                self.Buttons[rows][columns] = btn

        self.menu_frame = tk.Frame(master)
        self.menu_frame.config(background="black")
        self.menu_frame.pack()

        cb = tk.Button(
            self.menu_frame,
            text="create",
            command=self.fill_grid,
            bg="black",
            fg="white",
            highlightbackground="black",
            highlightcolor="white",
            highlightthickness=2,
        )
        chb = tk.Button(
            self.menu_frame,
            text="check",
            bg="black",
            fg="white",
            highlightbackground="black",
            highlightcolor="white",
            highlightthickness=2,
            command=self.check

        )
        sb = tk.Button(
            self.menu_frame,
            text="solve",
            bg="black",
            fg="white",
            highlightbackground="black",
            highlightcolor="white",
            highlightthickness=2,
            command=self.solveit
        )

        lb = tk.Button(
            self.menu_frame,
            text="load",
            bg="black",
            fg="white",
            highlightbackground="black",
            highlightcolor="white",
            highlightthickness=2,
            command=self.load_files
        )
        clear = tk.Button(
            self.menu_frame,
            text="clear",
            bg="black",
            fg="white",
            highlightbackground="black",
            highlightcolor="white",
            highlightthickness=2,
            command=self.cleartable
        )

        cb.pack(pady=1, ipadx=1000)
        chb.pack(pady=1, ipadx=1000)
        sb.pack(pady=1, ipadx=1000)
        lb.pack(pady=1, ipadx=1000)
        clear.pack(pady=1, ipadx=1000)

        self.btn_on_click = BtnOnClick()

        common_bg = '#' + ''.join([hex(x)[2:].zfill(2) for x in (181, 26, 18)])  # RGB in dec

        easy = tk.Radiobutton(
            self.menu_frame,
            text="Easy",
            value="easy",
            bg="black",
            fg="white",
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
            variable=self.btn_on_click.selected_value,
            selectcolor=common_bg
        )
        easy.pack(side="left", padx=50)
        easy.bind("<Enter>", lambda event: easy.config(bg="darkgray"))
        easy.bind("<Leave>", lambda event: easy.config(bg="black"))

        medium = tk.Radiobutton(
            self.menu_frame,
            text="Medium",
            value="medium",
            bg="black",
            fg="white",
            highlightbackground="black",
            highlightcolor="white",
            highlightthickness=2,
            variable=self.btn_on_click.selected_value,
            selectcolor=common_bg
        )
        medium.pack(side="left", padx=50)
        medium.bind("<Enter>", lambda event: medium.config(bg="darkgray"))
        medium.bind("<Leave>", lambda event: medium.config(bg="black"))

        difficult = tk.Radiobutton(
            self.menu_frame,
            text="Difficult",
            value="difficult",
            bg="black",
            fg="white",
            highlightbackground="black",
            highlightcolor="white",
            highlightthickness=2,
            variable=self.btn_on_click.selected_value,
            selectcolor=common_bg
        )
        difficult.pack(side="left", padx=50)
        difficult.bind("<Enter>", lambda event: difficult.config(bg="darkgray"))
        difficult.bind("<Leave>", lambda event: difficult.config(bg="black"))

    def fill_grid(self):
        self.cleartable()
        self.generate()
        for i in range(9):
            for j in range(9):
                v = self.board[i][j]
                btn = self.Buttons[i][j]

                btn.delete(0, "end")
                btn.insert(0, str(v))

                if v != 0:
                    btn.config(disabledbackground="#292828", disabledforeground="white")
                    btn.config(state=tk.DISABLED)
                else:
                    btn.config(disabledbackground="black", disabledforeground="white")
                    btn.config(state=tk.NORMAL)

    def generate(self):
        self.sb = SudokuBoard()

        r = Remove()
        difficulty = self.btn_on_click.selected_value.get()
        if difficulty == "":
            difficulty = "easy"
        self.board = r.remove(self.sb, difficulty)

    def solveit(self):
        validator = Validation(self.sb.board)
        if validator.check_duplicates():
            messagebox.showinfo("Invalid Sudoku", "The Sudoku puzzle contains duplicate values.")
            return
        solver = SudokuSolver(self.sb)
        if solver.solve():
            self.board = self.sb.board
            for i in range(9):
                for j in range(9):
                    self.Buttons[i][j].delete(0, tk.END)
                    self.Buttons[i][j].insert(0, str(self.board[i][j]))
        else:
            messagebox.showinfo("Unsolvable Sudoku", "The Sudoku puzzle is unsolvable.")

    def check(self):
        inputs = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.Buttons[i][j].get()
                row.append(val)
            inputs.append(row)

        validator = Validation(inputs)
        if validator.is_valid():
            messagebox.showinfo("Result", "Congratulations! Your solution is correct.")
        else:
            messagebox.showinfo("Result", "Sorry, your solution is incorrect.")

    def update_board(self, elmnts):
        for i in range(9):
            for j in range(9):
                value = elmnts[i][j]
                try:
                    value = int(value)
                except ValueError:
                    value = ""
                self.Buttons[i][j].delete(0, "end")
                self.Buttons[i][j].insert(0, str(value))

    def cleartable(self):
        for i in range(9):
            for j in range(9):
                btn = self.Buttons[i][j]
                btn.config(state=tk.NORMAL)
                btn.delete(0, tk.END)
                btn.config(background="black", foreground="white")

    def load_files(self):
        file_loc = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if file_loc:
            try:
                with open(file_loc, "r") as file:
                    lines = file.readlines()
                elmnts = []
                for line in lines:
                    row = [int(num) for num in line.strip().split(",")]
                    elmnts.append(row)

                self.sb = SudokuBoard()
                self.sb.board = elmnts

                validator = Validation(self.sb.board)
                if not validator.is_valid():
                    messagebox.showinfo("Invalid Sudoku", "The Sudoku puzzle in the file is not valid.")
                    return
                self.cleartable()
                for i in range(9):
                    for j in range(9):
                        v = self.sb.board[i][j]
                        btn = self.Buttons[i][j]
                        self.Buttons[i][j].delete(0, 'end')
                        self.Buttons[i][j].insert(0, str(v))
                        if v != 0:
                            btn.config(disabledbackground="#292828", disabledforeground="white")
                            btn.config(state=tk.DISABLED)
                        else:
                            btn.config(disabledbackground="black", disabledforeground="white")
                            btn.config(state=tk.NORMAL)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")


class BtnOnClick:
    def __init__(self):
        self.selected_value = tk.StringVar()


root = tk.Tk()
root.config(background="black")
sudoku_gui = SudokuGUI(root)
root.mainloop()
