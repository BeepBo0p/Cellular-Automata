import numpy as np
import pygame as pg
import random as rd
from numba import jit, njit


# Settings
width = 250
height = 250
coverage = 0.7
initial_cells = int(coverage * 0.01 * width * height)
steps = 100
click_radius = 5

# Create grid
grid = np.zeros((width, height))

# Randomly populate grid
for i in range(initial_cells):
    x = int(np.random.normal(width/2, width/6))
    y = int(np.random.normal(height/2, height/6))

    if x >= 0 and x < width and y >= 0 and y < height:

        grid[x][y] = 1
    
# Invert grid
grid = np.logical_not(grid)

@njit
def get_neighbours(grid, x, y):
        
        # Get number of neighbours
        neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                
                # Get neighbour position
                neighbour_x = x + i
                neighbour_y = y + j
                
                # Check if neighbour is on grid
                if neighbour_x >= 0 and neighbour_x < width and neighbour_y >= 0 and neighbour_y < height:
                    
                    # Add to neighbour count
                    neighbours += grid[neighbour_x][neighbour_y]
        
        # Remove cell from neighbour count
        neighbours -= grid[x][y]
        
        return neighbours

@njit
def run_generation(grid):
    
    for i in range(width):
        for j in range(height):
            
            # Get cell and neighbours
            cell = grid[i][j]
            neighbours = get_neighbours(grid, i, j)
            
            # Apply rules
            if cell == 1 and neighbours < 2:
                grid[i][j] = 0
            elif cell == 1 and (neighbours == 2 or neighbours == 3):
                grid[i][j] = 1#np.random.randint(0,1) #choice(a=[0, 1]), p=[0.1, 0.9])
            elif cell == 1 and neighbours > 3:
                grid[i][j] = 0
            elif cell == 0 and neighbours == 3:
                grid[i][j] = 1

def add_point(grid, x, y):
    
    # Check if point is on grid
    if x >= 0 and x < width and y >= 0 and y < height:
        
        # Add point
        grid[x][y] = 1
        grid[x+1][y] = 1
        grid[x][y+1] = 1
        grid[x+1][y+1] = 1
        grid[x-1][y] = 1
        grid[x][y-1] = 1
        grid[x-1][y-1] = 1
        grid[x+1][y-1] = 1
        grid[x-1][y+1] = 1
        
        
    return grid

def remove_point(grid, x, y):
    
    # Check if point is on grid
    if x >= 0 and x < width and y >= 0 and y < height:
        
        # Remove point
        grid[x][y] = 0
        grid[x+1][y] = 0
        grid[x][y+1] = 0
        grid[x+1][y+1] = 0
        grid[x-1][y] = 0
        grid[x][y-1] = 0
        grid[x-1][y-1] = 0
        grid[x+1][y-1] = 0
        grid[x-1][y+1] = 0
        
        
    return grid

window = pg.display.set_mode((width*3, height*3))
pg.display.set_caption('Game of Life')

running = True
paused = True
while running:
    
    # Check for quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    # Check for pause
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        pg.time.delay(200)
        paused = not paused
    
    # Check for mouse click
    mouse = pg.mouse.get_pressed()
    if mouse[0]:
        
        print('left click')
        
        # Get mouse position
        x, y = pg.mouse.get_pos()
        x = int(x/3)
        y = int(y/3)
        
        # Add point
        grid = add_point(grid, x, y)
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3, y*3, 3, 3))
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3+1, y*3, 3, 3))
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3, y*3+1, 3, 3))
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3+1, y*3+1, 3, 3))
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3-1, y*3, 3, 3))
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3, y*3-1, 3, 3))
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3-1, y*3-1, 3, 3))
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3+1, y*3-1, 3, 3))
        pg.draw.rect(surface=window, color=(255, 255, 255), rect=(x*3-1, y*3+1, 3, 3))
        
        pg.display.update()
        continue
        
        
    if mouse[2]:
            
        print('right click')
        # Get mouse position
        x, y = pg.mouse.get_pos()
        x = int(x/3)
        y = int(y/3)
            
        # Remove point
        grid = remove_point(grid, x, y)
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3, y*3, 3, 3))
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3+1, y*3, 3, 3))
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3, y*3+1, 3, 3))
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3+1, y*3+1, 3, 3))
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3-1, y*3, 3, 3))
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3, y*3-1, 3, 3))
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3-1, y*3-1, 3, 3))
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3+1, y*3-1, 3, 3))
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(x*3-1, y*3+1, 3, 3))
        
        pg.display.update()
        continue
    
        
    if paused:
        continue
    
    # Run generation
    run_generation(grid)
    
    # Draw grid
    for i in range(width):
        for j in range(height):
            
            # Get cell
            cell = grid[i][j]
            
            # Draw cell
            if cell == 1:
                pg.draw.rect(surface=window, color=(255, 255, 255), rect=(i*3, j*3, 3, 3))
                
            else:
                pg.draw.rect(surface=window, color=(0, 0, 0), rect=(i*3, j*3, 3, 3))
    
    # Update display
    pg.display.update()
    
    # Pause
    pg.time.delay(20)
