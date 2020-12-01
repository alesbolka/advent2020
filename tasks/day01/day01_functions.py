def find_pair(raw_input, target):
  input_length = len(raw_input)

  for ii in range(input_length - 1):
    for jj in range(ii+1, input_length):
      aa = int(raw_input[ii])
      bb = int(raw_input[jj])

      if aa + bb == target:
        return aa, bb, aa * bb
