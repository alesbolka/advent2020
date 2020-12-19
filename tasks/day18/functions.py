import math
import re

addition_regex = re.compile(r"([0-9]+)\s*\+\s*([0-9]+)")
parentheses_regex = re.compile(r"\(([0-9\s\+\*\-]+)\)")

def evaluate(expression, start = 0):
  res = 1
  num_str = ""
  op = "*"
  ii = start

  def do_math():
    nonlocal res, num_str
    if len(num_str) < 1:
      return

    if op == "+":
      res += int(num_str)
    elif op == "-":
      res -= int(num_str)
    elif op == "*":
      res *= int(num_str)
    else:
      print("Invalid operator {}".format(op))
      raise Exception("Evaluate error")
    num_str = ""

  while ii < len(expression):
    ch = expression[ii]
    if ch.isnumeric():
      num_str += ch
    elif ch == "(":
      num_str, ii = evaluate(expression, ii+1)
      if ii < 0:
        raise Exception("Unexpected return from subloop")
    elif ch == ")":
      do_math()
      return "{}".format(res), ii
    elif ch == " ":
      do_math()
    elif ch in ["*", "-", "+"]:
      op = ch
    else:
      print("Invalid symbol {}".format(ch))
      raise Exception("Evaluate error")

    ii += 1

  do_math()
  return res, -1

def adv_math(expression):
  def add(match):
    xx, yy = match.groups()
    return "{}".format(int(xx) + int(yy))

  def small_part(match):
    return "{}".format(adv_math(match.groups()[0]))

  while len(parentheses_regex.findall(expression)) > 0:
    # print(expression)
    expression = parentheses_regex.sub(small_part, expression)

  while len(addition_regex.findall(expression)) > 0:
    # print(expression)
    expression = addition_regex.sub(add, expression)

  # print("final", expression)
  return math.prod([int(xx.strip()) for xx in expression.split("*")])
