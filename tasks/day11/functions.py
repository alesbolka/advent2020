def parse_seats(raw_input):
  seats = {}
  neighbours = {}
  visible = {}

  for yy in range(len(raw_input)):
    for xx in range(len(raw_input[yy])):
      seat = raw_input[yy][xx]
      if seat == "L" or seat == "#":
        seats[(xx, yy)] = seat == "#"

  for seat in seats:
    neighbours[seat] = [(yy, xx) for yy in range(seat[0]-1, seat[0]+2) for xx in range(seat[1] - 1, seat[1] + 2) if (yy, xx) != seat and (yy, xx) in seats]
    visible[seat] = []

    for mod_yy in [-1, 0, 1]:
      for mod_xx in [-1, 0, 1]:
        if mod_yy == 0 and mod_xx == 0:
          continue
        xx, yy = seat

        while yy >= 0 and yy < len(raw_input) and xx >= 0 and xx < len(raw_input[yy]):
          yy += mod_yy
          xx += mod_xx
          if (xx, yy) in seats:
            visible[seat].append((xx, yy))
            break

  return (seats, neighbours, visible)

def iteration(seats, considerable, empty_thresh):
  newseats = seats.copy()
  changed = False
  for seat in seats:
    occupied = sum([1 for other in considerable[seat] if seats[other]])
    if occupied < 1 and not newseats[seat]:
      changed = True
      newseats[seat] = True
    elif occupied >= empty_thresh and newseats[seat]:
      changed = True
      newseats[seat] = False

  return (changed, newseats)

def iterate_till_stable(seats, considerable, empty_thresh = 4, max_iter = 10000):
  ok = True
  ii = 0
  while ok:
    ii+=1
    if ii >= max_iter:
      raise Exception("Too many iterations")
    ok, seats = iteration(seats, considerable, empty_thresh)

  return sum([1 for seat in seats if seats[seat]])

