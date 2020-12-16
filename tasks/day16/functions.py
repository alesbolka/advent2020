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

  return err_rate, my_ticket, valid_tickets