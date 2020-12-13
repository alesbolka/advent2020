from math import gcd
from itertools import combinations

def find_first_bus(raw_input):
  start_time, ids = raw_input
  start_time = int(start_time)
  busses = [int(xx) for xx in ids.split(",") if xx.isnumeric()]
  max_t = start_time + max(busses)
  time = start_time
  while time <= max_t:
    res = next((xx for xx in busses if (time % xx) < 1), None)
    if res != None:
      return res * (time - start_time)
    time += 1
  pass

def find_aligned_offset(raw_line):
  # (offset, interval), with no non-numeric values
  ids = [(ii, int(xx)) for ii, xx in enumerate(raw_line.split(",")) if xx.isnumeric()]

  # Lazy check to simplify script
  if max([gcd(xx, yy) for xx, yy in combinations([xx[1] for xx in ids], 2)]) > 1:
    raise Exception("not all numbers are primes")

  # start with the first element of the list as the result, it will be skipped immediately by the loop, as there is no leftover when dividing by 1
  res = ids[0][1]
  step = 1

  # go over each valid element of the input
  for off, num in ids:
    # Keep increasing the value by the step (lowest common multiple of all elements so far) until there is no leftover
    while (res + off) % num > 0:
      res += step
    # We found a match, increment the LCM
    step *= num

  return res
