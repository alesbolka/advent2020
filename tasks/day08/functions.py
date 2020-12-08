class GameOS:
  def __init__(self, code):
    self.index = 0
    self.instructions = []
    self.accumulator = 0
    self.source = []
    for instruction in code:
      op, arg = instruction.split(" ")
      self.source.append((op, int(arg)))
      self.instructions.append((op, int(arg)))

  def execute_till_repeat(self):
    try:
      return self.execute()
    except Exception:
      return self.accumulator

  def execute(self):
    self.index = 0
    self.accumulator = 0
    visited = []
    while self.index >= 0 and self.index < len(self.instructions):
      if self.index in visited:
        raise Exception("duplicate")
      com, arg = self.instructions[self.index]
      func = getattr(self, "command_{}".format(com), "command_invalid")
      visited.append(self.index)
      func(com, arg) # pylint: disable=not-callable

    return self.accumulator

  def find_simple_solution(self, replacements):
    for ii in range(len(self.source)):
      com, arg = self.source[ii]
      if com not in replacements:
        continue

      self.instructions = [xx for xx in self.source]
      self.instructions[ii] = (replacements[com], arg)
      try:
        return self.execute()
      except Exception:
        pass

  def command_acc(self, com, arg):
    self.accumulator += arg
    self.index += 1
    pass

  def command_jmp(self, com, arg):
    self.index += arg
    pass

  def command_nop(self, com, arg):
    self.index += 1
    pass

  def command_invalid(self, com, arg):
    print("Invalid command {} {} at index {}".format(com, arg, self.index))
    self.index = -1


