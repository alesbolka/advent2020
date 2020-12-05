def validate_line_repeats(line):
  rules_string, password = [part.strip() for part in line.split(":")]
  rules = [rule.split(" ") for rule in rules_string.split(",")]

  for rule in rules:
    low, high = [int(xx) for xx in rule[0].split("-")]
    lcount = password.count(rule[1])
    if lcount < low or lcount > high:
      return False

  return True

def validate_line_positions(line):
  rules_string, password = [part.strip() for part in line.split(":")]
  rules = [rule.split(" ") for rule in rules_string.split(",")]


  for rule in rules:
    ii, jj = [(int(xx) - 1) for xx in rule[0].split("-")]
    if len(password) < ii or len(password) < jj:
      return False
    aa, bb = password[ii], password[jj]
    if aa != rule[1] and bb != rule[1] or aa == rule[1] and aa == bb:
      return False

  return True

def count_valid_repeats(lines):
  return len([line for line in lines if validate_line_repeats(line)])

def count_valid_positions(lines):
  return len([line for line in lines if validate_line_positions(line)])
