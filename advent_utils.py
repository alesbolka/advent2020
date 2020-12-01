from pathlib import Path

def read_lines(path):
  file = Path(path)
  if not file.is_file:
    raise "Invalid input file provided: \"{0}\"".format(path)

  return file.read_text().splitlines()
