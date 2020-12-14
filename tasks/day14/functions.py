import re

instruction_regex = re.compile(r"^mem\[([0-9]+)\]\s*=\s*([0-9]+)")



def apply_bitmap(raw_input, int_length = 36):
  def parse_mask(row):
    mask_raw = row.split("=")[1]
    return [(ii - 1, int(bit)) for ii, bit in enumerate(mask_raw) if bit.isnumeric()]
  def parse_instruction(row):
    match = instruction_regex.match(row)
    if not match:
      raise Exception("regex parse failed on {}".format(row))
    index, value = match.groups()
    value = list("{0:b}".format(int(value)).zfill(int_length)) # convert to raw binary
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
