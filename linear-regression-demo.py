import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox

# Training examples
trainExamples = [(1, 1), (2, 3), (4, 3)]

# Feature mapping function
def phi(x):
    return np.array([1, x])

# Initialize the weight vector with zeros
def initialWeightVector(custom_weights=None):
    if custom_weights is not None and len(custom_weights) == 2:
        return np.array(custom_weights)
    return np.zeros(2)

# Compute the training loss
def trainLoss(w):
    return 1.0 / len(trainExamples) * sum((w.dot(phi(x)) - y)**2 for x, y in trainExamples)

# Compute the gradient of the training loss
def gradientTrainLoss(w):
    return 1.0 / len(trainExamples) * sum(2 * (w.dot(phi(x)) - y) * phi(x) for x, y in trainExamples)

# Global variables for the animation and weights
weights = []
ani = None

# Setup the figure and axis for the plot and widgets
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.35)  # Make room for widgets
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)

# Plot the training points
for x, y in trainExamples:
    ax.scatter(x, y, color='blue')

line, = ax.plot([], [], color='red', linewidth=2)
iteration_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
weights_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
loss_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)

# Initialize the animation function
def init():
    line.set_data([], [])
    iteration_text.set_text('')
    weights_text.set_text('')
    loss_text.set_text('')
    return line, iteration_text, weights_text, loss_text

# Define the animation update function
def animate(i):
    global weights
    w = weights[i]
    x_range = np.linspace(0, 5, 100)
    y_line = w[0] + w[1] * x_range
    line.set_data(x_range, y_line)
    iteration_text.set_text(f'Iteration: {i}')
    weights_text.set_text(f'Weights: w0 = {w[0]:.2f}, w1 = {w[1]:.2f}')
    loss_text.set_text(f'Train Loss: {trainLoss(w):.4f}')
    return line, iteration_text, weights_text, loss_text

# Start/Restart animation event handler
def start_restart_animation(event):
    global ani, weights
    interval = float(interval_text_box.text) if interval_text_box.text else 100
    custom_weights = [float(x.strip()) for x in weights_text_box.text.split(',')] if weights_text_box.text else [0, 0]
    weights = [initialWeightVector(custom_weights)]
    for _ in range(1, 500):
        w = weights[-1].copy()
        gradient = gradientTrainLoss(w)
        w -= 0.1 * gradient
        weights.append(w)
    if ani is not None:
        ani.event_source.stop()
    ani = FuncAnimation(fig, animate, frames=np.arange(0, len(weights)),
                        init_func=init, blit=True, interval=interval, repeat=False)

# Create a "Start/Restart" button
button_ax = fig.add_axes([0.81, 0.05, 0.15, 0.075])
button = Button(button_ax, 'Start/Restart')
button.on_clicked(start_restart_animation)

# Create a text box for the animation interval input
interval_text_box_ax = fig.add_axes([0.81, 0.15, 0.1, 0.05])
interval_text_box = TextBox(interval_text_box_ax, 'Interval (ms)', initial="100")

# Create a text box for the initial weights input
weights_text_box_ax = fig.add_axes([0.81, 0.25, 0.1, 0.05])
weights_text_box = TextBox(weights_text_box_ax, 'Initial Weights', initial="0, 0")

# Add title with author's name and LinkedIn URL
plt.suptitle("Linear Regression - Gradient Descent Demo - Author: Lijian Liu - V2024-01", fontsize=10)

plt.show()

