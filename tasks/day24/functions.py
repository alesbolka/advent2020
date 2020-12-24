# https://www.redblobgames.com/grids/hexagons/#coordinates-cube
# Decided to use cube coord system

from itertools import product

directions = {
  "e": (1, -1, 0),
  "ne": (1, 0, -1),
  "se": (0, -1, 1),
  "w": (-1, 1, 0),
  "nw": (0, 1, -1),
  "sw": (-1, 0, 1),
}

class Coord:
  def __init__(self):
    self.xyz = (0, 0, 0)

  def move(self, direction):
    global directions
    dr = directions[direction]
    self.xyz = tuple(val + dr[ii] for ii, val in enumerate(self.xyz))

class Grid:
  def __init__(self):
    self.tiles = {}
    self.flips = 0
    self.neigbhours = {}

  def flip(self, coords):
    if coords not in self.tiles:
      self.tiles[coords] = 0

    self.tiles[coords] = (self.tiles[coords] + 1) % 2
    self.flips += 1

  def count_black(self):
    return sum(self.tiles.values())

  def get_neighbours(self, crd):
    global directions
    if crd not in self.neigbhours:
      self.neigbhours[crd] = [tuple(val + directions[dr][ii] for ii, val in enumerate(crd)) for dr in directions]
    return self.neigbhours[crd]

  def daily(self):
    new = {}
    for crd, active in self.tiles.items():
      neighbours = self.get_neighbours(crd)
      if crd not in new:
        new[crd] = self.check(crd, neighbours)
      for nei in neighbours:
        if nei not in new:
          new[nei] = self.check(nei, self.get_neighbours(nei))


    self.tiles = new

  def check(self, current, neighbours):
    active_nei = sum([self.tiles.get(nei, 0) for nei in neighbours])
    active = self.tiles.get(current, 0)
    if active and active_nei not in [1, 2]:
      return 0
    elif not active and active_nei == 2:
      return 1

    return active



def parse_input(raw):
  grid = Grid()
  for row in raw:
    ii = 0
    crd = Coord()
    while ii < len(row):
      cmd = row[ii]
      if cmd in ["s", "n"]:
        ii += 1
        cmd += row[ii]

      crd.move(cmd)
      ii += 1
    grid.flip(crd.xyz)
  return grid

def part1(raw):
  grid = parse_input(raw)
  print(grid.count_black())

def part2(raw, iterations = 100):
  grid = parse_input(raw)
  for ii in range(iterations):
    grid.daily()

  print(grid.count_black())