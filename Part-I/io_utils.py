"""File input: each non-comment line contains ID START FINISH."""
from pathlib import Path
from algorithms import Delivery


def read_deliveries(path: str | Path) -> list[Delivery]:
    deliveries = []
    seen = set()
    for number, raw in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(f'Line {number}: expected ID START FINISH')
        identifier, start, finish = parts
        if identifier in seen:
            raise ValueError(f'Line {number}: duplicate ID {identifier}')
        try:
            delivery = Delivery(identifier, int(start), int(finish))
        except ValueError as exc:
            raise ValueError(f'Line {number}: {exc}') from exc
        seen.add(identifier)
        deliveries.append(delivery)
    return deliveries
