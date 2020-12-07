class Bag:
  def __init__(self, colour):
    self.colour = colour
    self.parents = {}
    self.children = {}

  def add_parent(self, bag):
    if bag.colour not in self.parents:
      self.parents[bag.colour] = bag

  def add_child(self, bag, count):
    if bag.colour not in self.children and bag.colour != "no other":
      self.children[bag.colour] = (bag, count)
      bag.add_parent(self)

  def get_parents(self, res = {}):
    for parent_colour in self.parents:
      if parent_colour not in res:
        res[parent_colour] = True
        res = self.parents[parent_colour].get_parents(res)

    return res

  def count_bags_inside(self, raw_map = {}):
    if self.colour in raw_map:
      return raw_map[self.colour]

    total = 0

    for child_colour in self.children:
      if child_colour not in raw_map:
        self.children[child_colour][0].count_bags_inside(raw_map)

      print("{} -> {}: {}".format(self.colour, child_colour, raw_map[child_colour]))
      total += (raw_map[child_colour] + 1) * self.children[child_colour][1]

    raw_map[self.colour] = total
    return total

class Collection:
  def __init__(self):
    self.bags = {}

  def get_bag(self, colour):
    if colour not in self.bags:
      self.bags[colour] = Bag(colour)

    return self.bags[colour]

  def get_parents(self, colour):
    return list(self.bags[colour].get_parents().keys())

  def get_bags_in_bag(self, colour):
    return self.bags[colour].count_bags_inside()

def parse_bag_string(st):
  if st == "no other bags":
    return (0, "no bags")

  count = 1
  parts = st.split(" ")
  if parts[0].isnumeric():
    count = int(parts[0])
    parts = parts[1:]

  if parts[-1] in ["bag", "bag.", "bag,", "bags", "bags.", "bags"]:
    parts = parts[:-1]

  return (count, " ".join(parts))

def parse_rules(raw_input):
  col = Collection()
  for rule in raw_input:
    pairs = [parse_bag_string(yy.strip()) for xx in rule.split("contain") for yy in xx.split(",")]
    parent = col.get_bag(pairs[0][1])
    for tup in pairs[1:]:
      child = col.get_bag(tup[1])
      parent.add_child(child, tup[0])

  return col
