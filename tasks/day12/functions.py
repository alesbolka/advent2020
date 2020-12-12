class NavSystem:
  def __init__(self, deg):
    # clockwise radial, 0 = north
    self.deg = (deg + 360) % 360
    self.xx = 0
    self.yy = 0

  def sail(self, instructions):
    for nav in instructions:
      val = int(nav[1:])
      cmd = nav[0]
      if cmd == "N" or cmd == "F" and self.deg == 0:
        self.yy += val
      elif cmd == "S" or cmd == "F" and self.deg == 180:
        self.yy -= val
      elif cmd == "E" or cmd == "F" and self.deg == 90:
        self.xx += val
      elif cmd == "W" or cmd == "F" and self.deg == 270:
        self.xx -= val
      elif cmd == "R":
        if (val % 90) > 0:
          raise Exception("Invalid angle {}".format(val))
        self.deg = (360 + self.deg + val) % 360
      elif cmd == "L":
        if (val % 90) > 0:
          raise Exception("Invalid angle {}".format(val))
        self.deg = (360 + self.deg - val) % 360
      else:
        raise Exception("Invalid command {}".format(cmd))

  def waypoint_navigation(self, instructions, wp_xx = 10, wp_yy = 1):
    for nav in instructions:
      val = int(nav[1:])
      cmd = nav[0]
      if cmd == "N":
        wp_yy += val
      elif cmd == "S":
        wp_yy -= val
      elif cmd == "E":
        wp_xx += val
      elif cmd == "W":
        wp_xx -= val
      elif cmd == "R":
        val = (val + 360) % 360
        if (val % 90) > 0:
          raise Exception("Invalid angle {}".format(val))
        while val > 0:
          tmp = wp_yy
          wp_yy = -wp_xx
          wp_xx = tmp
          val -= 90
      elif cmd == "L":
        val = (val + 360) % 360
        if (val % 90) > 0:
          raise Exception("Invalid angle {}".format(val))
        while val > 0:
          tmp = wp_yy
          wp_yy = wp_xx
          wp_xx = -tmp
          val -= 90
      elif cmd == "F":
        self.xx += val * wp_xx
        self.yy += val * wp_yy
      else:
        raise Exception("Invalid command {}".format(cmd))

  def mht(self, xx = 0, yy = 0):
    return abs(xx - self.xx) + abs(yy - self.yy)

