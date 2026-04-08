#Tkinter Lessons
import tkinter as tk
from tkinter import font as tkfont

BG = "#121212"
TEXT = "#FFFFFF"
SUBTLE = "#818384"


app = tk.Tk()
app.title("Wordle")
app.configure(bg=BG)
app.resizable(False, False)
app.geometry("400x600")

 
title_font  = tkfont.Font(family="Helvetica Neue", size=22, weight="bold")
legend_font = tkfont.Font(family="Helvetica Neue", size=11)
 
# ── Header 
header = tk.Frame(app, bg=BG)
header.pack(pady=(18, 4))
tk.Label(header, text="WORDLE", font=title_font,
         bg=BG, fg=TEXT).pack()
 
# ── Separator line ──────────────────────────────────
sep = tk.Frame(app, bg="#3a3a3c", height=1)
sep.pack(fill="x", padx=20, pady=(4, 0))
 
# ── Legend ──────────────────────────────────────────
legend = tk.Frame(app, bg=BG)
legend.pack(pady=(10, 0))
 
legend_items = [
    ("🟩", "Correct position"),
    ("🟨", "Wrong position"),
    ("🟧", "Wrong position — duplicate still hiding"),
    ("⬛", "Not in word"),
]
 
for emoji, desc in legend_items:
    row = tk.Frame(legend, bg=BG)
    row.pack(anchor="w", padx=24)
    tk.Label(row, text=f"{emoji}  {desc}",
             font=legend_font, bg=BG, fg=SUBTLE).pack(side="left")

# Grid Section

TILE_EMPTY  = "#121213"
TILE_BORDER = "#3a3a3c"
TILE_SIZE   = 58
GAP         = 5
 
tile_font = tkfont.Font(family="Times", size=26, weight="bold")
 
grid_frame = tk.Frame(app, bg=BG)
grid_frame.pack(pady=16)
 
tiles  = []   # tiles[row][col]  → Frame
labels = []   # labels[row][col] → Label
 
for r in range(6):
    row_tiles  = []
    row_labels = []
    for c in range(5):
        frame = tk.Frame(
            grid_frame,
            width=TILE_SIZE, height=TILE_SIZE,
            bg=TILE_EMPTY,
            highlightbackground=TILE_BORDER,
            highlightthickness=2,
        )
        frame.grid(row=r, column=c,
                   padx=GAP // 2, pady=GAP // 2)
        frame.grid_propagate(False)  # lock to TILE_SIZE
 
        lbl = tk.Label(
            frame, text="",
            font=tile_font,
            bg=TILE_EMPTY, fg="#ffffff",
            anchor="center",
        )
        lbl.place(relwidth=1, relheight=1)
 
        row_tiles.append(frame)
        row_labels.append(lbl)
 
    tiles.append(row_tiles)
    labels.append(row_labels)

current_row     = 0   # which row we're filling (0–5)
current_col     = 0   # which column is next (0–4)
current_letters = []  # letters typed so far this row
TILE_FILLED     = "#121213"
TILE_BORDER_ACTIVE = "#999999"   # lighter border when a letter is typed


 
def set_tile(row, col, text, bg, border):
    tiles[row][col].config(bg=bg, highlightbackground=border)
    labels[row][col].config(text=text, bg=bg)
 
def on_key(event):
    global current_row, current_col, current_letters
 
    key = event.keysym
 
    if key == 'Return':
        if len(current_letters) == 5:
            # Row is complete — advance to the next row
            print(f"Row {current_row} submitted: {''.join(current_letters)}")  # debug
            current_row    += 1
            current_col     = 0
            current_letters = []
            if current_row > 5:
                print("Game over — no more rows")
        else:
            print(f"Need 5 letters, only have {len(current_letters)}")  # debug
 
    elif key == 'BackSpace':
        if current_letters:
            current_col -= 1
            current_letters.pop()
            set_tile(current_row, current_col,
                     "", TILE_EMPTY, TILE_BORDER)
 
    elif len(key) == 1 and key.isalpha() and current_col < 5:
        current_letters.append(key.lower())
        set_tile(current_row, current_col,
                 key.upper(), TILE_FILLED, TILE_BORDER_ACTIVE)
        current_col += 1
 
app.bind('<Key>', on_key)
app.mainloop() 
