import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
from matplotlib.patches import Patch
from matplotlib import patches
from matplotlib.widgets import Button
from matplotlib.widgets import Slider


# File path
#file_path = 'mdr-pi-4-224.txt'
#file_path = 'v-final-training.txt'
#file_path = "mdr-pi-2.txt"
file_path = "mdr-prob-2-policy.txt"

# Function to parse a line into a dictionary
def parse_line(line):
    # Extract the dictionary string from the line
    dict_str = re.search(r'\{(.*)\}', line).group(0)
    # Convert the dictionary string to a dictionary
    data_dict = eval(dict_str)
    #data_dict = {k: int(v) for k, v in data_dict.items()}
    data_dict = {k: v for k, v in data_dict.items()}
    global min_value, max_value
    min_value = min([round(value, 1) for value in data_dict.values()])
    max_value = max([round(value, 1) for value in data_dict.values()])
    return data_dict


# Function to read the file and extract the tuples
def extract_tuples_from_actions(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Use regular expression to find all tuples after 'getAction'
    tuples = re.findall(r'getAction\(\((\d+, \d+)\)', file_content)

    # Convert string tuples to actual tuples
    tuple_list = [tuple(map(int, t.split(', '))) for t in tuples]

    return tuple_list

# Read the file and parse each line into a list of dictionaries
pi_list = []
min_value=999
max_value=-999
with open(file_path, 'r') as file:
    for line in file:
        #if line.startswith('best_actions='):
        #if line.startswith('pi='):
        #if line.startswith('V_opt='):
        if line.startswith('newV='):
            pi_list.append(parse_line(line))

final_actions = extract_tuples_from_actions("final-actions.txt")

# Mapping from values to labels and colors
value_to_label = {0: 'L', 1: 'N', 2: 'R'}
label_to_color = {'L': 'lightblue', 'N': 'lightgreen', 'R': 'salmon'}

iteration = 0
def common_frame(iteration):
    #ax.set_title(f'(Episode {iteration}) PI - Policy (L/N/R) by state (Position, Velocity) by Lijian Liu')
    ax.set_title(f'ValueIteration V_ops by state after {iteration} iterations - Author Lijian Liu')
    #ax.set_title(f'ValueIteration Policy by state after {iteration} iterations - Author Lijian Liu')
    # Set x and y limits
    ax.set_xlim(-1, 20)
    ax.set_ylim(0, 19)
    ax.set_xlabel('X - Position')
    ax.set_ylabel('Y - Velocity')
    ax.grid(True)
    ax.set_aspect('equal')

# Create the plot for animation, set a larger figure size here
fig, ax = plt.subplots(figsize=(8, 8))
common_frame(0)
# Define legend patches
legend_patches = [
    Patch(facecolor=label_to_color['L'], edgecolor='black', label='Left (L)'),
    Patch(facecolor=label_to_color['N'], edgecolor='black', label='Neutral (N)'),
    Patch(facecolor=label_to_color['R'], edgecolor='black', label='Right (R)')
]

# Flag to control the animation update
pause = True

# Function to update the animation
def update(frame):
    global iteration
    global pause
    if iteration >= len(pi_list):
        return
    ax.clear()
    if not pause:
        iteration += 1
    common_frame(iteration)
    colormap = plt.cm.Paired
    print(f"iteration{iteration-1}")

    min_value = 999
    max_value = -999
    for (x, y), value in pi_list[iteration-1].items():
        min_value = min(min_value, value)
        max_value = max(max_value, value)


    for (x, y), value in pi_list[iteration-1].items():
        # label = value_to_label[value]
        # bg_color = label_to_color[label]
        fontcolor = "black"
        label = round(value, 1)
        #print(f"label={label}")
        normalized_value = (value - min_value) / (max_value - min_value)
        if (x,y) in final_actions:
            #bg_color = colormap(normalized_value/2 + 0.5)
            bg_color = colormap(normalized_value * 2.0 / 3.0 + 0.3)
            fontcolor = "black"
        else:
            bg_color = colormap(normalized_value*2.0/3.0 + 0.3)
            #bg_color = colormap(normalized_value )
            fontcolor = 'black'
        ax.text(x, y, label, ha='center', va='center', fontsize=7, color=fontcolor,clip_on=True,
                bbox=dict(facecolor=bg_color, edgecolor="black"))

    for (x, y) in final_actions:
        # Create a rectangle patch
        rect = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=1,
                                 edgecolor='black', facecolor='yellow', alpha=.65)

        # Add the rectangle to the Axes
        ax.add_patch(rect)


    # Add a legend to the plot
    ax.legend(handles=legend_patches, loc='upper right')

# Function to handle button click
def on_click_start(event):
    global pause
    global iteration
    iteration = 0
    pause = False

def on_click_pause(event):
    global pause
    pause = not pause

def update_slider(val):
    global iteration
    iteration = int(val)

# Create button for starting animation
ax_button = plt.axes([0.81, 0.01, 0.1, 0.05]) # left, bottom, width, height
button = Button(ax_button, 'Start / Restart')
pause_button_box = plt.axes([0.61, 0.01, 0.1, 0.05]) # left, bottom, width, height
pause_button = Button(pause_button_box, 'Pause')
axfreq = plt.axes([0.25, 0.90, 0.65, 0.03])  # left, bottom, width, height
slider = Slider(axfreq, 'frame', 1, 386, valinit=1, valstep=1)
slider.on_changed(update_slider)

def on_press(event):
    global mouse_pressed
    global pause
    if event.inaxes == axfreq:
        mouse_pressed = True
        pause = True
        print("Mouse button pressed on the slider")

def on_release(event):
    global mouse_pressed
    mouse_pressed = False
    print("Mouse button released")
# Register the mouse event handlers
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)


# Create the animation
ani = animation.FuncAnimation(fig, update, interval=100, repeat=False)

# Button click event handler
button.on_clicked(on_click_start)
pause_button.on_clicked(on_click_pause)

plt.show()
