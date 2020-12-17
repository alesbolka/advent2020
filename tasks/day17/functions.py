from itertools import product

class Matrix:
  def __init__(self, raw):
    self.on = [3]
    self.off = [2, 3]
    self.active = {}


    for yy, row in enumerate(raw):
      for xx, state in enumerate(row):
        if state == "#":
          yy = int(yy)
          xx = int(xx)
          self.active[(xx, yy, 0)] = 1

  def get_neighbours(self, xx, yy, zz):
    src = (xx, yy, zz)
    return [combo for combo in product([xx-1, xx, xx+1], [yy-1, yy, yy+1], [zz-1, zz, zz+1]) if combo != src]

  def __str__(self):
    xs = [xx for (xx, yy, zz) in self.active]
    ys = [yy for (xx, yy, zz) in self.active]
    zs = [zz for (xx, yy, zz) in self.active]

    out = "matrix output:\n"
    for zz in range(min(zs), max(zs) + 1):
      out += "z:{}\n".format(zz)
      for yy in range(min(ys), max(ys) + 1):
        for xx in range(min(xs), max(xs) + 1):
          out += "#" if (xx, yy, zz) in self.active else "."
        out += "\n"

    return out

  def should_be_active(self, current, neighbours):
    count = sum([1 for node in neighbours if node in self.active])
    if current in self.active:
      return count in self.off

    return count in self.on

  def validate_node(self, node, neighbours, checked, active):
    if node not in checked:
      checked[node] = self.should_be_active(node, neighbours)

    if checked[node]:
      active[node] = 1

  def step(self):
    new_active = {}
    checked = {}

    for current in self.active.keys():
      neighbours = self.get_neighbours(*current)
      self.validate_node(current, neighbours, checked, new_active)

      for other in neighbours:
        nei2 = self.get_neighbours(*other)
        self.validate_node(other, nei2, checked, new_active)

    self.active = new_active

  def simulate(self, steps):
    for _ in range(steps):
      self.step()

  def count_active(self):
    return sum(self.active.values())