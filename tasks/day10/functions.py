def all_adapters_jumps(raw_input, start = 0):
  adapters = list(map(lambda xx: int(xx), raw_input))
  adapters.sort()

  prev = start
  jumps = {
    3: 1, # last jump
  }
  for ii in range(len(adapters)):
    jump = adapters[ii] - prev
    prev = adapters[ii]

    if not jump in jumps:
      jumps[jump] = 0

    jumps[jump] += 1

  return jumps


def all_possible_combinations(raw_input):
  raw = [0] + list(map(lambda xx: int(xx), raw_input))
  raw.sort()

  memory = {
    0: 1,
  }
  for ii in range(len(raw)):
    count = 0

    if raw[ii] in memory:
      continue

    jj = ii - 1
    while jj >= 0 and ii > 0:
      diff = raw[ii] - raw[jj]
      if diff < 0:
        raise Exception("Invalid values", raw[ii], raw[jj])

      jj -= 1
      if diff == 0:
        continue
      elif diff > 3:
        break

      count += memory[raw[jj + 1]]

    memory[raw[ii]] = count

  return memory[raw[-1]]


  # def find_next(path):
  #   ii = path[-1]
  #   for jj in range(ii + 1, max_l):
  #     diff = raw[jj] - raw[ii]
  #     if diff > 3:
  #       return
  #     if raw[jj] == target:
  #       new_path = path.copy()
  #       new_path.append(jj)
  #       res.append([raw[xx] for xx in new_path])
  #       continue # in case there are duplicates of last element

  #     new_path = path.copy()
  #     new_path.append(jj)
  #     find_next(new_path)

  # find_next([0])

  # return res

  # res = []

  #   pass

  # for ii in range(len(raw)):

  #   jj = -1
  #   while (ii + jj) >= 0 and (raw[ii] - raw[ii + jj]) <= 3:
  #     jj -= 1


