import pygame
from math import pi, cos, sin


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 255, 255)

colors = {
  "1": (146, 60, 63),
  "2": (233, 70, 63),
  "3": (0, 130, 168)
}

class Raycaster(object):
  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 50
    self.player = {
      "x": self.blocksize + 20,
      "y": self.blocksize + 20,
      "a": pi/3,
      "fov": pi/3
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

  def cast_ray(self, a):
    d = 0
    while True:
      x = self.player["x"] + d*cos(a)
      y = self.player["y"] + d*sin(a)
      x = int(x)
      y = int(y)

      i = int(x/50)
      j = int(y/50)

      if self.map[j][i] != ' ':
        return d, self.map[j][i]

      self.point(x, y, (255, 255, 255))

      d += 10

  def draw_stake(self, x, h, c):
    # draw a stake with x, y at the middle

    start = int(250 - h/2)
    end = int(250 + h/2)
    for y in range(start, end):
      self.point(x, y, c)


  def render(self):
    for x in range(0, 500, 50):
      for y in range(0, 500, 50):
        i = int(x/50)
        j = int(y/50)
        if self.map[j][i] != ' ':
          self.draw_rectangle(x, y, colors[self.map[j][i]])

    self.point(self.player["x"], self.player["y"], (255, 255, 255))

    for i in range(0, 500):
      self.point(500, i, (0, 0, 0))
      self.point(501, i, (0, 0, 0))
      self.point(499, i, (0, 0, 0))

    for i in range(1, 500):
      a =  self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/500
      d, c = self.cast_ray(a)
      x = 500 + i
      h = 500/(d*cos(a-self.player["a"])) * 100
      self.draw_stake(x, h, colors[c])

pygame.init()
screen = pygame.display.set_mode((1000, 500)) #, pygame.FULLSCREEN)

r = Raycaster(screen)
r.load_map('./map.txt')

c = 0
while True:
  r.clear()
  r.render()
  c+=1
  if c == 5:
    assert False, 1

  for e in pygame.event.get():
    if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
      exit(0)
    if e.type == pygame.KEYDOWN:
      if e.key == pygame.K_a:
        r.player["a"] -= pi/10
      elif e.key == pygame.K_d:
        r.player["a"] += pi/10

      elif e.key == pygame.K_RIGHT:
        r.player["x"] += 10
      elif e.key == pygame.K_LEFT:
        r.player["x"] -= 10
      elif e.key == pygame.K_UP:
        r.player["y"] += 10
      elif e.key == pygame.K_DOWN:
        r.player["y"] -= 10

  pygame.display.flip()
