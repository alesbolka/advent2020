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

        if aa + bb + cc== target:
          return aa, bb, cc, aa * bb * cc
