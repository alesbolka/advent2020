from functools import reduce

def find_pair(raw_input, target):
  input_length = len(raw_input)

  for ii in range(input_length - 1):
    for jj in range(ii+1, input_length):
      aa = int(raw_input[ii])
      bb = int(raw_input[jj])

      if aa + bb == target:
        return aa, bb, aa * bb

def find_triple(raw_input, target):
  input_length = len(raw_input)

  for ii in range(input_length - 1):
    for jj in range(ii+1, input_length):
      for kk in range(jj+1, input_length):
        aa = int(raw_input[ii])
        bb = int(raw_input[jj])
        cc = int(raw_input[kk])

        if aa + bb + cc == target:
          return aa, bb, cc, aa * bb * cc

def find_dynamic(raw_input, target, num):
  inp_len = len(raw_input)

  if inp_len < num:
    raise "Input list has a length of {} while expecting to match {} numbers".format(inp_len, num)

  for ii in range(inp_len):
    raw_input[ii] = int(raw_input[ii])

  indexes = []
  for ii in range(num):
    indexes.append(ii)

  def step():
    min_ii = num

    for ii in range(num):
      max_index = inp_len - 1 - ii
      indexes[num - 1 - ii] += 1

      if indexes[num - 1 - ii] <= max_index:
        break

      min_ii = num - ii - 1

    if indexes[num - 1] > inp_len:
      raise "Maximum index reached with no match"


  while True:
    val = 0
    for ii in indexes:
      val += raw_input[ii]

    if val == target:
      res = []
      for ii in indexes:
        res.append(raw_input[ii])
      res.append(reduce((lambda x, y: x * y), res))
      return res

    step()
