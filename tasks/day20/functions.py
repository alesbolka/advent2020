from copy import deepcopy
from math import sqrt
from itertools import combinations, product

Coords = tuple[int, int]
Edge = list[int]
ProcessOrder = list[list[Coords]]

TT = 0 # top edge
RR = 1 # right edge
BB = 2 # bottom edge
LL = 3 # left edge
edge_map = {
  TT: BB,
  BB: TT,
  LL: RR,
  RR: LL,
}

class Image:
  def __init__(self, img_id, content):
    self.id = img_id
    self.content = content
    l_x, l_y = len(content[0]), len(content)
    edges = [
      [xx for xx, val in enumerate(content[0]) if val == "#"], # top
      [yy for yy, row in enumerate(content) if row[-1] == "#"], # right
      [xx for xx, val in enumerate(content[-1]) if val == "#"], # bottom
      [yy for yy, row in enumerate(content) if row[0] == "#"], # left
    ]

    self.combos: list[Edge] = [
      deepcopy(edges),
      [deepcopy(edges[BB]), deepcopy(edges[RR]), deepcopy(edges[TT]), deepcopy(edges[LL])], # X-axis flip
      [deepcopy(edges[TT]), deepcopy(edges[LL]), deepcopy(edges[BB]), deepcopy(edges[RR])], # Y-axis flip
      [deepcopy(edges[BB]), deepcopy(edges[LL]), deepcopy(edges[TT]), deepcopy(edges[RR])], # double axis flip
    ]

    # manually reverse the relevant edges
    self.combos[1][LL].reverse()
    self.combos[1][RR].reverse()

    self.combos[2][TT].reverse()
    self.combos[2][BB].reverse()

    self.combos[3][TT].reverse()
    self.combos[3][BB].reverse()
    self.combos[3][LL].reverse()
    self.combos[3][RR].reverse()

    self.rotation = 0
    self.cfg = 0

  def get_edge(self, direction: int):
    return self.combos[self.cfg][(direction + self.rotation) % 4]

  def fits(self, reqs: dict[int, list[int]]):
    matches = []
    for rotation in range(4):
      for cfg, edges in enumerate(self.combos):
        layout = { req_dir: edges[(req_dir + rotation) % 4] for req_dir in reqs }
        if layout == reqs:
          matches.append((rotation, cfg))

    return matches


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
    self.neighbours: dict[Coords, list[Coords]] = {}
    for node in self.coords:
      xx, yy = node
      self.neighbours[node] = {pos: node for pos, node in {LL: (xx-1, yy), RR: (xx+1, yy), TT: (xx, yy-1), BB: (xx, yy+1)}.items() if node in self.coords}

    center = (int(dimension/2), int(dimension/2))
    # We can always rotate this one with the entire composition if it matches, so its orientation does not matter
    self.coords.remove(center)

    order = self.get_order(center)
    self.full_check(center, order)

  def get_order(self, start: Coords) -> ProcessOrder:
    order = []
    used = [start]
    limit = len(self.coords) + 1

    todo = [start]
    while len(todo) > 0:
      node = todo.pop(0)
      new_list = [xx for xx in self.neighbours[node].values() if xx not in used]
      if len(new_list) < 1:
        continue
      order.append(new_list)
      todo += order[-1]
      used += order[-1]

    return order

  def full_check(self, center: Coords, order: ProcessOrder):
    for parent in self.all:
      parent.rotation = 0
      layout = {
        center: parent
      }
      self.rec_check(layout, order)
      exit()

  def rec_check(self, layout: dict[Coords, Image], order: ProcessOrder, ord_step = 0, ord_pos = 0):
    remaining: list[Image] = [node for node in self.all if node not in layout.keys()]

    pos = order[ord_step][ord_pos]
    for img in remaining:
      fits = self.possible_fits(layout, pos, img)
      print(fits)
      exit()

  def possible_fits(self, layout: dict[Coords, Image], node: Coords, img: Image):
    reqs = {}

    for edge_id, nei in self.neighbours[node].items():
      if nei not in layout:
        # Nothing there yet, automatic pass
        continue

      reqs[edge_id] = layout[nei].get_edge(edge_map[edge_id])
    return img.fits(reqs)


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