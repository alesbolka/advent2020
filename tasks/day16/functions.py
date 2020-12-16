def parse_rule(text):
  parts = []
  for part in text.split(" or "):
    pair = part.split("-")
    parts.append((int(pair[0]), int(pair[1])))
  return parts

def validate_ticket(ticket, rules):
  err = 0
  for num in ticket:
    match = False
    for name in rules:
      if match:
        break

      for low, high in rules[name]:
        if low <= num and num <= high:
          match = True
          break

    if not match:
      err += num
  return err

def parse_tickets(raw_input):
  rules = {}
  handling_mine = False
  my_ticket = [];
  valid_tickets = []
  err_rate = 0

  for row in raw_input:
    if len(row) < 1:
      continue
    if row.strip() == 'your ticket:':
      handling_mine = True
      continue
    elif handling_mine:
      my_ticket = [int(xx) for xx in row.split(",")]
      handling_mine = False
      continue

    if row.strip() == 'nearby tickets:':
      continue

    parts = [xx.strip() for xx in row.split(":")]

    if len(parts) < 2:
      ticket = [int(xx) for xx in row.split(",")]
      invalid_rate = validate_ticket(ticket, rules)
      err_rate += invalid_rate
      if invalid_rate > 0:
        continue
      valid_tickets.append(ticket)
    elif len(parts[1]) > 0:
      rules[parts[0]] = parse_rule(parts[1])
    else:
      raise Exception("invalid input {}".format(row))

  return err_rate, my_ticket, valid_tickets, rules

def validate_position(numbers, rules):
  for num in numbers:
    match = False
    for low, high in rules:
      if low <= num and num <= high:
        match = True

    if not match:
      return False

  return True

def identify_fields(rules, tickets):
  if len(tickets) < 1:
    return {}


  mem = {}
  for pos in range(len(tickets[0])):
    # if pos != 6:
    #   continue



    values = [ticket[pos] for ticket in tickets]
    for name, pairs in rules.items():
      if name not in mem:
        mem[name] = []

      if validate_position(values, pairs):
        mem[name].append(pos)

  combos = list(mem.items())
  combos.sort(key=lambda it: len(it[1]))

  res = {}
  for ii in range(len(combos)):
    pos, possible = combos[ii]
    print(pos, len(possible), possible)

    # if len(possible) != 1:
      # print(pos, possible)
      # raise Exception("Mistakes were made")

    # res[pos] = possible[0]

    # for jj in range(ii + 1, len(combos)):
    #   combos[jj][1].remove(possible[0])

  return res