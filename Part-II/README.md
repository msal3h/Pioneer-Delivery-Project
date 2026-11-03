# Pioneer Delivery — Part II

Python 3 project for the divide-and-conquer assignment. No external packages needed.

## Run in VS Code

Open the `Part-II` folder, then use the terminal:

```bash
python3 main.py A    # closest locations
python3 main.py B    # dispatch inversions
python3 main.py C    # kth smallest time
python3 -m unittest discover -s tests -v
python3 benchmark.py
```

Edit the JSON files in `data/` to try your own inputs. `main.py` reads the corresponding file and prints the answer. The algorithm functions can also be imported independently from `algorithms.py`.

## Files

- `algorithms.py` — Tasks A, B, C
- `main.py` — runs one task at a time
- `data/` — sample JSON input files
- `tests/test_algorithms.py` — required cases, extra cases, and reference checks
- `benchmark.py` — timing measurements
- `Task-D-report.pdf` — short design and testing report

## Input formats

- **A** (`locations.json`): a JSON list of `{ "id": "A", "x": 0, "y": 0 }` objects. At least two unique IDs and distinct coordinates.
- **B** (`orders.json`): `{ "planned": ["A", "B"], "actual": ["B", "A"] }`. Both lists must contain the same distinct IDs.
- **C** (`times.json`): `{ "times": [18, 4, 29], "k": 2 }`. Nonnegative integer times; k is 1-based.

Invalid input raises a clear `ValueError` from the algorithms; the command-line runner prints an error message.

## Required test results

| Task | Cases | Expected / observed |
|---|---|---|
| A | A1, A2, A3, A4 | 25, 1, 16, 9 |
| B | B1, B2, B3, B4 | 2, 0, 6, 0 |
| B | 100,000 reversed IDs | 4,999,950,000 |
| C | C1, C2, C3, C4, C5 | 16, 4, 35, 7, 3 |

Extra cases include tied closest pairs, a single inversion, sorted and reverse-sorted times, and many duplicates. Random small inputs are compared against simple reference solutions. All tests passed.

The PDF report contains the algorithm explanations, complexity analysis, and measured performance results.
