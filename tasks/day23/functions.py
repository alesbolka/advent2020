class Cup:
  def __init__(self, label):
    self.label = label
    self.next = None

class Game:
  def __init__(self, initial, min_lenght = 0):
    self.cups = {}
    prev = None
    ii = 0
    min_lenght = max(min_lenght, len(initial))

    while ii < min_lenght:
      if ii < len(initial):
        ch = int(initial[ii])
      else:
        ch = ii + 1

      cur = Cup(ch)
      self.cups[ch] = cur
      if prev:
        prev.next = cur
      else:
        self.current = cur
        self.min = ch
        self.max = ch

      self.min = min(self.min, ch)
      self.max = max(self.max, ch)

      prev = cur
      ii += 1

    self.cups[prev.label].next = self.current

  def play(self, moves = 100):
    for ii in range(moves):
      self.move()

  def move(self):
    removed = []

    for ii in range(3):
      removed.append(self.current.next.label)
      self.current.next = self.current.next.next

    label = self.current.label - 1

    while label in removed or label not in self.cups:
      label -= 1
      if label < self.min:
        label = self.max

    for ii in removed:
      tmp = self.cups[label].next
      self.cups[label].next = self.cups[ii]
      self.cups[ii].next = tmp
      label = ii

    self.current = self.current.next

  def part1_label(self):
    res = ""
    nxt = self.cups[1].next

    while nxt != self.cups[1]:
      res += str(nxt.label)
      nxt = nxt.next
    return res

  def part2_label(self):
    nxt = self.cups[1].next
    return nxt.label * nxt.next.label