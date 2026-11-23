import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle

def display_level(heights):

    max_height = 8
    width = len(heights)

    level = np.zeros((max_height, width))

    for x, height in enumerate(heights):
        for y in range(height):
            level[max_height - 1 - y, x] = 1

    colors = ListedColormap([
        "#87CEEB",  
        "#8B4513"   
    ])

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.imshow(level, cmap=colors, interpolation="nearest", vmin=0, vmax=1)

    # Add a thin green strip (1/4 of a tile) on top of each ground column
    grass_height = 0.25

    for x, height in enumerate(heights):
        if height > 0:
            top_y = max_height - height

            grass = Rectangle(
                (x - 0.5, top_y - 0.5),   
                1,                      
                grass_height,             
                facecolor="#65B84A",
                edgecolor="none"
            )
            ax.add_patch(grass)

    ax.set_title("Procedurally Generated Platform Level")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Rows")

    plt.show()