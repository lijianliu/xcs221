import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Training data
trainExamples = np.array([(1, 1), (2, 3), (4, 3)])

# Feature transformation function (phi)
def phi(x):
    # Assume phi(x) is x itself for simplicity
    return np.array([1, x])

# Training loss function
def trainLoss(w):
    return 1.0 / len(trainExamples) * sum((w.dot(phi(x)) - y)**2 for x, y in trainExamples)

# Gradient of the training loss function
def gradientTrainLoss(w):
    return 1.0 / len(trainExamples) * sum(2 * (w.dot(phi(x)) - y) * phi(x) for x, y in trainExamples)

# Prepare the grid for the loss surface
w0_range = np.linspace(0, 80, 230)
w1_range = np.linspace(-20, 10, 230)
w0, w1 = np.meshgrid(w0_range, w1_range)

# Compute the loss for each combination of w0 and w1
loss_surface = np.array([[trainLoss(np.array([w0_i, w1_j]))
                          for w1_j in w1_range] for w0_i in w0_range])

# Gradient descent parameters
epochs = 500
learning_rate = 0.01
w = np.array([66.0, 0.0])  # Initial weights
path = np.zeros((epochs, 3))  # Store the path of w0, w1, and loss

# Perform gradient descent
for i in range(epochs):
    grad = gradientTrainLoss(w)
    path[i] = np.array([w[0], w[1], trainLoss(w)])
    w -= learning_rate * grad


# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(w0, w1, loss_surface, cmap='coolwarm', alpha=0.8)
ax.scatter(path[0, 0], path[0, 1], path[0, 2], color='g', s=50, label='Initial Point')
ax.plot(path[:, 0], path[:, 1], path[:, 2], 'r.-', markersize=5, lw=2, label='Gradient Descent Path')
ax.set_xlabel('w0')
ax.set_ylabel('w1')
ax.set_zlabel('Loss')
ax.set_title('Loss Surface with Gradient Descent Path')
ax.view_init(elev=20., azim=120)
ax.legend()
plt.show()
