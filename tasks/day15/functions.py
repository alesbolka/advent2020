def iterate(row, stop = 2020):
  mem =  {}
  ii = 0
  last = -1
  for num in row.split(","):
    num = int(num)
    ii += 1
    mem[num] = (ii, None)
    last = num


  while ii < stop:
    ii += 1

    if not mem[last][1]:
      # number was said for the first time
      to_say = 0
    else:
      to_say = mem[last][0] - mem[last][1]

    if to_say in mem:
      mem[to_say] = (ii, mem[to_say][0])
    else:
      mem[to_say] = (ii, None)
    last = to_say

  return last