"""Run all four tasks from the VS Code terminal."""
import argparse
from algorithms import (FlexibleDelivery, greedy_profit_schedule,
                        maximum_deliveries, minimum_drivers,
                        minimum_rejections, schedule_value)
from io_utils import read_deliveries


def run(path):
    deliveries = read_deliveries(path)
    print(f'Loaded {len(deliveries)} deliveries from {path}')
    print('\nTASK A — Maximum deliveries for one driver')
    selected = maximum_deliveries(deliveries)
    for d in selected:
        print(f'  {d.id}: {d.start} -> {d.finish}')
    print(f'Total deliveries completed: {len(selected)}')

    print('\nTASK B — Minimum number of drivers')
    schedules = minimum_drivers(deliveries)
    for i, schedule in enumerate(schedules, 1):
        print(f'Driver {i}: ' + ', '.join(f'{d.id} ({d.start}-{d.finish})' for d in schedule))
    print(f'Minimum drivers required: {len(schedules)}')

    print('\nTASK C — Minimum rejected deliveries')
    print(f'Minimum deliveries rejected: {minimum_rejections(deliveries)}')

    print('\nTASK D — Counterexample to profit-first greedy')
    # Greedy: B at 0, A at 1, C at 2 (value 4.5).
    # Better: B at 0, C at 1, A at 2 (value 14/3).
    a = FlexibleDelivery('A', 0, 2)
    b = FlexibleDelivery('B', 0, 3)
    c = FlexibleDelivery('C', 1, 1)
    greedy = greedy_profit_schedule([a, b, c])
    better = [(b, 0), (c, 1), (a, 2)]
    for title, schedule in [('Greedy G', greedy), ('Better S', better)]:
        print(f'{title}:')
        for d, slot in schedule:
            print(f'  {d.id}: ready={d.ready}, profit={d.profit}, slot={slot}, delay={slot-d.ready}, value={d.profit/(1+slot-d.ready):.2f}')
        print(f'  Total value: {schedule_value(schedule):.2f}')
    print('Because 14/3 > 9/2, greedy G is not always optimal.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pioneer Delivery scheduling')
    parser.add_argument('file', nargs='?', default='data/deliveries.txt', help='Path to delivery data file')
    args = parser.parse_args()
    run(args.file)
