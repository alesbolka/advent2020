from copy import deepcopy
from math import sqrt
from itertools import combinations, product

Coords = tuple[int, int]
ProcessOrder = list[list[Coords]]

mp = {
  (0,0): '1951',
  (1,0): '2311',
  (2,0): '3079',

  (0,1): '2729',
  (1,1): '1427',
  (2,1): '2473',

  (0,2): '2971',
  (1,2): '1489',
  (2,2): '1171',
}

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

class Image:
  def __init__(self, img_id, content):
    self.id = img_id
    self.content = content

    l_x, l_y = len(content[0]), len(content)
    if l_x != l_y:
      raise Exception("Mismatched image dimensions")

    edges = {
      TT: content[0], # top
      RR: "".join([row[-1] for yy, row in enumerate(content)]), # right
      BB: content[-1], # bottom
      LL: "".join([row[0] for yy, row in enumerate(content)]), # left
    }

    self.combos = [
      { TT: edges[TT][:], RR: edges[RR][:], BB: edges[BB][:], LL: edges[LL][:] },
      { TT: edges[BB][:], RR: edges[RR][::-1], BB: edges[TT][:], LL: edges[LL][::-1] }, # X-axis flip
      { TT: edges[TT][::-1], RR: edges[LL][:], BB: edges[BB][::-1], LL: edges[RR][:] }, # Y-axis flip
      { TT: edges[BB][::-1], RR: edges[LL][::-1], BB: edges[TT][::-1], LL: edges[RR][::-1] }, # double axis flip
    ]

    self.flips = [
      deepcopy(self.content),
      [row for row in self.content[::-1]],
      [row[::-1] for row in self.content],
      [row[::-1] for row in self.content[::-1]],
    ]

    for jj in range(4):
      tmp = deepcopy(self.combos[jj])
      img_tmp = deepcopy(self.flips[jj])
      for ii in range(1,4):
        tmp = { (xx + 1) % 4: tmp[xx] for xx in tmp }
        tmp[TT] = tmp[TT][::-1]
        tmp[BB] = tmp[BB][::-1]
        new_img = []
        for xx in range(l_x):
          new_row = ""
          for yy in range(l_y):
            new_row += img_tmp[l_y - 1 - yy][xx]
          new_img.append(new_row)
        img_tmp = new_img

        if tmp not in self.combos:
          self.combos.append(tmp)
          self.flips.append(img_tmp)

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
    return self.flips[self.combos.index(self.active)]

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
    res = {}

    for yy in range(self.max + 1):
      row_res = []
      jj = 0
      for xx in range(self.max + 1):
        tmp = layout[(xx, yy)].correct_image()
        # print(len(tmp))
        for ii in range(1, len(tmp) - 1):
          row_index = ii + jj * len(tmp) - 1
          if row_index not in res:
            res[row_index] = ""
          res[row_index] += tmp[ii][1:-1]
        jj += 1
    full = Image("full_image", list(res.values()))

    # for xx in full.flips:
    #   print("\n".join(xx))
    #   print("")
    # exit()


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