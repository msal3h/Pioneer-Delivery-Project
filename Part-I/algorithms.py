"""Greedy scheduling algorithms for Pioneer Delivery."""
from dataclasses import dataclass
import heapq


@dataclass(frozen=True)
class Delivery:
    id: str
    start: int
    finish: int

    def __post_init__(self):
        if self.start >= self.finish:
            raise ValueError(f'{self.id}: start must be before finish')


def maximum_deliveries(deliveries: list[Delivery]) -> list[Delivery]:
    """Task A: earliest-finish-time interval scheduling, O(n log n)."""
    ordered = sorted(deliveries, key=lambda d: (d.finish, d.start, d.id))
    selected = []
    last_finish = float('-inf')
    for delivery in ordered:
        if delivery.start >= last_finish:
            selected.append(delivery)
            last_finish = delivery.finish
    return selected


def minimum_drivers(deliveries: list[Delivery]) -> list[list[Delivery]]:
    """Task B: interval partitioning with a min-heap, O(n log n)."""
    ordered = sorted(deliveries, key=lambda d: (d.start, d.finish, d.id))
    heap = []  # (next available time, driver index)
    schedules: list[list[Delivery]] = []
    for delivery in ordered:
        if heap and heap[0][0] <= delivery.start:
            _, driver = heapq.heappop(heap)
        else:
            driver = len(schedules)
            schedules.append([])
        schedules[driver].append(delivery)
        heapq.heappush(heap, (delivery.finish, driver))
    return schedules


def minimum_rejections(deliveries: list[Delivery]) -> int:
    """Task C: total requests minus maximum compatible requests."""
    return len(deliveries) - len(maximum_deliveries(deliveries))


@dataclass(frozen=True)
class FlexibleDelivery:
    id: str
    ready: int
    profit: int

    def __post_init__(self):
        if self.ready < 0 or self.profit <= 0:
            raise ValueError('Ready times must be nonnegative and profits positive')


def greedy_profit_schedule(deliveries: list[FlexibleDelivery]):
    """Task D: manager's proposed (not always optimal) strategy."""
    occupied = set()
    result = []
    for delivery in sorted(deliveries, key=lambda d: -d.profit):
        slot = delivery.ready
        while slot in occupied:
            slot += 1
        occupied.add(slot)
        result.append((delivery, slot))
    return result


def schedule_value(schedule) -> float:
    return sum(d.profit / (1 + slot - d.ready) for d, slot in schedule)


def validate_flexible_schedule(schedule):
    slots = [slot for _, slot in schedule]
    return len(slots) == len(set(slots)) and all(slot >= d.ready for d, slot in schedule)
