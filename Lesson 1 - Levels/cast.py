import pygame
from math import pi, cos, sin


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 255, 255)


class Raycaster(object):
  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 50
    self.player = {
      "x": self.blocksize + 10,
      "y": self.blocksize + 10,
      "a": pi/2.2
    }
    self.map = []
    self.clear()

  def clear(self):
    for x in range(self.width):
      for y in range(self.height):
        r = int((x/self.width)*255) if x/self.width < 1 else 1
        g = int((y/self.height)*255) if y/self.height < 1 else 1
        b = 0
        color = (r, g, b)
        self.point(x, y, color)

  def point(self, x, y, c = None):
    screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, c):
    for cx in range(x, x + self.blocksize + 1):
      for cy in range(y, y + self.blocksize + 1):
        self.point(cx, cy, c)

  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  def render(self):
    for x in range(0, 500, 50):
      for y in range(0, 500, 50):
        i = int(x/50)
        j = int(y/50)
        if self.map[j][i] != ' ':
          self.draw_rectangle(x, y, (0, 255, 255))

    self.point(self.player["x"], self.player["y"], (255, 255, 255))


pygame.init()
screen = pygame.display.set_mode((500, 500))

r = Raycaster(screen)
r.load_map('./map.txt')

while True:
  r.render()

  pygame.display.flip()
