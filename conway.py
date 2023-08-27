import pygame
from time import sleep
import numpy as np

'''
    Click to toggle cells
    Press space to make single steps
    Press 'p' to make steps in a loop
'''

resolution = (500, 500)
grid_size = (25, 25)

class Conway:
    def __init__(self, screen, cells_x, cells_y):
        self.screen = screen
        self.cells_x = cells_x
        self.cells_y = cells_y

        self.px_full_width = screen.get_width()
        self.px_full_height = screen.get_height()
        self.px_cell_width = self.px_full_width // cells_x
        self.px_cell_height = self.px_full_height // cells_y

        self.cells = np.zeros((2, cells_x, cells_y), dtype=bool)
        self.buffer = 0

        # create grid
        grid_color = (0, 0, 0)
        self.grid = pygame.Surface((self.px_full_width, self.px_full_height), flags=pygame.SRCALPHA)
        for x in range(self.cells_x):
            pygame.draw.line(self.grid, grid_color, (x * self.px_cell_width, 0), (x * self.px_cell_width, self.px_full_width))
        for y in range(self.cells_y):
            pygame.draw.line(self.grid, grid_color, (0, y * self.px_cell_height), (self.px_full_height, y * self.px_cell_height))
    
    def draw_cell(self, x, y, alive):
        color_alive = (237, 237, 237)
        color_dead = (69, 69, 69)
        if alive:
            color = color_alive
        else:
            color = color_dead
        rect = pygame.Rect(x * self.px_cell_width, y * self.px_cell_height, self.px_cell_width, self.px_cell_height)
        pygame.draw.rect(self.screen, color, rect)

    def draw(self):
        for x in range(self.cells_x):
            for y in range(self.cells_y):
                alive = self.cells[self.buffer, x, y]
                self.draw_cell(x, y, alive)
        self.screen.blit(self.grid, (0, 0))

    def toggle_cell(self, x, y):
        self.cells[self.buffer, x, y] = not self.cells[self.buffer, x, y]

    def step(self):
        temp_buffer = 1 - self.buffer
        self.cells[temp_buffer,:,:].fill(False)
        for x in range(self.cells_x):
            for y in range(self.cells_y):
                # center = (x, y)
                previous_state = self.cells[self.buffer, x, y]

                if x == 11 and y == 12:
                    pass
                
                up = (x, y-1)
                down = (x, y+1)
                right = (x+1, y)
                left = (x-1, y)
                up_right = (x+1, y-1)
                up_left = (x-1, y-1)
                down_right = (x+1, y+1)
                down_left = (x-1, y+1)
                
                positions = []
                for pos in [up, down, right, left, up_right, up_left, down_right, down_left]:
                    if 0 <= pos[0] < self.cells_x and 0 <= pos[1] < self.cells_y:
                        positions.append(pos)
                states = []
                for pos in positions:
                    states.append(self.cells[self.buffer, pos[0], pos[1]])
                
                n_alive_around = sum(states) # cantidad de celdas aledanias vivas
                
                if n_alive_around < 2:
                    self.cells[temp_buffer, x, y] = False
                elif n_alive_around == 2:
                    self.cells[temp_buffer, x, y] = previous_state
                elif n_alive_around == 3:
                    self.cells[temp_buffer, x, y] = True
                else:
                    self.cells[temp_buffer, x, y] = False
        self.buffer = temp_buffer
                



pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

conway = Conway(screen, grid_size[0], grid_size[1])

# Run until the user asks to quit
running = True
auto_step = False
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                conway.step()
            elif event.key == pygame.K_p:
                auto_step = not auto_step
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > 0 and mouse_y > 0 and mouse_x < conway.px_full_width and mouse_y < conway.px_full_height:
                cell_pos_x = mouse_x // conway.px_cell_width
                cell_pos_y = mouse_y // conway.px_cell_height
                conway.toggle_cell(cell_pos_x, cell_pos_y)

    #screen.fill((255, 0, 255))

    if auto_step:
        conway.step()
    
    conway.draw()
    
    # Flip the display
    clock.tick(10)
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()