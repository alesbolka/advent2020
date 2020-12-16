def parse_rule(text):
  parts = []
  for part in text.split(" or "):
    pair = part.split("-")
    parts.append((int(pair[0]), int(pair[1])))
  return parts

def validate_ticket(ticket, rules):
  err = 0
  had_errors = False
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
      had_errors = True
      err += num
  return err, had_errors

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

      invalid_rate, had_errs = validate_ticket(ticket, rules)
      err_rate += invalid_rate

      if had_errs > 0:
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


  by_pos = {}
  by_rule = {}
  res = {}

  for pos in range(len(tickets[0])):
    if pos not in by_pos:
      by_pos[pos] = []

    values = [ticket[pos] for ticket in tickets]
    for name, pairs in rules.items():
      if name not in by_rule:
        by_rule[name] = []

      if validate_position(values, pairs):
        by_pos[pos].append(name)
        by_rule[name].append(pos)

  by_pos = list(by_pos.items())
  by_pos.sort(key=lambda it: len(it[1]))
  by_rule = list(by_rule.items())
  by_rule.sort(key=lambda it: len(it[1]))

  abort_time = len(by_pos) + len(by_rule) + 2
  xx = 0
  while len(by_pos) > 0 or len(by_rule) > 0:
    xx += 1
    if xx > abort_time:
      raise Exception("too many iterations")

    if len(by_pos) > 0:
      el = by_pos[0]

      if len(el[1]) < 1:
        by_pos.pop(0)
        continue

      if len(el[1]) == 1:
        name = el[1][0]
        pos = el[0]
        by_pos.pop(0)

        res[name] = pos
        for ii in range(len(by_pos)):
          if name in by_pos[ii][1]:
            by_pos[ii][1].remove(name)
        for ii in range(len(by_rule)):
          if pos in by_rule[ii][1]:
            by_rule[ii][1].remove(pos)
        continue

    if len(by_rule) > 0:
      el = by_rule[0]

      if len(el[1]) < 1:
        by_rule.pop(0)
        continue

      if len(el[1]) == 1:
        pos = el[1][0]
        name = el[0]
        by_rule.pop(0)
        res[name] = pos
        for ii in range(len(by_pos)):
          if name in by_pos[ii][1]:
            by_pos[ii][1].remove(name)
        for ii in range(len(by_rule)):
          if pos in by_rule[ii][1]:
            by_rule[ii][1].remove(pos)
        continue

  return res

def multiply_departure_fields(ticket, legend):
  res = 1
  for field in legend:
    if field.startswith("departure"):
      res *= ticket[legend[field]]

  return res