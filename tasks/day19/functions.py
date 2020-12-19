import re

letter_regex = re.compile(r"\"([a-zA-Z]+)\"")
id_list_regex = re.compile(r"([0-9]+)")

class RuleSystem:
  def __init__(self, raw_input, with_loops = False):
    self.ruleset = {}
    self.rows = []
    ready = {}
    raw = {}
    counter = 0
    max_l = 0

    def parse_rule(rule_id):
      nonlocal raw, ready, counter, with_loops
      counter += 1
      if counter > 1000000:
        raise Exception("Too many iterations")

      if rule_id in ready:
        return ready[rule_id]

      res = []
      for ruleset in raw[rule_id].split("|"):
        ltr = letter_regex.match(ruleset)
        sub_res = []
        if ltr:
          res.append(ltr.group(1))
          continue

        for sub_id in id_list_regex.findall(ruleset):
          sub_res.append(parse_rule(sub_id))

        # Hardcoded cheats
        if with_loops and rule_id == "8":
          # 8: 42 | 42 8 => at least one or more repetittion of pattern 42
          res.append(sub_res[0] + "+")
        elif with_loops and rule_id == "11":
          # 11: 42 31 | 42 11 31 => n repeats of 42, followed by n repeats of 31
          r42, r31 = sub_res
          sub_res = []
          for ii in range(1, max_l):
            sub_res.append("{}{}".format(
              "{}{{{}}}".format(r42, ii),
              "{}{{{}}}".format(r31, ii),
            ))
          res.append("(" + "|".join(sub_res) + ")")
        else:
          res.append("".join(sub_res))

      ready[rule_id] = "".join(res)
      if len(res) > 1:
        ready[rule_id] = "({})".format("|".join(res))

      return ready[rule_id]

    rule_mode = True
    for row in raw_input:
      if len(row) < 1:
        rule_mode = False
        continue

      if rule_mode:
        rule_id, rule = row.split(": ")
        raw[rule_id] = rule
        continue

      self.rows.append(row)
      max_l = max(len(row), max_l)

    for rule_id in raw:
      self.ruleset[rule_id] = parse_rule(rule_id)

  def count_valid(self, rule_to_match):
    rule_string = self.ruleset["{}".format(rule_to_match)]
    rule = re.compile("^{}$".format(rule_string))
    counter = 0
    for row in self.rows:
      if rule.match(row):
        counter += 1

    return counter


