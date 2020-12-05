def parse_seats(raw_input):
  seats = {}
  for line in raw_input:
    if len(line) < 1:
      continue
    row = int(line[:7].replace("F", "0").replace("B", "1"), 2)
    seat = int(line[7:].replace("R", "1").replace("L", "0"), 2)
    seat_id = row * 8 + seat
    seats[seat_id] = (row, seat, seat_id)

  return seats

def find_highest_seat_id(seats):
  return max(seats,  key=int)

def find_empty(seats):
  ids = sorted(seats)
  for seat_id in ids:
    if (seat_id + 1) not in seats and (seat_id + 2) in seats:
      return seat_id + 1
