"""Run individual tasks: python3 main.py A|B|C"""
import json
import sys
from pathlib import Path
from algorithms import Point, closest_pair, count_inversions, kth_smallest

DATA = Path(__file__).parent / 'data'


def main():
    if len(sys.argv) != 2 or sys.argv[1].upper() not in ('A', 'B', 'C'):
        print('Usage: python3 main.py A|B|C')
        return 1
    task = sys.argv[1].upper()
    try:
        if task == 'A':
            points = [Point(**item) for item in json.loads((DATA / 'locations.json').read_text())]
            a, b, d2 = closest_pair(points)
            print(f'Closest locations: {a.id}, {b.id}; squared distance: {d2}')
        elif task == 'B':
            orders = json.loads((DATA / 'orders.json').read_text())
            print(f'Inversions: {count_inversions(orders["planned"], orders["actual"])}')
        else:
            data = json.loads((DATA / 'times.json').read_text())
            print(f'kth smallest time: {kth_smallest(data["times"], data["k"])}')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
