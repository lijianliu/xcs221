import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
from matplotlib.patches import Patch
from matplotlib.widgets import Button

# File path
file_path = 'mdr-pi.txt'

# Function to parse a line into a dictionary
def parse_line(line):
    # Extract the dictionary string from the line
    dict_str = re.search(r'\{(.*)\}', line).group(0)
    # Convert the dictionary string to a dictionary
    data_dict = eval(dict_str)
    return data_dict

# Read the file and parse each line into a list of dictionaries
pi_list = []
with open(file_path, 'r') as file:
    for line in file:
        if line.startswith('pi='):
            pi_list.append(parse_line(line))

# Mapping from values to labels and colors
value_to_label = {0: 'L', 1: 'N', 2: 'R'}
label_to_color = {'L': 'lightblue', 'N': 'lightgreen', 'R': 'salmon'}

iteration = 0
def common_frame(iteration):
    ax.set_title(f'(Episode {iteration}) PI - Policy (L/N/R) by state (Position, Velocity) by Lijian Liu')
    # Set x and y limits
    ax.set_xlim(-1, 20)
    ax.set_ylim(-1, 20)
    ax.set_xlabel('X - Position')
    ax.set_ylabel('Y - Velocity')
    ax.grid(True)
    ax.set_aspect('equal')

# Create the plot for animation, set a larger figure size here
fig, ax = plt.subplots(figsize=(10, 8))
common_frame(0)
# Define legend patches
legend_patches = [
    Patch(facecolor=label_to_color['L'], edgecolor='black', label='Left (L)'),
    Patch(facecolor=label_to_color['N'], edgecolor='black', label='Neutral (N)'),
    Patch(facecolor=label_to_color['R'], edgecolor='black', label='Right (R)')
]

# Flag to control the animation update
animation_running = False

# Function to update the animation
def update(frame):
    print("update()")
    global iteration

    if not animation_running or iteration >= len(pi_list):
        return
    ax.clear()
    iteration += 1
    common_frame(iteration)

    print(f"iteration{iteration-1}")
    for (x, y), value in pi_list[iteration-1].items():
        label = value_to_label[value]
        bg_color = label_to_color[label]
        ax.text(x, y, label, ha='center', va='center', fontsize=12,
                bbox=dict(facecolor=bg_color, edgecolor='black'))

    # Add a legend to the plot
    ax.legend(handles=legend_patches, loc='upper right')

# Function to handle button click
def on_click(event):
    global animation_running
    animation_running = True

# Create button for starting animation
ax_button = plt.axes([0.81, 0.01, 0.1, 0.05])
button = Button(ax_button, 'Start')

# Create the animation
ani = animation.FuncAnimation(fig, update, interval=1000, repeat=False)

# Button click event handler
button.on_clicked(on_click)

plt.show()
