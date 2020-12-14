import re
from itertools import product

instruction_regex = re.compile(r"^mem\[([0-9]+)\]\s*=\s*([0-9]+)")

def apply_bitmap_v1(raw_input):
  def parse_mask(row):
    mask_raw = row.split("=")[1]
    return [(ii - 1, int(bit)) for ii, bit in enumerate(mask_raw) if bit.isnumeric()]

  def parse_instruction(row):
    match = instruction_regex.match(row)
    if not match:
      raise Exception("regex parse failed on {}".format(row))
    index, value = match.groups()
    value = list("{0:b}".format(int(value)).zfill(36)) # convert to raw binary
    return (index, value)

  mask = []
  mem = {}

  for row in raw_input:
    if row.startswith("mask"):
      mask = parse_mask(row)
    elif row.startswith("mem"):
      index, value = parse_instruction(row)
      for ii, bit in mask:
        value[ii] = "{}".format(bit)
      mem[index] = "".join(value)

  return sum([int(xx, 2) for xx in mem.values()])

def apply_bitmap_v2(raw_input):
  mem = {}
  masks = []

  def parse_instruction(row):
    match = instruction_regex.match(row)
    if not match:
      raise Exception("regex parse failed on {}".format(row))
    index, value = match.groups()
    value = int(value)
    index = list("{0:b}".format(int(index)).zfill(36)) # convert to raw binary
    return (index, value)

  def parse_mask(row):
    mask_raw = row.split("=")[1].strip()
    dynamic = [] # list of indexes with dynamic entries
    static = [] # list of static masks
    tmp = [] # helper values for itertools.product

    for ii in range(len(mask_raw)):
      if mask_raw[ii].isnumeric():
        if int(mask_raw[ii]) == 1:
          static.append((ii, 1))
      elif mask_raw[ii].lower() == "x":
        dynamic.append(ii)
        tmp.append([0, 1])

    # all possible dynamic mask combinations
    return [
      static + [
        (dynamic[ii], val) for ii, val in enumerate(combo)
      ] for combo in list(product(*tmp))
    ]

  def modify_index(index_list, val):
    for mask in masks:
      copy = index_list.copy()
      for pair in mask:
        copy[pair[0]] = "{}".format(pair[1])
      mem["".join(copy)] = val

  for row in raw_input:
    if row.startswith("mask"):
      masks = parse_mask(row)
    elif row.startswith("mem"):
      modify_index(*parse_instruction(row))

  return sum(mem.values())