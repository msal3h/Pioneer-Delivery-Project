"""Divide-and-conquer algorithms for Pioneer Delivery, Part II."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    id: str
    x: int
    y: int


def squared_distance(a, b):
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


def closest_pair(points):
    """Return (point1, point2, squared_distance) in O(n log n) time."""
    if len(points) < 2:
        raise ValueError('At least two locations are required')
    if len({p.id for p in points}) != len(points):
        raise ValueError('Location IDs must be unique')
    if len({(p.x, p.y) for p in points}) != len(points):
        raise ValueError('Locations must have different coordinates')
    px = sorted(points, key=lambda p: (p.x, p.y, p.id))
    py = sorted(points, key=lambda p: (p.y, p.x, p.id))

    def solve(x_sorted, y_sorted):
        n = len(x_sorted)
        if n <= 3:
            best = None
            for i in range(n):
                for j in range(i + 1, n):
                    candidate = (x_sorted[i], x_sorted[j], squared_distance(x_sorted[i], x_sorted[j]))
                    if best is None or candidate[2] < best[2]:
                        best = candidate
            return best

        mid = n // 2
        left_x, right_x = x_sorted[:mid], x_sorted[mid:]
        left_ids = {p.id for p in left_x}
        left_y = [p for p in y_sorted if p.id in left_ids]
        right_y = [p for p in y_sorted if p.id not in left_ids]
        left_best = solve(left_x, left_y)
        right_best = solve(right_x, right_y)
        best = left_best if left_best[2] <= right_best[2] else right_best
        d2 = best[2]
        dividing_x = right_x[0].x
        strip = [p for p in y_sorted if (p.x - dividing_x) ** 2 < d2]
        for i, p in enumerate(strip):
            for q in strip[i + 1:i + 8]:
                if (q.y - p.y) ** 2 >= d2:
                    break
                candidate_d2 = squared_distance(p, q)
                if candidate_d2 < d2:
                    best = (p, q, candidate_d2)
                    d2 = candidate_d2
        return best

    return solve(px, py)


def count_inversions(planned, actual):
    """Count pairs reversed relative to planned order, O(n log n)."""
    if len(planned) != len(actual) or len(set(planned)) != len(planned) or set(planned) != set(actual):
        raise ValueError('Planned and actual must contain the same distinct IDs')
    if not planned:
        raise ValueError('At least one delivery is required')
    rank = {delivery: i for i, delivery in enumerate(planned)}
    values = [rank[delivery] for delivery in actual]

    def sort_count(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, left_count = sort_count(a[:mid])
        right, right_count = sort_count(a[mid:])
        merged, i, j = [], 0, 0
        total = left_count + right_count
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
                total += len(left) - i
        merged.extend(left[i:]); merged.extend(right[j:])
        return merged, total

    return sort_count(values)[1]


def kth_smallest(times, k):
    """Deterministic median-of-medians selection, 1-based k, O(n) worst case."""
    if not times or any(not isinstance(t, int) or t < 0 for t in times):
        raise ValueError('Times must be a nonempty list of nonnegative integers')
    if not isinstance(k, int) or not 1 <= k <= len(times):
        raise ValueError('k must be between 1 and the number of times')

    def select(values, rank):
        if len(values) <= 5:
            return sorted(values)[rank - 1]
        medians = []
        for i in range(0, len(values), 5):
            group = sorted(values[i:i + 5])
            medians.append(group[len(group) // 2])
        pivot = select(medians, (len(medians) + 1) // 2)
        low = [x for x in values if x < pivot]
        equal = [x for x in values if x == pivot]
        high = [x for x in values if x > pivot]
        if rank <= len(low):
            return select(low, rank)
        if rank <= len(low) + len(equal):
            return pivot
        return select(high, rank - len(low) - len(equal))

    return select(list(times), k)
