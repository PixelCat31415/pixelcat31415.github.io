import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# 1. Define the range for x and y (standard normal covers ~99.7% within +/- 3 std dev)
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)

# 2. Create a coordinate grid
X, Y = np.meshgrid(x, y)

# 3. Calculate the joint PDF for standard normal i.i.d variables
# Formula: (1 / (2 * pi)) * exp(-(x^2 + y^2) / 2)
Z = (1 / (2 * np.pi)) * np.exp(-(X**2 + Y**2) / 2)

# 4. Plotting
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Create the surface plot
surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis, edgecolor='none', alpha=0.9)
ax.set_box_aspect((1, 1, 1/3))

# Add labels and title
ax.set_title('Joint PDF of Two I.I.D. Standard Normal RVs')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Density')

# Add a color bar for reference
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
