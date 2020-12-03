class Grid:
  grid = []

  def __init__(self, input_lines):
    self.grid = input_lines

  def count_trees_basic(self, xx, yy, dx, dy):
    count = 0
    while yy < len(self.grid):
      xx += dx
      yy += dy

      if self.is_tree(xx, yy):
        count +=1


    return count

  def is_tree(self, xx, yy):
    if yy >= len(self.grid):
      return False

    real_x = xx % len(self.grid[yy])

    if self.grid[yy][real_x] == '#':
      return True

    return False
