import random
import unittest
from algorithms import Point, closest_pair, count_inversions, kth_smallest, squared_distance


class AlgorithmTests(unittest.TestCase):
    def test_a_required(self):
        cases = [
            ([('A',0,0),('B',3,4)],25),
            ([('A',0,0),('B',7,2),('C',4,5),('D',5,5),('E',12,2),('F',2,9)],1),
            ([('A',-3,1),('B',-3,11),('C',1,1),('D',2,15)],16),
            ([('A',-5,-5),('B',-5,-2),('C',6,8)],9),
        ]
        for items, expected in cases:
            pts = [Point(*item) for item in items]
            a,b,d2 = closest_pair(pts)
            self.assertEqual(d2, expected)
            self.assertEqual(d2, squared_distance(a,b))
        a,b,d2 = closest_pair([Point('A',0,0),Point('B',1,0),Point('C',2,0)])
        self.assertEqual(d2, 1)  # additional: tied closest pairs
        with self.assertRaises(ValueError): closest_pair([Point('A',0,0)])

    def test_b_required(self):
        cases = [
            (['A','B','C','D','E'],['A','C','D','B','E'],2),
            (['A','B','C','D'],['A','B','C','D'],0),
            (['A','B','C','D'],['D','C','B','A'],6),
            (['A'],['A'],0),
        ]
        for planned, actual, expected in cases:
            self.assertEqual(count_inversions(planned,actual),expected)
        self.assertEqual(count_inversions([1,2,3],[2,1,3]),1) # additional
        n=100_000
        self.assertEqual(count_inversions(list(range(n)),list(range(n-1,-1,-1))),4_999_950_000)
        with self.assertRaises(ValueError): count_inversions(['A'],['B'])

    def test_c_required(self):
        times = [18,4,29,11,4,16,35,9,22]
        for k, expected in [(5,16),(2,4),(9,35)]:
            self.assertEqual(kth_smallest(times,k),expected)
        self.assertEqual(kth_smallest([7]*6,4),7)
        self.assertEqual(kth_smallest([8,3],1),3)
        for values in [list(range(20)),list(range(19,-1,-1)),[2]*100+[1]*50+[3]*70]:
            for k in (1,len(values)//2,len(values)):
                self.assertEqual(kth_smallest(values,k),sorted(values)[k-1])
        with self.assertRaises(ValueError): kth_smallest([1,2],3)

    def test_random_reference_checks(self):
        rng = random.Random(413)
        for n in range(2,30):
            pts = [Point(str(i), i, rng.randrange(-100,100)) for i in range(n)]
            expected = min(squared_distance(pts[i],pts[j]) for i in range(n) for j in range(i+1,n))
            self.assertEqual(closest_pair(pts)[2],expected)
        for n in range(1,35):
            planned=list(range(n)); actual=planned[:]; rng.shuffle(actual)
            expected=sum(actual[i]>actual[j] for i in range(n) for j in range(i+1,n))
            self.assertEqual(count_inversions(planned,actual),expected)
            vals=[rng.randrange(10) for _ in range(n)]
            for k in range(1,n+1):
                self.assertEqual(kth_smallest(vals,k),sorted(vals)[k-1])


if __name__ == '__main__': unittest.main()
