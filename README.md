My advent of code 2020 attempt.
I last touched python over 10 years ago at the uni, so I thought it would be a good exercise.

I tend to write my solutions in a way that expect the user to know some things about the task, they are not meant to be 100% reusable (maybe next year).
Example for running day 23:

```python
import time
from advent_utils import read_lines
import tasks.day23.functions as daily_code

t0 = time.time()

sample = read_lines('./tasks/day23/sample.txt')
dataset = read_lines('./tasks/day23/input.txt')

game = daily_code.Game(sample[1], 1000 * 1000)
game.play(10 * 1000 * 1000)
print("res 2", game.part2_label())



print("Execution time: {}".format(time.time() - t0))
```

Others might actually have clearly defined part 1 and 2 functions, depending on how lazy i was when writing this. The code is not nice, I just wanted to get it to work. If I failed obtaining the solution on my own, a README is present next to the code with a brief explanation.