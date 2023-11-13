import tkinter as tk
import random
import pygame
from pygame.locals import JOYAXISMOTION, JOYBUTTONDOWN

# Main game variables
score = 0
high_score = 0
current_arrow = None

# Colors for the text arrows
arrow_colors = {
    'Up': 'yellow',
    'Down': 'green',
    'Left': 'blue',
    'Right': 'red',
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

# Function to handle joystick events
def on_joy_event(event):
    global score, current_arrow
    if event.type == JOYAXISMOTION:
        # Check left joystick or right joystick movement
        if event.axis in (0, 1, 3, 4):  # X and Y axes for both left and right joysticks
            axis_value = event.dict['value']
            if axis_value < -0.5:
                handle_joystick_movement('Left')
            elif axis_value > 0.5:
                handle_joystick_movement('Right')

    elif event.type == JOYBUTTONDOWN:
        # Check D-pad buttons
        if event.dict['button'] in (0, 1, 2, 3):
            handle_joystick_movement(['Up', 'Down', 'Left', 'Right'][event.dict['button']])

        # Check Start button
        elif event.dict['button'] == 7:
            restart_game()

# Function to handle joystick movement
def handle_joystick_movement(direction):
    global score, current_arrow
    if direction == current_arrow:
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

# Initialize pygame for joystick handling
pygame.init()

# Joystick setup
joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    pygame.event.set_allowed([JOYAXISMOTION, JOYBUTTONDOWN])

    # Bind joystick events to handle joystick movements
    root.bind('<Motion>', on_joy_event)
    root.bind('<Button-1>', on_joy_event)
    root.bind('<Button-3>', on_joy_event)
    root.bind('<Button-2>', on_joy_event)
    root.bind('<B1-Motion>', on_joy_event)

# Start the GUI main loop
root.mainloop()
