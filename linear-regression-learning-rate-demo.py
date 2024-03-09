import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Given training data
#trainExamples = np.array([(0, 0), (2, 2)])
trainExamples = np.array([(1, 1), (2, 3), (4, 3)])



# Feature transformation function (phi)
def phi(x):
    return np.array([1, x])


# Training loss function
def trainLoss(w):
    return 1.0 / len(trainExamples) * sum((w.dot(phi(x)) - y) ** 2 for x, y in trainExamples)


# Gradient of the training loss function
def gradientTrainLoss(w):
    return 1.0 / len(trainExamples) * sum(2 * (w.dot(phi(x)) - y) * phi(x) for x, y in trainExamples)


# Gradient descent parameters
epochs = 2000
learning_rate = 0.1  # Initial learning rate
initial_weights = np.array([-0.75, -0.5])  # Starting point for weights

# Prepare the grid for the heatmap
grid_size = 50
w0_range = np.linspace(-1, 3, grid_size)
w1_range = np.linspace(-1, 3, grid_size)
loss_grid = np.zeros((grid_size, grid_size))

# Compute the loss for each combination of w0 and w1
for i, w0 in enumerate(w0_range):
    for j, w1 in enumerate(w1_range):
        loss_grid[i, j] = trainLoss(np.array([w0, w1]))

# Tkinter GUI setup
root = tk.Tk()
root.wm_title("Gradient Descent Learning Rate Adjustment")

# Initialize the plot
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# Learning rate label
lr_label = tk.Label(root, text=f"Learning Rate: {learning_rate}")
lr_label.pack()


# Plotting function
def plot():
    # Clear the current plot
    ax.clear()

    # Display the loss heatmap
    ax.imshow(loss_grid, extent=[w0_range.min(), w0_range.max(), w1_range.min(), w1_range.max()],
              origin='lower', cmap='coolwarm', aspect='auto')

    # Run gradient descent
    w = initial_weights.copy()
    path = np.zeros((epochs, 2))  # Store the path of w0, w1
    for i in range(epochs):
        grad = gradientTrainLoss(w)
        path[i] = w
        w -= learning_rate * grad

    # Plot the gradient descent path
    ax.plot(path[:, 0], path[:, 1], 'r.-', markersize=5, lw=2, label='Gradient Descent Path')
    ax.scatter(path[0, 0], path[0, 1], color='yellow', s=50, label='Start Point')
    ax.scatter(path[-1, 0], path[-1, 1], color='red', s=50, label='End Point')
    ax.set_xlabel('w0')
    ax.set_ylabel('w1')
    ax.set_title('Training Loss Heatmap with Gradient Descent Path')
    ax.legend(loc='lower center')
    canvas.draw()


plot()  # Initial plot


# Button event functions
def increase_lr():
    global learning_rate
    learning_rate += 0.001
    lr_label.config(text=f"Learning Rate: {learning_rate:.4f}")
    plot()


def decrease_lr():
    global learning_rate
    learning_rate = max(0.01, learning_rate - 0.001)
    lr_label.config(text=f"Learning Rate: {learning_rate:.4f}")
    plot()


# Buttons
button_frame = tk.Frame(root)
button_increase = tk.Button(button_frame, text="Increase LR", command=increase_lr)
button_decrease = tk.Button(button_frame, text="Decrease LR", command=decrease_lr)
button_increase.pack(side=tk.LEFT)
button_decrease.pack(side=tk.LEFT)
button_frame.pack(side=tk.TOP)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Start the Tkinter loop
tk.mainloop()
