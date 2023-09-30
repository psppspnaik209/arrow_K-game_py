import tkinter as tk
import random

# main game variables
score = 0
high_score = 0
current_arrow = None

# colors for the text arrows
arrow_colors = {
    'Up': 'red',
    'Down': 'blue',
    'Left': 'green',
    'Right': 'orange',
}

# Function to start the game
def start_game():
    global score, current_arrow
    score = 0
    update_score()
    current_arrow = generate_arrow()
    show_arrow(current_arrow)

# Function to make a random arrow direction text
def generate_arrow():
    directions = ['Up', 'Down', 'Left', 'Right']
    return random.choice(directions)

# Function to show the arrow text on the GUI with the correct color
def show_arrow(arrow):
    arrow_label.config(text=arrow, fg=arrow_colors[arrow])

# Function to handle key presses
def on_key_press(event):
    global score, current_arrow
    if event.keysym == current_arrow:
        score += 1
        update_score()
        current_arrow = generate_arrow()
        show_arrow(current_arrow)
    else:
        end_game()

# Function to update the score
def update_score():
    score_label.config(text=f'Score: {score}')
    update_high_score()

# Function to update the high score
def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        high_score_label.config(text=f'High Score: {high_score}')

# Function to end the game
def end_game():
    global score, current_arrow
    score_label.config(text=f'Game Over! Your Score: {score}')
    if score > high_score:
        high_score_label.config(text=f'New High Score: {score}')
    score = 0
    current_arrow = None

# Function to restart the game using the Restart button
def restart_game(event=None):
    start_game()

# Function to toggle "Always on Top" on/off
def toggle_always_on_top():
    current_state = root.attributes('-topmost')
    root.attributes('-topmost', not current_state)

# The main GUI window
root = tk.Tk()
root.title('Arrow Key Game')

# Fixed window size
root.geometry("400x200")

# Create and configure GUI elements
start_button = tk.Button(root, text='Start Game', command=start_game)
start_button.pack()

arrow_label = tk.Label(root, text='', font=('Helvetica', 48))
arrow_label.pack()

score_label = tk.Label(root, text='Score: 0', font=('Helvetica', 24))
score_label.pack()

high_score_label = tk.Label(root, text='High Score: 0', font=('Helvetica', 18))
high_score_label.pack()

# Button to toggle "Always on Top"
always_on_top_button = tk.Button(root, text='Toggle Always on Top', command=toggle_always_on_top)
always_on_top_button.pack()

# Bind key presses to the game
root.bind('<Up>', on_key_press)
root.bind('<Down>', on_key_press)
root.bind('<Left>', on_key_press)
root.bind('<Right>', on_key_press)

# Bind space bar and Enter key to restart the game
root.bind('<space>', restart_game)
root.bind('<Return>', restart_game)
root.bind('<KP_Enter>', restart_game)  # Numpad Enter

# Start the GUI main loop
root.mainloop()
