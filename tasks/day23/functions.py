class Game:
  def __init__(self, initial, min_lenght = 0):
    self.cups = [int(ch) for ch in initial]
    current = max(self.cups)
    while len(self.cups) < min_lenght:
      current += 1
      self.cups.append(current)

    self.current = self.cups[0]
    self.min = min(self.cups)
    self.max = max(self.cups)
    self.len = len(self.cups)

  def play(self, moves = 100):
    for ii in range(moves):
      self.move()
    return self.get_label()

  def move(self):
    removed = []

    for ii in range(3):
      remove_index = (self.cups.index(self.current) + 1) % len(self.cups)
      removed.append(self.cups.pop(remove_index))

    label = self.current - 1

    while label not in self.cups:
      label -= 1
      if label < self.min:
        label = self.max

    destination = self.cups.index(label)
    self.cups = (
      self.cups[:destination + 1] +
      removed +
      self.cups[destination + 1:]
    )

    next_index = (self.cups.index(self.current) + 1) % self.len
    self.current = self.cups[next_index]

  def get_label(self):
    index1 = self.cups.index(1)
    res = ""
    for ii in range(1, self.len):
      res += str(self.cups[(ii + index1) % self.len])

    return res
    # return ""