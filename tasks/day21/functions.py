def parse_input(raw_input):
  allergies = {}
  ings = {}
  appear = {}

  def check(alg):
    nonlocal allergies, ings
    if len(allergies[alg]) != 1:
      return

    food = allergies[alg][0]
    allergies[alg] = []
    ings[food] = alg
    for othr in allergies:
      if food not in allergies[othr]:
        continue
      allergies[othr].remove(food)
      if len(allergies[othr]) == 1:
        check(othr)

  for row in raw_input:
    ingredients_raw, allergens_raw = row.split(" (contains ")
    allergens = allergens_raw[:-1].split(", ")
    ingredients = [xx.strip() for xx in ingredients_raw.split(" ")]
    for ing in ingredients:
      if ing not in ings:
        ings[ing] = None
        appear[ing] = 0
      appear[ing] += 1

    for allergen in allergens:
      if allergen not in allergies:
        allergies[allergen] = ingredients
        continue
      allergies[allergen] = [xx for xx in allergies[allergen] if xx in ingredients]

      check(allergen)

  print("Appearances of non-allergenic ingredients:", sum([appear[xx] for xx in ings if not ings[xx]]))

  flipped = { alg: ing for ing, alg in ings.items() if alg }
  order = list(flipped.keys())
  order.sort()
  print(",".join([flipped[alg] for alg in order]))

