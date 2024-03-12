import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

# Load the CSV data, now considering the header
df = pd.read_csv('training_results.csv', na_values=',,').fillna(0)

# Initialize the figure and axis for the plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Make room for the start button


def init():
    """Initialization function for the animation."""
    ax.clear()
    ax.set_title('Ready')
    ax.axhline(y=0, color='k', linestyle='-')  # Baseline
    ax.set_xlim(0, len(df.columns))
    ax.set_ylim(-1.2, 1.2)  # Adjusted Y-axis limits


def animate(i):
    """Update the plot for each frame."""
    ax.clear()
    ax.set_title(f'Iteration {4000 * (i + 1)} - Author: Lijian Liu 2024 for XCS221')
    weights = df.iloc[i].values
    columns = df.columns
    indices = np.arange(len(weights))

    # Sorting weights to find top 30 positive and negative
    sorted_indices = np.argsort(weights)
    top_positive_indices = sorted_indices[-30:]
    top_negative_indices = sorted_indices[:30]

    # Plot all weights
    ax.scatter(indices[weights > 0], weights[weights > 0], color='blue', s=1)
    ax.scatter(indices[weights < 0], weights[weights < 0], color='red', s=1)
    ax.axhline(y=0, color='k', linestyle='-')  # Baseline

    # Annotate top positive weights
    for idx in top_positive_indices:
        ax.text(idx, weights[idx], columns[idx], fontsize=8, ha='center', bbox=dict(facecolor='lightblue', alpha=0.8))

    # Annotate top negative weights
    for idx in top_negative_indices:
        ax.text(idx, weights[idx], columns[idx], fontsize=8, ha='center', bbox=dict(facecolor='lightpink', alpha=0.8))

    # Y-axis labels
    ax.text(len(df.columns) * 0.95, 1.0, 'Positive sentiment', horizontalalignment='right', verticalalignment='center',
            fontsize=9, bbox=dict(facecolor='white', alpha=1))
    ax.text(len(df.columns) * 0.95, -1.0, 'Negative sentiment', horizontalalignment='right', verticalalignment='center',
            fontsize=9, bbox=dict(facecolor='white', alpha=1))

    # X-axis label
    ax.set_xlabel('Feature index')

    ax.set_xlim(0, len(weights))
    ax.set_ylim(-2.2, 2.2)


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

