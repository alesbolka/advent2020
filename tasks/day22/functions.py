class Player:
  def __init__(self, player_id):
    self.id = player_id
    self.deck = []

  def draw(self):
    return self.deck.pop(0)

  def win(self, cards):
    cards.sort(reverse = True)
    self.deck += cards

class Game:
  def __init__(self, players):
    self.players = players
    self.memory = {}
    self.games = 0

  def active(self):
    return [pp for pp in self.players if len(pp.deck) > 0]

  def play(self):
    act = self.active()
    ii = 0
    while len(act) > 1:
      ii += 1
      board = [player.draw() for player in act]
      max_val = max(board)
      act[board.index(max_val)].win(board)
      act = self.active()
      if ii > 10000:
        raise Exception("Too many rounds")

    deck = act[0].deck
    return sum([(len(deck) - ii) * deck[ii] for ii in range(len(deck))])

  def recursive_combat(self, decks):
    gameId = "-".join([str(ii) + str(decks[ii]) for ii in range(len(decks))])
    if gameId in self.memory:
      return self.memory[gameId]

    self.games += 1
    game = self.games
    if len(decks) != 2:
      # half the code works for any number of decks, did not want to adapt
      raise Exception("Lazy late check, logic is not adapted to be dynamic")

    active = [deck for deck in decks if len(deck) > 0]
    self.ii = 0
    used = {}
    while len(active) > 1:
      self.ii += 1
      roundId = "-".join([str(ii) + str(decks[ii]) for ii in range(len(active))])
      if roundId in used:
        return 0
      used[roundId] = True
      board = [deck.pop(0) for deck in active]
      sub_decks = [active[ii][:board[ii]] for ii in range(len(board)) if board[ii] <= len(active[ii])]
      if len(sub_decks) == len(active):
        winner = self.recursive_combat(sub_decks)
        board = [board[winner], board[(winner + 1) % 2]]
      else:
        max_val = max(board)
        winner = board.index(max_val)
        board.sort(reverse = True)
      active[winner] += board
      active = [deck for deck in active if len(deck) > 0]

      if self.ii > 10000:
        raise Exception("too many iterations")


    if game > 1:
      ls = [len(xx) for xx in decks]
      if len([ll for ll in ls if ll > 0]) != 1:
        raise Exception("math fail")
      self.memory[gameId] = ls.index(max(ls))
      return self.memory[gameId]

    return sum([(len(active[0]) - ii) * active[0][ii] for ii in range(len(active[0]))])

def parse_input(raw):
  players = []
  for row in raw:
    if row.startswith("Player "):
      players.append(Player(row[:-1]))
    elif len(row) > 0:
      players[-1].deck.append(int(row))

  return players
