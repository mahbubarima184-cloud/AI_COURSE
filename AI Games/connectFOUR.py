import tkinter as tk
from tkinter import messagebox
import random, math

# === Constants ===
ROWS, COLS = 6, 7
PLAYER, AI, EMPTY = 1, 2, 0
WIN_COUNT, DEPTH = 4, 4
COLORS = {EMPTY: "#FFF8DC", PLAYER: "#FF5C58", AI: "#F9D923"}

# === Game Logic ===
def new_board(): return [[EMPTY]*COLS for _ in range(ROWS)]
def drop(b, r, c, p): b[r][c] = p
def valid(b, c): return b[0][c] == EMPTY
def get_row(b, c): return next(r for r in range(ROWS-1, -1, -1) if b[r][c] == EMPTY)
def valid_cols(b): return [c for c in range(COLS) if valid(b, c)]

def win(b, p):
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(b[r][c+i] == p for i in range(4)): return True
    for r in range(ROWS-3):
        for c in range(COLS):
            if all(b[r+i][c] == p for i in range(4)): return True
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(b[r+i][c+i] == p for i in range(4)): return True
            if all(b[r+3-i][c+i] == p for i in range(4)): return True
    return False

def score_window(w, p):
    opp = PLAYER if p == AI else AI
    return 100*w.count(p)*(w.count(p)==4) + 10*(w.count(p)==3 and w.count(EMPTY)==1) + \
           5*(w.count(p)==2 and w.count(EMPTY)==2) - 80*(w.count(opp)==3 and w.count(EMPTY)==1)

def score(b, p):
    s = [b[r][COLS//2] for r in range(ROWS)].count(p) * 3
    for r in range(ROWS):
        for c in range(COLS-3): s += score_window(b[r][c:c+4], p)
    for c in range(COLS):
        for r in range(ROWS-3): s += score_window([b[r+i][c] for i in range(4)], p)
    for r in range(ROWS-3):
        for c in range(COLS-3):
            s += score_window([b[r+i][c+i] for i in range(4)], p)
            s += score_window([b[r+3-i][c+i] for i in range(4)], p)
    return s

def minimax(b, d, a, bta, maxing):
    if win(b, PLAYER): return None, -math.inf
    if win(b, AI): return None, math.inf
    if d == 0 or not valid_cols(b): return None, score(b, AI)
    best, val = random.choice(valid_cols(b)), -math.inf if maxing else math.inf
    for c in valid_cols(b):
        temp = [r[:] for r in b]
        drop(temp, get_row(temp, c), c, AI if maxing else PLAYER)
        _, s = minimax(temp, d-1, a, bta, not maxing)
        if maxing:
            if s > val: val, best = s, c
            a = max(a, val)
        else:
            if s < val: val, best = s, c
            bta = min(bta, val)
        if a >= bta: break
    return best, val

# === GUI ===
class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=COLS*80, height=ROWS*80, bg="#333")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.play)
        tk.Button(root, text="New Game", command=self.restart).pack(pady=5)
        self.restart()

    def restart(self):
        self.board = new_board()
        self.turn = random.choice([PLAYER, AI])
        self.over = False
        self.draw()
        if self.turn == AI: self.root.after(500, self.ai_play)

    def draw(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                color = COLORS[self.board[r][c]]
                self.canvas.create_oval(c*80+5, r*80+5, c*80+75, r*80+75, fill=color, outline="black")

    def play(self, e):
        if self.over or self.turn != PLAYER: return
        c = e.x // 80
        if valid(self.board, c):
            drop(self.board, get_row(self.board, c), c, PLAYER)
            self.next_turn(PLAYER)

    def ai_play(self):
        if self.over: return
        c, _ = minimax(self.board, DEPTH, -math.inf, math.inf, True)
        if c is not None and valid(self.board, c):
            drop(self.board, get_row(self.board, c), c, AI)
            self.next_turn(AI)

    def next_turn(self, p):
        self.draw()
        if win(self.board, p): self.end("You win!" if p == PLAYER else "AI wins!")
        elif not valid_cols(self.board): self.end("It's a tie!")
        else:
            self.turn = PLAYER if p == AI else AI
            if self.turn == AI: self.root.after(500, self.ai_play)

    def end(self, msg):
        self.over = True
        messagebox.showinfo("Game Over", msg)

# === Run ===
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    ConnectFour(root)
    root.mainloop()


