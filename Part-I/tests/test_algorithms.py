import unittest
from algorithms import (Delivery, FlexibleDelivery, maximum_deliveries,
                        minimum_drivers, minimum_rejections,
                        greedy_profit_schedule, schedule_value,
                        validate_flexible_schedule)


def make(intervals):
    return [Delivery(f'D{i+1}', a, b) for i, (a, b) in enumerate(intervals)]


class SchedulingTests(unittest.TestCase):
    def test_task_a_all_required_cases(self):
        cases = [([], 0), ([(1, 3)], 1),
                 ([(1, 3), (3, 5), (5, 7)], 3),
                 ([(1, 5), (2, 6), (3, 7)], 1),
                 ([(5, 7), (1, 3), (3, 5), (2, 4)], 3),
                 ([(1, 4), (2, 4), (4, 6)], 2)]
        for intervals, expected in cases:
            with self.subTest(intervals=intervals):
                selected = maximum_deliveries(make(intervals))
                self.assertEqual(len(selected), expected)
                self.assertTrue(all(x.finish <= y.start for x, y in zip(selected, selected[1:])))

    def test_task_b_all_required_cases(self):
        cases = [([], 0), ([(1, 3)], 1),
                 ([(1, 3), (3, 5), (5, 7)], 1),
                 ([(1, 5), (2, 6), (3, 7)], 3),
                 ([(1, 4), (2, 5), (4, 7), (5, 8)], 2),
                 ([(5, 8), (1, 4), (2, 5), (4, 6), (6, 9)], 2)]
        for intervals, expected in cases:
            with self.subTest(intervals=intervals):
                schedules = minimum_drivers(make(intervals))
                self.assertEqual(len(schedules), expected)
                self.assertEqual(sum(map(len, schedules)), len(intervals))
                for schedule in schedules:
                    self.assertTrue(all(x.finish <= y.start for x, y in zip(schedule, schedule[1:])))

    def test_task_c_all_required_cases(self):
        cases = [([], 0), ([(1, 3)], 0),
                 ([(1, 3), (3, 5), (5, 7)], 0),
                 ([(1, 5), (2, 6), (3, 7)], 2),
                 ([(5, 7), (1, 3), (3, 5), (2, 4)], 1),
                 ([(1, 2), (2, 3), (3, 4), (1, 3)], 1)]
        for intervals, expected in cases:
            with self.subTest(intervals=intervals):
                self.assertEqual(minimum_rejections(make(intervals)), expected)

    def test_task_d_counterexample(self):
        a, b, c = FlexibleDelivery('A', 0, 2), FlexibleDelivery('B', 0, 3), FlexibleDelivery('C', 1, 1)
        greedy = greedy_profit_schedule([a, b, c])
        better = [(b, 0), (c, 1), (a, 2)]
        self.assertTrue(validate_flexible_schedule(greedy))
        self.assertTrue(validate_flexible_schedule(better))
        self.assertAlmostEqual(schedule_value(greedy), 4.5)
        self.assertAlmostEqual(schedule_value(better), 14/3)
        self.assertGreater(schedule_value(better), schedule_value(greedy))


if __name__ == '__main__':
    unittest.main()
