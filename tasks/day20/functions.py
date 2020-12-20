from copy import deepcopy
from math import sqrt
from itertools import combinations, product
import re

Coords = tuple[int, int]
ProcessOrder = list[list[Coords]]
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

raw_monster = """                  #
#    ##    ##    ###
 #  #  #  #  #  #   """
monster_size = 0
monster = []
for line in raw_monster.split("\n"):
  line = line.replace(" ", ".")
  monster_size += line.count("#")
  monster.append(re.compile("(?=(" + line + "))"))

def find_monsters(img):
  res = 0
  # Not adapted to monsters taller than 3!
  for ii in range(1, len(img) - 1):
    m1 = [match.start(0) for match in monster[1].finditer(img[ii])]
    # the middle line has the most # symbols, so should be the fastest to process
    if len(m1) < 1:
      continue

    m0 = [match.start(0) for match in monster[0].finditer(img[ii-1])]
    if len(m0) < 1:
      continue

    m2 = [match.start(0) for match in monster[0].finditer(img[ii+1])]
    if len(m2) < 1:
      continue

    res += len([xx for xx in m0 if xx in m1 and xx in m2]) > 0

  return res

def count_roughness(img):
  global monster_size
  max_c = 0
  total_artifacts = "".join(img).count("#")
  max_monsters = 0
  for ii in range(4):
    # rotate
    img = rotate(img)
    max_monsters = max(max_monsters, find_monsters(img))

    # flip by X axis
    img = flipX(img)
    max_monsters = max(max_monsters, find_monsters(img))

    # flip by Y axis
    img = flipY(img)
    max_monsters = max(max_monsters, find_monsters(img))

    # Flip back to original position
    img = flipXY(img)
    max_monsters = max(max_monsters, find_monsters(img))

  return total_artifacts - max_monsters * monster_size

def rotate(rows):
  return ["".join([rows[yy][xx] for yy in range(len(rows) - 1, -1, -1)]) for xx in range(len(rows)) ]
def flipX(rows):
  return [rows[yy] for yy in range(len(rows) - 1, -1, -1)]
def flipY(rows):
  return [row[::-1] for row in rows]
def flipXY(rows):
  return flipX(flipY(rows))
def calc_edge(rows):
  return {
    TT: rows[0], # top
    RR: "".join([row[-1] for row in rows]), # right
    BB: rows[-1], # bottom
    LL: "".join([row[0] for row in rows]), # left
  }

class Image:
  def __init__(self, img_id, content):
    self.id = img_id
    self.content = []
    self.combos = []

    l_x, l_y = len(content[0]), len(content)
    if l_x != l_y:
      raise Exception("Mismatched image dimensions")

    for ii in range(4):
      # rotate
      content = rotate(content)
      edges = calc_edge(content)
      if edges not in self.combos:
        self.combos.append(edges)
        self.content.append(content)

      # flip by X axis
      content = flipX(content)
      edges = calc_edge(content)
      if edges not in self.combos:
        self.combos.append(edges)
        self.content.append(content)

      # flip by Y axis
      content = flipY(content)
      edges = calc_edge(content)
      if edges not in self.combos:
        self.combos.append(edges)
        self.content.append(content)

      # Flip back to original position
      content = flipXY(content)
      edges = calc_edge(content)
      if edges not in self.combos:
        self.combos.append(edges)
        self.content.append(content)

    self.active = self.combos[0]

  def get_edge(self, direction):
    return self.active[direction]

  def fits(self, reqs: dict[int, list[int]]):
    matches = []
    for layout in self.combos:
      if reqs == { req_dir: layout[req_dir] for req_dir in reqs }:
        matches.append(layout)

    return matches

  def lock(self, orientation):
    if orientation not in self.combos:
      raise Exception("invalid orientation used")
    self.active = orientation
    return self

  def correct_image(self):
    return self.content[self.combos.index(self.active)]

class Collection:
  def __init__(self):
    self.all: list[Image] = []

  def add(self, img):
    self.all.append(img)

  def compose(self):
    dimension = int(sqrt(len(self.all)))
    if dimension ** 2 != len(self.all):
      # Sensitive due to float btw, might error unnecessarily
      print("{:0.2f} is not a valid dimension (sqrt of {})".format(dimension, len(self.all)))
      raise Exception("Invalid input")

    self.coords: list[Coords] = list(product(range(0, dimension), range(0, dimension)))
    self.neighbours: dict[Coords, dict[int, Coords]] = {}
    self.max = dimension - 1

    for node in self.coords:
      xx, yy = node
      self.neighbours[node] = {pos: node for pos, node in {LL: (xx-1, yy), RR: (xx+1, yy), TT: (xx, yy-1), BB: (xx, yy+1)}.items() if node in self.coords}
    center = (int(dimension/2), int(dimension/2))
    # We can always rotate this one with the entire composition if it matches, so its orientation does not matter
    self.coords.remove(center)

    order = self.get_order(center)
    layout = self.full_check(center, order)
    if not layout:
      return None

    img = self.build_images(layout)

    aa = int(layout[(0, 0)].id)
    bb = int(layout[(self.max, 0)].id)
    cc = int(layout[(0, self.max)].id)
    dd = int(layout[(self.max, self.max)].id)

    return (aa * bb * cc * dd, img)

  def get_order(self, start: Coords) -> ProcessOrder:
    order = []
    limit = len(self.coords) + 1

    todo = [start]
    while len(todo) > 0:
      node = todo.pop(0)
      for ngb in self.neighbours[node].values():
        if ngb not in order:
          order.append(ngb)
          todo.append(ngb)

    order.remove(start)

    return order

  def full_check(self, center: Coords, order: ProcessOrder):
    for parent in self.all:
      for src in parent.combos:
        layout = {
          center: parent.lock(src),
        }
        correct = self.rec_check(layout, order)
        if correct:
          return correct

  def rec_check(self, layout: dict[Coords, Image], order: ProcessOrder, step = 0):
    remaining = [node for node in self.all if node not in layout.values()]
    if step >= len(order):
      return layout
    pos = order[step]

    for img in remaining:
      fits = self.possible_fits(layout, pos, img)
      if len(fits) < 1:
        # img cannot fit into this position
        continue

      for fit in fits:
        l2 = layout.copy()
        l2[pos] = img.lock(fit)
        res = self.rec_check(l2, order, step + 1)
        if res:
          return res

  def possible_fits(self, layout: dict[Coords, Image], node: Coords, img: Image):
    reqs = {}
    for edge_id, nei in self.neighbours[node].items():
      if nei not in layout:
        # Nothing there yet, automatic pass
        continue

      reqs[edge_id] = layout[nei].get_edge(edge_map[edge_id])
    return img.fits(reqs)

  def build_images(self, layout):
    max_ii = None
    res = []
    for yy in range(self.max + 1):
      sub_results = []
      for xx in range(self.max + 1):
        rows = layout[(yy,xx)].correct_image()
        if not max_ii:
          max_ii = len(rows)
        sub_results.append(rows)


      for xy in range(1, max_ii - 1):
        res.append("")
        for segment in sub_results:
          res[-1] += segment[xy][1:-1]

    return res


def parse_images(raw_input):
  img_id = ""
  img = []
  imgs = Collection()
  for row in raw_input:
    if row.startswith("Tile "):
      img_id = row[5:-1]
      continue
    elif len(row) < 1:
      imgs.add(Image(img_id, img))
      img_id = ""
      img = []
      continue

    img.append(row)

  if img_id != "":
    imgs.add(Image(img_id, img))
    img_id = ""
    img = []
  return imgs