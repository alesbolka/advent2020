from itertools import combinations

class Sequencer:
  def __init__(self, sequence, raw_input):
    self.sequence = sequence
    self.list = list(map(lambda x: int(x), raw_input))

  def can_be_added(self, index):
    sub_list = self.list[index - self.sequence : index]
    num = self.list[index]
    for pair in combinations(sub_list, 2):
      if (pair[0] + pair[1]) == num:
        return True

    return False

  def find_first_invalid(self):
    ii = -1
    for num in self.list:
      ii += 1
      if ii < self.sequence:
        continue

      if not self.can_be_added(ii):
        return (ii, num)

    return (-1, 0)

  def find_contiguous_set(self, index):
    for ii in range(index):
      total = self.list[ii]

      for jj in range(ii + 1, index):
        total += self.list[jj]

        if total == self.list[index]:
          sub_list = self.list[ii:jj]
          return max(sub_list) + min(sub_list)

        if total > self.list[index]:
          break

    return False
