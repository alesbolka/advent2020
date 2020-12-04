import re

hcl_regex = re.compile("^#[0-9a-f]{6}$", re.IGNORECASE)
pid_regex = re.compile("^[0-9]{9}$")

def create_numeric_validator(minV, maxV):
  def V(val):
    val = int(val)
    return val >= minV and val <= maxV
  return V

validate_height_cm = create_numeric_validator(150, 193)
validate_height_in = create_numeric_validator(59, 76)

def validate_height(val):
  unit = val[-2:]
  if unit == 'cm':
    return validate_height_cm(val[:-2])
  elif unit == 'in':
    return validate_height_in(val[:-2])

  return False

def validate_hcl(val):
  return hcl_regex.match(val)

def validate_ecl(val):
  valid_colours = [ "amb", "blu", "brn", "gry", "grn", "hzl", "oth" ]
  return val in valid_colours

def validate_pid(val):
  return pid_regex.match(val)


validators = {
  "byr": create_numeric_validator(1920, 2002),
  "iyr": create_numeric_validator(2010, 2020),
  "eyr": create_numeric_validator(2020, 2030),
  "hgt": validate_height,
  "hcl": validate_hcl,
  "ecl": validate_ecl,
  "pid": validate_pid
}
class Passport:
  def __init__(self):
    self.props = {
      "byr": "",
      "iyr": "",
      "eyr": "",
      "hgt": "",
      "hcl": "",
      "ecl": "",
      "pid": "",
      "cid": "",
    }
    pass

  def parse_line(self, line):
    pairs = [xx.split(":") for xx in line.split(" ")]
    for pair in pairs:
      self.props[pair[0]] = pair[1]

  def is_valid_basic(self):
    fields = [ "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid" ]
    for field in fields:
      if len(self.props[field]) < 1:
        return False

    return True

  def is_valid_adv(self):
    for field in validators:
      val = self.props[field]
      if len(val) < 1:
        return False

      if not validators[field](val):
        return False

    return True

def create_passport_list(raw_input):
  pp_list = []
  ii = 0
  pp_list.append(Passport())
  for line in raw_input:
    if len(line.strip()) < 1:
      ii += 1
      pp_list.append(Passport())
      continue

    pp_list[ii].parse_line(line)

  return pp_list

def count_valid_in_list(raw_input):
  pp_list = create_passport_list(raw_input)
  return sum(1 for pp in pp_list if pp.is_valid_adv())