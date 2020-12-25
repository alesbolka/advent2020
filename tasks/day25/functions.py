class Crypto:
  def __init__(self, loop = 0, const = 20201227):
    self.const = const
    self.loop = loop

  def reverse_engineer(target, subject_number, constant = 20201227):
    cry = Crypto(const = constant)
    val = 1
    ii = 0
    seen = {}
    while val not in seen:
      seen[val] = True
      ii += 1
      val *= subject_number
      val = val % constant
      if val == target:
        cry.loop = ii
        return cry

    raise Exception("Recursion detected")

  def sign(self, num):
    val = 1
    for ii in range(self.loop):
      val *= num
      val = val % self.const
    return val


def part1(raw):
  card_pub, door_pub = int(raw[0]), int(raw[1])
  card = Crypto.reverse_engineer(card_pub, 7)
  door = Crypto.reverse_engineer(door_pub, 7)

  print(card.sign(door_pub), door.sign(card_pub))
  # doorPublic = Crypto(subj=7, loop=2)
  # cardPublic = Crypto(subj=7, loop=2)
