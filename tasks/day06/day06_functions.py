def count_total_sum(raw_input):
  res = 0
  group_str = ""
  for row in raw_input:
    group_str += row
    if len(row) < 1:
      res += len(set(group_str))
      group_str = ""

  if len(group_str) > 0:
    res += len(set(group_str))

  return res

def count_group_common(raw_input):
  res = 0
  group_count = 0
  group_data = {}
  for row in raw_input:
    if len(row) < 1:
      for key in group_data:
        if group_data[key] == group_count:
          res += 1

      group_data = {}
      group_count = 0
      continue

    group_count += 1

    for qq in row:
      if qq not in group_data:
        group_data[qq] = 0

      group_data[qq] += 1

  if group_count > 0:
    for key in group_data:
      if group_data[key] == group_count:
        res += 1

  return res