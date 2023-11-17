import numpy as np
import pygame as pg
import random as rd
from numba import jit, njit


# Settings
width = 200
height = 200
coverage = 0.1
initial_cells = int(coverage * 0.01 * width * height)
steps = 100
click_radius = 0
s = 6

# Create grid
grid = np.zeros((width, height))

# Randomly populate grid
for i in range(initial_cells):
    x = int(np.random.normal(width/2, width/6))
    y = int(np.random.normal(height/2, height/6))

    #if x >= 0 and x < width and y >= 0 and y < height:

        #grid[x][y] = 1
    
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
    
    new_grid = np.zeros((width, height))
    
    for i in range(width):
        for j in range(height):
            
            # Get cell and neighbours
            cell = grid[i][j]
            neighbours = get_neighbours(grid, i, j)
            #print(neighbours)
            
            # Apply rules
            if cell == 1 and neighbours < 2:
                new_grid[i][j] = 0
            elif cell == 1 and (neighbours == 2 or neighbours == 3):
                new_grid[i][j] = 1
            elif cell == 1 and neighbours > 3:
                new_grid[i][j] = 0
            elif cell == 0 and neighbours == 3:
                new_grid[i][j] = 1
                
    return new_grid 
    
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


def pencil(grid: np.array, x: int, y: int , radius: int, eraser: bool = False) -> np.array:
    
    tip = 1 if not eraser else 0
    
    # Check if point is on grid
    if x >= 0 and x < width and y >= 0 and y < height:
        
        for i in range(-radius, radius+1):
            for j in range(-radius, radius+1):
                
                # Get neighbour position
                neighbour_x = x + i
                neighbour_y = y + j
                
                # Check if neighbour is on grid
                if neighbour_x >= 0 and neighbour_x < width and neighbour_y >= 0 and neighbour_y < height:
                    
                    # Draw point
                    grid[neighbour_x][neighbour_y] = tip
                    pg.draw.rect(surface=window, color=(255*tip, 255*tip, 255*tip), rect=(neighbour_x*s, neighbour_y*s, s, s))
    pg.display.update()
        
    return grid



window = pg.display.set_mode((width*s, height*s))
pg.transform.scale(window, (width*s, height*s))
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
        
        
    for event in pg.event.get():
        
        pg.time.delay(20)
        
        if event.type == pg.MOUSEBUTTONDOWN:
            
            if event.button == 4:
                
                print('up scroll')
                if click_radius == 0:
                    click_radius = 0.1
                    
                if click_radius < 1:
                    click_radius = min(1, click_radius+0.1)
                
                click_radius *= 1.1
                
                continue
            
            elif event.button == 5:
                
                print('down scroll')
                if click_radius > 1:
                    click_radius = max(0, click_radius*0.9)
                    
                else:
                    click_radius = max(0, click_radius-0.1)
                
                continue
    

        
        
    # Check for mouse click
    mouse = pg.mouse.get_pressed()
    if mouse[0]:
        
        print('left click')
        
        # Get mouse position
        x, y = pg.mouse.get_pos()
        x = int(x/s)
        y = int(y/s)
        
        # Add point
        grid = pencil(grid, x, y, int(click_radius))
        
        continue
        
        
    if mouse[2]:
            
        print('right click')
        # Get mouse position
        x, y = pg.mouse.get_pos()
        x = int(x/s)
        y = int(y/s)
            
        # Remove point
        grid = pencil(grid, x, y, int(click_radius), eraser=True)
        
        continue
    

    

    
        
    if paused:
        
        # Display pencil size in top left
        pg.draw.rect(surface=window, color=(0, 0, 0), rect=(0, 0, 100, 20))
        pg.font.init()
        font = pg.font.SysFont('Arial', 12)
        text = font.render(f'Pencil size: {click_radius:0.2f}', True, (255, 255, 255))
        window.blit(text, (0, 0))
        pg.display.update()
        
        continue
    
    # Run generation
    grid = run_generation(grid)
    
    # Draw grid
    for i in range(width):
        for j in range(height):
            
            # Get cell
            cell = grid[i][j]
            
            color = [255 * cell, 255 * cell, 255 * cell]
            
            pg.draw.rect(surface=window, color=color, rect=(i*s, j*s, s, s))
                    
    # Update display
    pg.display.update()


    
    pg.event.clear()
