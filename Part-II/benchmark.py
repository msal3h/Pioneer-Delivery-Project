"""Repeatable approximate timing measurements; run from the Part-II folder."""
import random
from time import perf_counter
from algorithms import Point, closest_pair, count_inversions, kth_smallest


def measure(fn):
    start = perf_counter()
    fn()
    return (perf_counter() - start) * 1000


def benchmark():
    rng = random.Random(413)
    print('n,closest_pair_ms,inversions_ms,selection_ms')
    for n in (100, 1000, 5000):
        points = [Point(str(i), i, rng.randrange(100000)) for i in range(n)]
        planned = list(range(n))
        actual = planned[:]
        rng.shuffle(actual)
        times = [rng.randrange(1000) for _ in range(n)]
        a = measure(lambda: closest_pair(points))
        b = measure(lambda: count_inversions(planned, actual))
        c = measure(lambda: kth_smallest(times, (n + 1)//2))
        print(f'{n},{a:.3f},{b:.3f},{c:.3f}')


if __name__ == '__main__': benchmark()
