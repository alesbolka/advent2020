from copy import deepcopy
from math import sqrt
from itertools import combinations, product
import re

TT = 0 # top edge
RR = 1 # right edge4
BB = 2 # bottom edge
LL = 3 # left edge
edge_map = {
  TT: BB,
  BB: TT,
  LL: RR,
  RR: LL,
}

def parse_input(raw_input):
  can = Canvas()
  title = ""
  img_rows = []

  for row in raw_input:
    if row.strip() == "":
      can.add(Image(title, img_rows))
      title = ""
      img_rows = []
    elif row.startswith("Tile "):
      title = row[5:-1]
    else:
      img_rows.append(row)

  if len(title) > 0:
    can.add(Image(title, img_rows))

  return can

def rotate(rows):
  return ["".join([rows[yy][xx] for yy in range(len(rows) - 1, -1, -1)]) for xx in range(len(rows)) ]

def flip(rows):
  return [rows[yy] for yy in range(len(rows) - 1, -1, -1)]

def calc_edge(rows):
  return {
    TT: rows[0], # top
    RR: "".join([row[-1] for row in rows]), # right
    BB: rows[-1], # bottom
    LL: "".join([row[0] for row in rows]), # left
  }

expected = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###"""

class Image:
  def __init__(self, img_id, content):
    self.id = img_id
    self.content = []
    self.orientation = 0

    for _ in range(2):
      content = flip(content)
      for _ in range(4):
        content = rotate(content)
        self.content.append({ "content": content, "edges": calc_edge(content) })

  def reset(self):
    self.orientation = 0
    return self

  def iterate(self):
    for ii in range(len(self.content)):
      self.orientation = ii
      yield ii

  def check(self, pos, neighbours):
    # dr = direction nei is in relative to pos
    for dr, nei, img in neighbours:
      my_edge = self.get_edge(dr)
      other_edge = img.get_edge(edge_map[dr])
      if my_edge != other_edge:
        return False
    return True

  def get_edge(self, side):
    return self.content[self.orientation]["edges"][side]

  def get_current(self, join = False):
    if join:
      return "\n".join(self.content[self.orientation]["content"])
    return self.content[self.orientation]["content"]

class Canvas:
  def __init__(self):
    self.imgs = []
    self.neighbours = {}

  def add(self, img):
    self.imgs.append(img)

  def compose(self):
    self.prep_grid()
    res = self.recurse({}, self.order[:])
    if not res:
      return None

    return self.glue(res)

  def prep_grid(self):
    dimension = int(sqrt(len(self.imgs)))
    if dimension ** 2 != len(self.imgs):
      # Sensitive due to float btw, might error unnecessarily
      print("{:0.2f} is not a valid dimension (sqrt of {})".format(dimension, len(self.imgs)))
      raise Exception("Invalid input")

    self.dimension = dimension
    self.coords = list(product(range(0, dimension), range(0, dimension)))
    self.neighbours = {}
    for node in self.coords:
      xx, yy = node
      self.neighbours[node] = {pos: node for pos, node in {LL: (xx-1, yy), RR: (xx+1, yy), TT: (xx, yy-1), BB: (xx, yy+1)}.items() if node in self.coords}

    center = int(dimension / 2)

    self.order = [(center, center)]

    todo = [(center, center)]
    while len(todo) > 0:
      node = todo.pop(0)
      for ngb in self.neighbours[node].values():
        if ngb not in self.order:
          self.order.append(ngb)
          todo.append(ngb)

  def recurse(self, layout, order):
    if len(order) < 1:
      return layout
    l2 = layout.copy()

    pos = order[0]
    remaining = [img for img in self.imgs if img not in l2.values()]
    current_neighbours = [(dr, px, l2[px]) for dr, px in self.neighbours[pos].items() if px in l2]
    for img in remaining:
      l2[pos] = img.reset()
      for _ in img.iterate():
        if img.check(pos, current_neighbours):
          res = self.recurse(l2, order[1:])
          if res:
            return res

    return None

  def glue(self, layout):
    multi = (
      int(layout[0, 0].id) *
      int(layout[self.dimension - 1, 0].id) *
      int(layout[0, self.dimension - 1].id) *
      int(layout[self.dimension - 1, self.dimension - 1].id)
    )
    res = []
    for xx in range(self.dimension):
      row = []
      for yy in range(self.dimension):
        img = layout[(xx, yy)].get_current()
        for img_row in img[1:-1]:
          row.append(img_row[1:-1])
      if len(res) < 1:
        res += row
      else:
        for ii in range(len(row)):
          res[ii] += row[ii]

    return Image("{}".format(multi), res)

raw_monster = """                  #
#    ##    ##    ###
 #  #  #  #  #  #   """

def find_monsters(image: Image):
  monster = [
    re.compile(r"(?=(.{18}#.))"),
    re.compile(r"(?=(#.{4}##.{4}##.{4}###))"),
    re.compile(r"(?=(.#..#..#..#..#..#...))"),
  ]
  monster_size = 15
  wave_count = image.get_current(True).count("#")
  max_res = 0

  for _ in image.iterate():
    img = image.get_current()
    res = 0
    for ii in range(1, len(img) - 1):
      # This regex is the most restrictive, so it will rule out the most errors
      m1 = [match.start(0) for match in monster[1].finditer(img[ii])]
      if len(m1) < 1:
        continue

      m2 = [match.start(0) for match in monster[2].finditer(img[ii+1])]
      if len(m2) < 1:
        continue

      m0 = [match.start(0) for match in monster[0].finditer(img[ii-1])]
      if len(m0) < 1:
        continue

      for xx in m1:
        if xx not in m0 or xx not in m2:
          continue
        res += 1

    max_res = max(res, max_res)

  return wave_count - monster_size * max_res


def find_monsters_dynamic(img: Image, pattern):
  raise Exception("Does not work")
  monster_size = 0
  monster = []
  for line in pattern.split("\n"):
    line = line.replace(" ", ".")
    monster_size += line.count("#")
    monster.append(re.compile("(?=(" + line + "))"))
  scan_range = range(len(monster))
  offset = len(monster) - 1
  wave_count = img.get_current(True).count("#")

  for _ in img.iterate():
    lines = img.get_current()
    monsters = 0
    for ii in range(len(lines)):
      if ii < len(monster) -1:
        continue

      matches = []
      for jj in scan_range:
        scan_index = ii - offset + jj
        matches.append([match.start(0) for match in monster[jj].finditer(lines[scan_index])])

      if len([xx for xx in matches[0] for other in matches[1:] if xx in other]) > 0:
        monsters +=1

  return wave_count - monsters * monster_size