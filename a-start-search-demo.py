import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button


# Function to parse the map file
def parse_map(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    nodes = {}
    edges = []

    for line in lines:
        if line.strip() and line[0].isdigit():
            parts = line.split(' ')
            node_id = parts[0]
            lat_lon = parts[1].strip('()').split(',')
            lat, lon = lat_lon[0], lat_lon[1].split(':')[0].strip(')')
            nodes[node_id] = (float(lat), float(lon))
        elif '->' in line:
            target_node = line.strip().split(' ')[1]
            edges.append((node_id, target_node))

    return nodes, edges


# Function to parse the UCS output file to get the search paths
def parse_ucs_output_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    paths = []
    actions = []
    action_start = False

    for line in lines:
        if 'actions =' in line:
            actions = line.strip("actions = []\n").split(', ')
            actions = [action.strip("'") for action in actions]
        elif '=>' in line and not action_start:
            parts = line.split('=>')
            from_node = parts[0].split("'")[1]
            to_node = parts[1].split("'")[1]
            paths.append((from_node, to_node))

    return paths, actions


# Function to plot the map with animation
def plot_map_with_animation(nodes, edges, paths, actions):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')

    # Add markers for start and end locations
    start_x, start_y = nodes[actions[0]]
    end_x, end_y = nodes[actions[-1]]
    # ax.plot(start_y, start_x, 'go', markersize=12, zorder=5)  # Start location in green
    # ax.plot(end_y, end_x, 'yo', markersize=12, zorder=5)  # End location in red

    ax.plot(start_y, start_x, marker='o', color='yellow', markersize=10, markeredgewidth=1.5, markeredgecolor='black',
            alpha=0.6, zorder=3)

    ax.plot(end_y, end_x, marker='*', color='yellow', markersize=15, markeredgewidth=1.5, markeredgecolor='black',
            alpha=0.6, zorder=3)

    # Draw the static map once
    for edge in edges:
        x1, y1 = nodes[edge[0]]
        x2, y2 = nodes[edge[1]]
        ax.plot([y1, y2], [x1, x2], 'lightgray', linewidth=0.5)

    is_end_path_draw = False
    steps = 100

    # Animation update function
    def update(frame):
        nonlocal is_end_path_draw

        # Only draw a new line for the current frame's path
        print(f"frame={frame}")
        if is_end_path_draw:
            return []

        for n in range(steps):
            index = steps * frame + n
            if index < len(paths):
                from_node, to_node = paths[steps * frame + n]
                x1, y1 = nodes[from_node]
                x2, y2 = nodes[to_node]
                ax.plot([y1, y2], [x1, x2], 'r-', linewidth=1)
                if n == 0:
                    print(f"ax.plot([y1={y1}, y2={y2}], [x1={x1}, x2={x2}], 'r-', linewidth=1)")
            elif not is_end_path_draw:
                print(f"action={actions}")
                # When all paths are done, draw the action path in blue
                action_y, action_x = zip(*[(nodes[action][1], nodes[action][0]) for action in actions])
                ax.plot(action_y, action_x, 'b-', linewidth=2, zorder=2)
                is_end_path_draw = True
                print(f"done is_end_path_draw")
                print(f"action_y={action_y}")
                print(f"action_x={action_x}")
        return []

    def start_animation(event):
        # Start the animation
        print(f"paths={len(paths)}")
        print(f"total_frames= {int(len(paths) / steps) + 1}")
        total_frames = int(len(paths) / steps) + 1  # One extra frame for the actions

        ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=1, blit=True, repeat=False)
        plt.show()

    # Create a button axis
    button_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    button = Button(button_ax, 'Start')

    # Assign the callback function to the button
    button.on_clicked(start_animation)
    plt.show()
    return


# Paths to files
map_file_path = 'readableStanfordMap.txt'
ucs_output_file_path = 'Test_4b.test_3.txt'
# 'test_3a.test_4.txt'

# Read the map and UCS output
nodes, edges = parse_map(map_file_path)
paths, actions = parse_ucs_output_file(ucs_output_file_path)

# Create the animation
ani = plot_map_with_animation(nodes, edges, paths, actions)

