import tkinter as tk
import math

# --- Game State Variables ---
current_player = 'X'  # Player is 'X', AI is 'O'
board = [''] * 9      # 3x3 board (index 0-8)
buttons = []
game_over = False

# --- Game Algorithms ---
def check_win(b, p):
    win = [
        (0,1,2),(3,4,5),(6,7,8), # Horizontal
        (0,3,6),(1,4,7),(2,5,8), # Vertical
        (0,4,8),(2,4,6)          # Diagonal
    ]
    for c in win:
        if b[c[0]] == b[c[1]] == b[c[2]] == p:
            return True, c
    return False, None

def check_draw(b):
    return '' not in b

def get_empty(b):
    return [i for i, v in enumerate(b) if v == '']

def minimax(b, depth, is_max):
    if check_win(b, 'O')[0]: return 10 - depth
    if check_win(b, 'X')[0]: return -10 + depth
    if check_draw(b): return 0
    if is_max:
        best = -math.inf
        for i in get_empty(b):
            b[i] = 'O'
            score = minimax(b, depth+1, False)
            b[i] = ''
            best = max(best, score)
        return best
    else:
        best = math.inf
        for i in get_empty(b):
            b[i] = 'X'
            score = minimax(b, depth+1, True)
            b[i] = ''
            best = min(best, score)
        return best

def best_move(b):
    best = -math.inf
    move = -1
    for i in get_empty(b):
        b[i] = 'O'
        score = minimax(b, 0, False)
        b[i] = ''
        if score > best:
            best = score
            move = i
    return move

# --- GUI Functions ---
def update_status(msg):
    status_label.config(text=msg)

def check_state():
    global game_over
    win, combo = check_win(board, 'X')
    if win:
        update_status("Player X Wins!")
        for i in combo: buttons[i].config(bg='green')
        game_over = True
        return
    win, combo = check_win(board, 'O')
    if win:
        update_status("AI O Wins!")
        for i in combo: buttons[i].config(bg='red')
        game_over = True
        return
    if check_draw(board):
        update_status("It's a Draw!")
        game_over = True
        return
    update_status("Your turn! You are X")

def ai_play():
    global current_player
    if game_over: return
    root.after(400, do_ai)

def do_ai():
    global current_player
    idx = best_move(board)
    if idx != -1:
        board[idx] = 'O'
        buttons[idx].config(text='O', state=tk.DISABLED, fg='blue', font=('Arial', 24, 'bold'))
    check_state()
    # Only update status and switch turn if game is not over
    if not game_over:
        current_player = 'X'
        update_status("Your turn! You are X")

def click_btn(idx):
    global current_player
    if board[idx] == '' and current_player == 'X' and not game_over:
        board[idx] = 'X'
        buttons[idx].config(text='X', state=tk.DISABLED, fg='red', font=('Arial', 24, 'bold'))
        check_state()
        if not game_over:
            current_player = 'O'
            update_status("AI's turn...")
            ai_play()

def reset():
    global board, current_player, game_over
    board = [''] * 9
    current_player = 'X'
    game_over = False
    for b in buttons:
        b.config(text='', state=tk.NORMAL, bg='SystemButtonFace')
    update_status("New Game! Your turn! You are X")

# --- Tkinter Window ---
root = tk.Tk()
root.title("Easy Tic-Tac-Toe Minimax")
status_label = tk.Label(root, text="New Game! Your turn! You are X", font=('Arial', 14, 'bold'), pady=10)
status_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
board_frame = tk.Frame(root)
board_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
for i in range(9):
    btn = tk.Button(board_frame, text='', font=('Arial', 24), width=4, height=2,
                    command=lambda i=i: click_btn(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)
new_game_btn = tk.Button(root, text="New Game", font=('Arial', 12, 'bold'), bg='lightblue',
                         command=reset)
new_game_btn.grid(row=2, column=0, columnspan=3, pady=20)

if __name__ == "__main__":
    root.mainloop()






