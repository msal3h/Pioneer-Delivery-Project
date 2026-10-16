# Pioneer Delivery — Part I

CS 413: Analysis of Algorithms  
Language: Python 3 

This program schedules delivery requests using greedy algorithms. It finds the most deliveries oe driver can take, the fewest drivers needed for all requests, and the minimum number of rejected requests. It also includes a counterexample where a greedy strategy fails.

## How to run

Open this folder in VS Code and run these commands in the terminal:

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

The first command runs the program with the sample data. The second runs the tests. To use another input file, run `python3 main.py path/to/file.txt`.

## Input file

The sample file is `data/deliveries.txt`. Each line contains a delivery ID, start time, and finish time, separated by spaces:

```text
D01 10 13
D02 2 5
D03 4 7
```

Times are integers and the start must be before the finish. Delivery IDs must be unique. A delivery can start right when another one ends.

## Files

- `main.py` runs the program and prints the results.
- `algorithms.py` contains the scheduling algorithms.
- `io_utils.py` reads and checks the input file.
- `data/deliveries.txt` contains sample deliveries.
- `tests/test_algorithms.y` contains the required test cases.

## Task A: Maximum deliveries for one driver

**Greedy choice:** Sort deliveries by finish time and select the next one that doesn't overlap with the last selected delivery.

**Why it works:** Choosing the delivery that ends earliest leaves as much time as possible for later deliveries. If an optimal schedule starts with a different delivery, we can replace it with the earliest-finishing one without losing any later deliveries. Repeating this gives an optimal schedule.

**Time complexity:** `O(n log n)` for sorting, followed by an `O(n)` scan, so `O(n log n)` overall.

## Task B: Minimum number of drivers

**Priority queue:** A min-heap stores each driver's finish time and driver number. The earliest available driver is at the top.

**Driver assignment:** Sort deliveries by start time. Reuse the earliest available driver if they finish by the next delivery's start time. Otherwise, add a driver. Update the heap after each assignment.

**Why it works:** A new driver is added only when all current drivers are busy. At that point, those overlapping deliveries require another driver, so adding one is necessary.

**Time complexity:** Sorting and heap operations take `O(n log n)` overall.

## Task C: Minimum rejected deliveries

This uses Task A. If there are `n` deliveries and the maximum compatible set contains `k`, the minimum rejected is **`n - k`**. Keeping any more than `k` would contradict Task A's maximum.

**Time complexity:** `O(n log n)`, since it uses Task A.

## Task D: Counterexample

The proposed greedy strategy schedules deliveries by highest profit first, using the earliest available slot. Each delivery takes one slot, and its value is `profit / (1 + delay)`.

| Delivery | Ready time | Profit |
|---|---:|---:|
| A | 0 | 2 |
| B | 0 | 3 |
| C | 1 | 1 |

**Greedy schedule:** B at time 0, A at time 1, C at time 2.

`V(G) = 3 + 2/2 + 1/2 = 4.5`

**Better schedule:** B at time 0, C at time 1, A at time 2.

`V(S) = 3 + 1 + 2/3 ≈ 4.67`

Both schedules follow the ready-time and non-overlap rules. Since `4.67 > 4.5`, the greedy strategy does not always give the best result.

## Required test results

Each task uses its own six test inputs from the assignment (the same test number does not necessarily mean the same intervals).

| Test | Task A: selected | Task B: drivers | Task C: rejected |
|---|---:|---:|---:|
| 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 3 | 1 | 0 |
| 4 | 1 | 3 | 2 |
| 5 | 3 | 2 | 1 |
| 6 | 2 | 2 | 1 |

All required cases pass. The tests also check that deliveries assigned to the same driver do not overlap.
