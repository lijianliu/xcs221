import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

# Load the CSV data
df = pd.read_csv('1b_training_results.csv', header=None, na_values=',,').fillna(0)

# Initialize the figure and axis for the plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Make room for the start button

def init():
    """Initialization function for the animation."""
    ax.clear()
    ax.set_title('Ready')
    ax.axhline(y=0, color='k', linestyle='-')  # Baseline
    ax.set_xlim(0, len(df.columns))
    ax.set_ylim(-1, 1)  # Default Y-axis limits

def animate(i):
    """Update the plot for each frame."""
    ax.clear()
    ax.set_title(f'Iteration {50 * (i + 1)} - Author: Lijian Liu 2024 for XCS221')
    weights = df.iloc[i].values
    indices = np.arange(len(weights))
    ax.scatter(indices[weights > 0], weights[weights > 0], color='blue', s=1)
    ax.scatter(indices[weights < 0], weights[weights < 0], color='red', s=1)
    ax.axhline(y=0, color='k', linestyle='-')  # Baseline
    ax.set_xlim(0, len(weights))
    ax.set_ylim(-1.2, 1.2)  # Keep the Y-axis constant for visual consistency

# Global variable for the animation object
ani = None

def toggle_animation(event):
    global ani
    label = button.label.get_text()
    if label == 'Start':
        button.label.set_text('Pause')
        ani = FuncAnimation(fig, animate, frames=len(df), init_func=init, interval=20, repeat=False)
        fig.canvas.draw()
    elif label == 'Pause':
        ani.event_source.stop()
        button.label.set_text('Resume')
    elif label == 'Resume':
        ani.event_source.start()
        button.label.set_text('Pause')

# Create a start/pause/resume button and assign the event handler
button_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
button = Button(button_ax, 'Start')
button.on_clicked(toggle_animation)

plt.show()

